from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from django.core.exceptions import ValidationError


# Contexte Manager du model utilisateur personalisé
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("l'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(self, email, password, **extra_fields)


# Model utilisateur personalisé
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('company', 'Entreprise'),
        ('employee', 'Employé'),
        ('admin', 'Administrateur'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name or self.email.split("@")[0]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def is_company(self):
        return self.user_type == 'company'

    def is_employee(self):
        return self.user_type == 'employee'

    def is_admin(self):
        return self.user_type == 'admin'

    def verify_email_is_ok(self):
        self.is_email_verified = True
        self.is_active = True
        self.save()

    def complete_first_login(self):
        self.is_first_login = False
        self.save()

    def clean(self):
        super().clean()
        if self.is_company() and not hasattr(self, 'company_profile'):
            raise ValidationError(
                "Un utilisateur de type entreprise doit avoir un profil d'entreprise.")
        if self.is_employee() and not hasattr(self, 'employee_profile'):
            raise ValidationError(
                "Un utilisateur de type employé doit avoir un profil d'employé.")


# Convention collective
class ConventionCollective(models.Model):
    nom = models.CharField(max_length=155)

    def __str__(self) -> str:
        return self.nom or 'N/A'


# Model de Profile entreprise
class CompanyProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='company_profile')
    nom_entreprise = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    addresse = models.TextField(blank=True)
    code_postal = models.CharField(max_length=20, blank=True)
    convention_collective = models.ForeignKey(
        ConventionCollective, on_delete=models.CASCADE, blank=True, null=True)
    code_dexploitation = models.CharField(max_length=50, blank=True)
    cnss = models.CharField(max_length=50, blank=True)
    matricule_fiscale = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    registration_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    def complete_registration(self):
        self.registration_complete = False
        self.save()

    def clean(self):
        super().clean()
        if not self.user.is_company():
            raise ValidationError(
                "Le profil d'entreprise ne peut être associé qu'à un utilisateur de type entreprise.")

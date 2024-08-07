from .forms import CompanyRegistrationForm
from .forms import CustomUserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .utils import send_validation_email
from django.contrib import messages
from django.contrib.auth import get_user_model, login


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.verify_email_is_ok()
        messages.success(request, 'Votre email a été confirmé avec succès. Vous pouvez maintenant vous connecter.')
        return redirect('sign_in')
    else:
        messages.error(request, 'Le lien de confirmation est invalide ou a expiré.')
        return redirect('home_landing')


def home_landing(request):
    return render(request, 'payroll/landing/home.html')


def register_view(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_validation_email(request, user)
            return redirect('confirmation_email')
        else:
            messages.error(request, 'Une erreur est survenue')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'payroll/accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Session expires when browser closes

            messages.success(request, 'Connexion reussie ...!')

            return redirect('home-dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'payroll/accounts/login.html', {'form': form})


def sign_up_completion_view(request):
    return render(request, 'payroll/accounts/company_register_completion.html')


def dahsboard_home_view(request):
    return render(request, 'payroll/dashboard/home.html')


def user_profile_manage_view(request):
    return render(request, 'payroll/dashboard/manage_user_profile.html')


def profile_view(request):
    return render(request, 'payroll/dashboard/profile_company.html')


def edit_profile_view(request):
    return render(request, 'payroll/dashboard/edit_company_profile.html')


def confirmation_by_email_view(request):
    return render(request, 'payroll/accounts/confirmation_email.html')


"""
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                
                # Gestion de l'option "Se souvenir de moi"
                if form.cleaned_data.get('remember_me'):
                    # La session expirera lorsque le navigateur sera fermé
                    request.session.set_expiry(0)
                else:
                    # Définir une durée d'expiration de session personnalisée (par exemple, 2 semaines)
                    two_weeks = 14 * 24 * 60 * 60  # 14 jours en secondes
                    request.session.set_expiry(two_weeks)
                
                return redirect('home')  # Rediriger vers la page d'accueil après la connexion
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

"""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, CompanyProfile
from django import forms


class CompanyRegistrationForm(forms.ModelForm):
    company_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Les mots de passe ne correspondent pas")

        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.user_type = 'company'
        user.name = self.cleaned_data['company_name']

        if commit:
            user.save()
            CompanyProfile.objects.create(
                user=user, 
                nom_entreprise=self.cleaned_data['company_name']
            )
        
        return user

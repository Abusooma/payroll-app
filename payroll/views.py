from .forms import CompanyRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .utils import send_validation_email
from django.contrib import messages
from django.contrib.auth import get_user_model


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
        return redirect('home')


def home_landing(request):
    return render(request, 'payroll/landing/home.html')


def register_view(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_validation_email(request, user)  # Correction de l'ordre des arguments
            return redirect('confirmation_email')  # Ajout du return
        else:
            messages.error(request, 'Une erreur est survenue')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'payroll/accounts/register.html', {'form': form})


def login_view(request):
    return render(request, 'payroll/accounts/login.html')


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

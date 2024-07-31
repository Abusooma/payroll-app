from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CompanyRegistrationForm


def home_landing(request):
    return render(request, 'payroll/landing/home.html')


def register_view(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vous êtes connectez avec success ..!')
            return redirect('home-dashboard')
        else:
            messages.error(request, 'Une erreur est survenue')
            for error in list(form.errors.values()):
                print(error)
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

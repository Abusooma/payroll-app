from django.urls import path
from . import views

urlpatterns = [
    # URLS DE LANDING PAGES
    path('', views.home_landing, name='home_landing'),
    path('page/signup/', views.register_view, name='sign_up'),
    path('page/signup/completion/', views.sign_up_completion_view, name='sign_up_completion'),
    path('page/signin/', views.login_view, name='sign_in'),
    path('payroll-solution/register/success', views.confirmation_by_email_view, name='confirmation_email'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # URLS DE DASHBOARD PAGES
    path('payroll-solution/dashboard/', views.dahsboard_home_view, name='home-dashboard'),
    path('payroll-solution/dashboard/user-profile-manage', views.user_profile_manage_view, name='user-profile-manage'),
    path('payroll-solution/dashboard/profile-company', views.profile_view, name='profile-company'),
    path('payroll-solution/dashboard/edit_profile-company', views.edit_profile_view, name='edit_profile-company'),
]

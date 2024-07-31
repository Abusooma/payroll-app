from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .models import CompanyProfile
from PayrollSolution import settings


def create_company_profile(user):
    CompanyProfile.objects.create(
        user=user,
        nom_entreprise=user.name
    )
    group, created = Group.objects.get_or_create(name='Company')
    user.groups.add(group)


def send_email(subject, to_email, context, template_name):
    from_email = settings.EMAIL_HOST_USER
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_validation_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    validation_link = f"{request.scheme}://{current_site.domain}{activation_link}"

    context = {
        'username': user.name,
        'email': user.email,
        'validation_link': validation_link
    }
    subject = 'Validation de votre email'
    send_email(subject, user.email, context, template_name='payroll/emails/validation_email.html')

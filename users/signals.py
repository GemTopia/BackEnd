from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from GemTopia import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.user_name,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key
    }

    email_html_message = render_to_string('email/user_reset_password.html', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for GemTopia",
        # message:
        'Password Reset for GemTopia',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

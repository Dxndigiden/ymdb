from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER
from .configs import MAIL_CONFIG


def auth_send_mail(new_user: bool, user, code):
    """Отправляет пользователю сообщение с кодом на электронную почту."""
    recipient_list = [user.email, ]
    if new_user:
        subject = MAIL_CONFIG.get('new_user_mail_subject')
        message = MAIL_CONFIG.get(
            'new_user_message').format(
                username=user.username,
                code=code)
    else:
        subject = MAIL_CONFIG.get('user_mail_subject')
        message = MAIL_CONFIG.get(
            'user_mail_message').format(
                username=user.username,
                code=code)
    send_mail(subject=subject,
              message=message,
              from_email=EMAIL_HOST_USER,
              recipient_list=recipient_list,
              fail_silently=False)

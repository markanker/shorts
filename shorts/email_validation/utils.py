from django.core.mail import send_mail
from django.urls import reverse

from random import choices, randint
from .models import EmailVerificationModel
from utils import get_hash_ip_address
from string import ascii_letters, digits
from django.conf import settings

from exceptions import EmailVerificationError

CODE_CHARACTERS = ascii_letters + digits


def get_random_unique_code():
    code = ''.join(choices(CODE_CHARACTERS, k=randint(15, 30)))
    while EmailVerificationModel.objects.filter(code=code):
        code = ''.join(choices(CODE_CHARACTERS, k=randint(15, 30)))
    return code


def send_code(email_verif_obj: EmailVerificationModel, request):
    path = reverse('verify-email', kwargs={'verif_code': email_verif_obj.code})
    link = f"{request.scheme}://{request.get_host()}{path}"
    address = email_verif_obj.user.email
    mail_subject = "Your email verification code"
    mail_message = (f"Hello. You are receiving this mail because you are attempting to "
                    f"register on our service. If you are not, please, ignore this message."
                    f"Otherwise, just click on the following link to verify you own this "
                    f"email: \n{link}")
    send_mail(
        subject=mail_subject,
        message=mail_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[address],
        fail_silently=True,
    )
    email_verif_obj.sent_mail_to_user_counter += 1
    email_verif_obj.save()


def verify_email(user, request):
    email_verif_obj = EmailVerificationModel.objects.create(
        user=user,
        code=get_random_unique_code(),
        hash_ip_address=get_hash_ip_address(request),
    )
    send_code(email_verif_obj, request=request)


def send_again(request):
    try:
        email_verif_obj = EmailVerificationModel.objects.get(
            is_verified=False,
            hash_ip_address=get_hash_ip_address(request),
        )
    except EmailVerificationModel.DoesNotExist:
        raise EmailVerificationError("You cannot send code again")

    email_verif_obj.code = get_random_unique_code()
    email_verif_obj.save()

    send_code(email_verif_obj, request)

from celery import shared_task

from django.core.mail import send_mail
@shared_task
def add(x, y):
    print(f"args: {x}, {y}")
    raise ValueError("TEST ERROR")
    return x + y

@shared_task
def send_otp(email, code):
    send_mail(
        "Subject here",
        "Here is there message",
        "from@example.com",
        [email],
        fail_silently=False

    )
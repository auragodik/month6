from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime

@shared_task
def add(x, y):
    print(f"args: {x}, {y}")
    raise ValueError("TEST ERROR")
    return x + y

@shared_task
def send_otp(email, code):
    send_mail(
        "Subject here",
        f"Your OTP code is {code}",
        "from@example.com",
        [email],
        fail_silently=False
    )

@shared_task
def save_text_to_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: {text}\n")
    return f"Text saved to {filename}"

@shared_task
def delete_old_files(file_list):
    deleted_files = []
    for file_path in file_list:
        try:
            import os
            os.remove(file_path)
            deleted_files.append(file_path)
        except FileNotFoundError:
            continue
    return f"Deleted files: {deleted_files}"

@shared_task
def send_welcome_email(email):
    subject = "Добро пожаловать!"
    message = "Спасибо за регистрацию на нашем сайте."
    send_mail(subject, message, 'no-reply@example.com', [email])
    return f"Email sent to {email}"

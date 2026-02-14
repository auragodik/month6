from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from common.validators import phone_validator
from users.managers import CustomUserManagers


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=13, validators=[phone_validator], blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    registration_source = models.CharField(max_length=20,choices=[('local','Local'),('google','Google'),('facebook','Facebook')], default='local')
    birthdate = models.DateField(null=True, blank=True)


    objects = CustomUserManagers()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
    def _str_(self):
        return self.email

    
    def clean(self):
        super().clean()
        if self.is_superuser and not self.phone_number:
            raise ValidationError({
                'phone_number': 'Номер телефона (Кыргызстан) обязателен для суперпользователя.'
            })
    
    

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)



class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

   
   
    def _str_(self):
        return f"Код подтверждения для {self.user.email}"
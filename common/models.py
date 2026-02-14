from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now) # auto_now_add=True
    
    class Meta:
        abstract = True
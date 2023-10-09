from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE={'blank':True,'null':True}

class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True,verbose_name='почта')

    phone=models.CharField(max_length=150,**NULLABLE,verbose_name='Телефон')
    avatar=models.ImageField(upload_to='users/',**NULLABLE,verbose_name='Аватар')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    verification_token = models.CharField(max_length=15, verbose_name='Код верификации', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Статус верификации')

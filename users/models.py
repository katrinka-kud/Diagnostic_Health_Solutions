from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='E-mail')

    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    middle_name = models.CharField(max_length=100, verbose_name='отчество', **NULLABLE)
    birthday = models.DateField(verbose_name='дата рождения')
    phone = models.CharField(unique=True, max_length=35, verbose_name='номер телефона')

    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        birthday_formatted = self.birthday.strftime('%d.%m.%Y')
        return f'{self.last_name} {self.first_name} {self.middle_name}, дата рождения: {birthday_formatted}'

    class Meta:
        verbose_name = 'пациент'
        verbose_name_plural = 'пациенты'

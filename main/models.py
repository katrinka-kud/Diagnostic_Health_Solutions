from django.db import models
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Specializations(models.Model):
    title = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'специализации'


class Doctors(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    middle_name = models.CharField(max_length=100, verbose_name='отчество', **NULLABLE)
    avatar = models.ImageField(upload_to='doctors/', verbose_name='фото', **NULLABLE)
    specialty = models.ManyToManyField('Specializations', verbose_name='специализация')
    experience_years = models.PositiveIntegerField(verbose_name='опыт работы (лет)', default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='рейтинг', default=0.0)
    phone_number = models.CharField(max_length=15, verbose_name='номер телефона', **NULLABLE)
    email = models.EmailField(verbose_name='электронная почта', **NULLABLE)

    def __str__(self):
        return f'{self.last_name} {self.first_name}, Специализация: {self.specialty}, Рейтинг: {self.rating}, Опыт работы: {self.experience_years} лет'

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'врачи'


class Services(models.Model):
    title = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='стоимость')
    doctor = models.ManyToManyField('Doctors', verbose_name='врач')
    specialty = models.ForeignKey(Specializations, on_delete=models.CASCADE, verbose_name='специализация')

    def __str__(self):
        return f'{self.title} - {self.price}'

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'


class Reviews(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='имя пользователя')
    review_text = models.TextField(verbose_name='текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def str(self):
        return f'Отзыв {self.review_text} от {self.user_name}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-created_at',)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, verbose_name='врач')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пациент')
    services = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='выбранная услуга')
    appointment_date = models.DateTimeField(verbose_name='дата и время записи')

    def __str__(self):
        return f'Запись на прием: {self.patient} к {self.doctor} на {self.appointment_date}'

    class Meta:
        verbose_name = 'запись на прием'
        verbose_name_plural = 'записи на прием'
        ordering = ('appointment_date',)

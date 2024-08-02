from django.contrib import admin

from main.models import Specializations, Doctors, Services, Reviews, Appointment


@admin.register(Specializations)
class SpecializationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    list_filter = ('specialty',)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'review_text')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'services', 'appointment_date')
    list_filter = ('services', 'appointment_date')

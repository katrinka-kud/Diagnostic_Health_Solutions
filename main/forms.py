from django.forms import ModelForm

from main.models import Appointment


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('services', 'appointment_date')

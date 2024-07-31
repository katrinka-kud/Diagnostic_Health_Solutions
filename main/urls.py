from django.urls import path

from main.apps import MainConfig
from main.views import HomeView, DoctorsListView, DoctorsDetailView, AppointmentCreateView, ServicesListView, \
    ReviewsListView, ReviewsCreateView, ReviewsDeleteView, MedicalDiagView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('medical_company/', MedicalDiagView.as_view(), name='medical_company'),
    path('doctors_list/', DoctorsListView.as_view(), name='doctors_list'),
    path('doctors_detail/<int:pk>/', DoctorsDetailView.as_view(), name='doctors_detail'),
    path('services_list/', ServicesListView.as_view(), name='services_list'),
    path('reviews_list/', ReviewsListView.as_view(), name='reviews_list'),
    path('reviews_create/', ReviewsCreateView.as_view(), name='reviews_create'),
    path('reviews_delete/<int:pk>/', ReviewsDeleteView.as_view(), name='reviews_delete'),
    path('create/appointment/<int:pk>/', AppointmentCreateView.as_view(), name='appointment_create'),
]

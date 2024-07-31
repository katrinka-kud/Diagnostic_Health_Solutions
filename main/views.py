from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

from blog.models import Blog
from main.forms import AppointmentForm
from main.models import Doctors, Appointment, Services, Reviews


class MedicalDiagView(TemplateView):
    template_name = 'main/medical_company.html'


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        random_blogs = Blog.objects.order_by('?')[:3]
        blog_article_title = [blog.title for blog in random_blogs]
        blog_article_pk = [blog.pk for blog in random_blogs]
        context_data['articles'] = dict(zip(blog_article_title, blog_article_pk))

        return context_data


class DoctorsListView(ListView):
    model = Doctors


class DoctorsDetailView(DetailView):
    model = Doctors


class ServicesListView(ListView):
    model = Services


class ReviewsListView(ListView):
    model = Reviews


class ReviewsCreateView(CreateView):
    model = Reviews
    fields = ('review_text',)
    success_url = reverse_lazy('main:reviews_list')

    def form_valid(self, form):
        form.instance.user_name = self.request.user.first_name
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ReviewsDeleteView(DeleteView):
    model = Reviews
    success_url = reverse_lazy('main:reviews_list')


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        services = get_object_or_404(Services, pk=self.kwargs['pk'])
        context_data['services'] = services
        return context_data

    def form_valid(self, form):
        # print(self.request.POST)
        form.instance.patient = self.request.user
        # form.instance.services = self.get_service()
        # print(f'Услуга: {form.instance.services}')
        return super().form_valid(form)

    # def get_service(self):
    #     service = self.request.POST.get('service')
    #     return Services.objects.get(pk=service)

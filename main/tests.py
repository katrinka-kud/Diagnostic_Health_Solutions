from datetime import date

from django.test import TestCase, SimpleTestCase
from django.urls import reverse

from blog.models import Blog
from main.models import Doctors, Services
from main.templatetags.my_tags import media_filter
from users.models import User


class TestMain(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
            last_name='Test',
            first_name='Test',
            password='123asd',
            birthday=date(2000, 1, 1),
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

    def test_user_creation(self):
        """Проверяем, что пользователь создан корректно"""
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertTrue(self.user.check_password('123asd'))
        self.assertEqual(self.user.last_name, 'Test')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.birthday, date(2000, 1, 1))
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_user_login(self):
        """Проверяем, что пользователь может войти в систему"""
        response = self.client.post(reverse('login'), {
            'email': 'test@test.com',
            'password': '123asd'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_access_admin(self):
        """Проверяем, что пользователь с правами администратора может получить доступ к админке"""
        self.client.login(email='test@test.com', password='123asd')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        """Проверяем, что пользователь может выйти из системы"""
        self.client.login(email='test@test.com', password='123asd')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после выхода


class HomeViewTests(TestCase):
    """Тесты для представления главной страницы"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.com',
                                             last_name='Test',
                                             first_name='Test',
                                             password='123asd',
                                             birthday=date(2000, 1, 1), )
        Blog.objects.create(title='Blog 1')
        Blog.objects.create(title='Blog 2')
        Blog.objects.create(title='Blog 3')

    def test_home_view_status_code(self):
        """Проверяем, что статус код главной страницы равен 200"""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Проверяем, что при загрузке главной страницы используется правильный шаблон"""
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_home_view_context(self):
        """Проверяем, что контекст главной страницы содержит список статей"""
        response = self.client.get(reverse('main:home'))
        self.assertIn('articles', response.context)


class DoctorsListViewTests(TestCase):
    """Тесты для представления списка врачей"""

    def setUp(self):
        self.doctor = Doctors.objects.create(name='Dr. Smith', specialty='Cardiology')

    def test_doctors_list_view_status_code(self):
        """Проверяем, что статус код страницы списка врачей равен 200"""
        response = self.client.get(reverse('main:doctors_list'))
        self.assertEqual(response.status_code, 200)

    def test_doctors_list_view_template(self):
        """Проверяем, что при загрузке страницы списка врачей используется правильный шаблон"""
        response = self.client.get(reverse('main:doctors_list'))
        self.assertTemplateUsed(response, 'main/doctors_list.html')

    def test_doctors_list_view_context(self):
        """Проверяем, что контекст страницы списка врачей содержит специальность"""
        response = self.client.get(reverse('main:doctors_list'))
        self.assertIn('specialty', response.context)


class DoctorsDetailViewTests(TestCase):
    """Тесты для представления деталей врача"""

    def setUp(self):
        self.doctor = Doctors.objects.create(name='Dr. Smith', specialty=self.specialty)

    def test_doctor_detail_view_status_code(self):
        """Проверяем, что статус код страницы деталей врача равен 200"""
        response = self.client.get(reverse('main:doctors_detail', args=[self.doctor.pk]))
        self.assertEqual(response.status_code, 200)

    def test_doctor_detail_view_template(self):
        """Проверяем, что при загрузке страницы деталей врача используется правильный шаблон"""
        response = self.client.get(reverse('main:doctors_detail', args=[self.doctor.pk]))
        self.assertTemplateUsed(response, 'main/doctors_detail.html')


class ReviewsCreateViewTests(TestCase):
    """Тесты для представления создания отзывов"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.com',
                                             last_name='Test',
                                             first_name='Test',
                                             password='123asd',
                                             birthday=date(2000, 1, 1), )
        self.client.login(username='Test', password='123asd')

    def test_review_create_view_status_code(self):
        """Проверяем, что статус код страницы создания отзыва равен 302 (перенаправление)"""
        response = self.client.post(reverse('main:reviews_create'), {'reviews_text': 'Great service!'})
        self.assertEqual(response.status_code, 302)

    def test_review_create_view_template(self):
        """Проверяем, что при загрузке страницы создания отзыва используется правильный шаблон"""
        response = self.client.get(reverse('main:reviews_create'))
        self.assertTemplateUsed(response, 'main/reviews_form.html')


class AppointmentCreateViewTests(TestCase):
    """Тесты для представления создания записей на прием"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.com',
                                             last_name='Test',
                                             first_name='Test',
                                             password='123asd',
                                             birthday=date(2000, 1, 1), )
        self.client.login(username='Test', password='123asd')
        self.service = Services.objects.create(title='Consultation', price=1000)

    def test_appointment_create_view_status_code(self):
        """Проверяем, что статус код страницы создания записи на прием равен 302 (перенаправление)"""
        response = self.client.post(reverse('main:appointment_create', args=[self.service.pk]), {
            'date': '2023-10-01',
            'time': '10:00 AM',
            'price': 1000,
        })
        self.assertEqual(response.status_code, 302)

    def test_appointment_create_view_template(self):
        """Проверяем, что при загрузке страницы создания записи на прием используется правильный шаблон"""
        response = self.client.get(reverse('main:appointment_create', args=[self.service.pk]))
        self.assertTemplateUsed(response, 'main/appointment_form.html')


class MediaFilterTest(SimpleTestCase):

    def test_media_filter_with_value(self):
        """Проверяем, что фильтр возвращает корректный путь для заданного значения"""
        self.assertEqual(media_filter('image.jpg'), '/media/image.jpg')

    def test_media_filter_with_empty_value(self):
        """Проверяем, что фильтр возвращает '#' для пустого значения"""
        self.assertEqual(media_filter(''), '#')

    def test_media_filter_with_none_value(self):
        """Проверяем, что фильтр возвращает '#' для значения None"""
        self.assertEqual(media_filter(None), '#')

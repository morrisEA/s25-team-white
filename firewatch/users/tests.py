from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from armory.models import ServiceMember, Command, Location


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.location = Location.objects.create(city="Norfolk", state="VA", zip_code=23503)
        self.command = Command.objects.create(
            name="Alpha Command",
            service_branch="Navy",
            total_service_members=100,
            commanding_officer="John Smith",
            location_id=self.location
        )

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.servicemember = ServiceMember.objects.create(
            user=self.user,
            first="Jane",
            last="Doe",
            rate="IT",
            rank="2nd",
            end_of_service_date="2030-01-01",
            command_id=self.command
        )

    def test_index_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('users:index'))
        self.assertRedirects(response, reverse('users:login'))

    def test_index_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/dashboard.html')
        
        self.assertContains(response, str(self.servicemember))
        self.assertContains(response, self.command.name)

    def test_login_view_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('users:index'))

    def test_login_view_post_fail(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        self.assertContains(response, "Invalid credentials.")
        
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('users:login'))

        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(f"{self.user.username} has logged out." in str(m) for m in messages))

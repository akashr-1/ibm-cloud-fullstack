from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CarDealer
from .restapis import get_dealers_from_cf

class DjangoAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.dealer = CarDealer.objects.create(name='Test Dealer', short_name='testdealer')

    def test_about_view(self):
        response = self.client.get(reverse('djangoapp:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Us")

    def test_contact_view(self):
        response = self.client.get(reverse('djangoapp:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")

    def test_registration_view(self):
        response = self.client.get(reverse('djangoapp:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registration")

    def test_login_view(self):
        response = self.client.get(reverse('djangoapp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_index_view(self):
        response = self.client.get(reverse('djangoapp:index'))
        self.assertEqual(response.status_code, 200)

    def test_get_dealerships(self):
        response = self.client.get(reverse('djangoapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dealer.short_name)

    def test_invalid_dealer_details(self):
        response = self.client.get(reverse('djangoapp:dealer_details', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_add_review_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('djangoapp:add_review', args=[self.dealer.id]))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('djangoapp:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def tearDown(self):
        self.user.delete()
        self.dealer.delete()


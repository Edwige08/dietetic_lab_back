from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dietetics.models import Users, Foodbases, Foods
from rest_framework_simplejwt.tokens import RefreshToken

class AuthEndpointsTests(APITestCase):
    def setUp(self):  # Create a test user
        self.user_data = {
            'mail': 'test@example.com',
            'password': 'TestPassword123!',
            'firstname': 'Test',
            'lastname': 'User',
            'gender': 'h'
        }
        self.user = Users.objects.create_user(**self.user_data)
        
    def test_register_user(self):  # User creation: success
        url = reverse('register')
        data = {
            'mail': 'newuser@example.com',
            'password': 'NewPassword123!',
            'firstname': 'New',
            'lastname': 'User',
            'gender': 'h'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(mail='newuser@example.com').exists())

    def test_login_user(self):  # User login: success
        url = reverse('token_obtain_pair')
        data = {
            'mail': self.user_data['mail'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_user_without_password(self):  # ❌ User creation: missing password
        url = reverse('register')
        data = {
            'mail': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User',
            'gender': 'h'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_user_without_mail(self):  # ❌ User creation: missing email
        url = reverse('register')
        data = {
            'password': 'TestPassword123!',
            'firstname': 'New',
            'lastname': 'User',
            'gender': 'h'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mail', response.data)

    def test_register_user_with_invalid_mail(self):  # ❌ User creation: invalid email
        url = reverse('register')
        data = {
            'mail': 'invalid-email',
            'password': 'TestPassword123!',
            'firstname': 'New',
            'lastname': 'User',
            'gender': 'h'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mail', response.data)

    def test_register_user_with_duplicate_mail(self):  # ❌ User creation: email already used
        url = reverse('register')
        data = {
            'mail': self.user_data['mail'],  # Use the mail already used in setUp
            'password': 'TestPassword123!',
            'firstname': 'New',
            'lastname': 'User',
            'gender': 'h'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mail', response.data)

    def test_login_with_wrong_password(self):  # ❌ User login: wrong password
        url = reverse('token_obtain_pair')
        data = {
            'mail': self.user_data['mail'],
            'password': 'WrongPassword123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_nonexistent_user(self):  # ❌ User login: wrong email
        url = reverse('token_obtain_pair')
        data = {
            'mail': 'nonexistent@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ResourceEndpointsTests(APITestCase):
    def setUp(self):  # Create a test user and login
        self.user = Users.objects.create_user(
            mail='test@example.com',
            password='TestPassword123!',
            firstname='Test',
            lastname='User',
            gender='h'
        )
        
        # Authenticate user for testing
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create test data
        self.personal_db = Foodbases.objects.create(
            user=self.user,
            title="Base de données de test"
        )
        
        self.food = Foods.objects.create(
            alim_nom_fr='Test Food',
            energie_reg_ue_kcal=100,
            proteines=10,
            lipides=5,
            glucides=15,
            personal_db=self.personal_db
        )

    def test_get_personal_database(self):
        url = '/api/v1/personal-databases/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_foods(self):
        url = reverse('foods-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_access_without_token(self):  # ❌ Access without authentication token
        # Remove authentication token
        self.client.credentials()
        
        # Try to access to the personal database
        url = '/api/v1/personal-databases/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_personal_database(self):  # ❌ Create personal database: missing title
        url = '/api/v1/personal-databases/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_invalid_food(self):  # ❌ Create food: invalid data
        url = reverse('foods-list')
        data = {
            'alim_nom_fr': '',  # Empty name
            'energie_reg_ue_kcal': -100,  # Negative value
            'proteines': 'invalid',  # Non-numeric value
            'personal_db': self.personal_db.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
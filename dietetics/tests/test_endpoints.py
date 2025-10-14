from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dietetics.models import Users, PersonnalDatabases, Foods, Meals, Commentaries
from rest_framework_simplejwt.tokens import RefreshToken

class AuthEndpointsTests(APITestCase):
    def setUp(self):  # Créer un utilisateur de test
        self.user_data = {
            'mail': 'test@example.com',
            'password': 'testpassword123',
            'firstname': 'Test',
            'lastname': 'User',
            'gender': 'h'
        }
        self.user = Users.objects.create_user(**self.user_data)
        
    def test_register_user(self):
        url = reverse('register')
        data = {
            'mail': 'newuser@example.com',
            'password': 'newpassword123',
            'firstname': 'New',
            'lastname': 'User',
            'gender': 'h'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(mail='newuser@example.com').exists())

    def test_login_user(self):
        url = reverse('token_obtain_pair')
        data = {
            'mail': self.user_data['mail'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class ResourceEndpointsTests(APITestCase):
    def setUp(self):
        # Créer un utilisateur de test et le connecter
        self.user = Users.objects.create_user(
            mail='test@example.com',
            password='testpassword123',
            firstname='Test',
            lastname='User',
            gender='h'
        )
        
        # Authentifier l'utilisateur pour les tests
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Créer des données de test
        self.personal_db = PersonnalDatabases.objects.create(
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
        url = reverse('personnaldatabases-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_foods(self):
        url = reverse('foods-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
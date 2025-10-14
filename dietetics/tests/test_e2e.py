from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class PersonalDatabaseE2ETest(APITestCase):
    def test_complete_personal_database_flow(self):
        # 1. new user registration
        register_url = reverse('register')
        user_data = {
            'mail': 'newuser@example.com',
            'password': 'newpassword123',
            'firstname': 'John',
            'lastname': 'Doe',
            'gender': 'h'
        }
        response = self.client.post(register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. login to get the token
        login_url = reverse('token_obtain_pair')
        login_data = {
            'mail': user_data['mail'],
            'password': user_data['password']
        }
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # token configuration for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        
        # 3. creating a personal database
        personal_db_url = reverse('personnaldatabases-list')
        personal_db_data = {
            'title': 'Ma base de données personnelle'
        }
        response = self.client.post(personal_db_url, personal_db_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        personal_db_id = response.data['id']
        
        # 4. adding food to the personal database
        foods_url = reverse('foods-list')
        food_data = {
            'alim_nom_fr': 'Pomme',
            'energie_reg_ue_kcal': 52,
            'proteines': 0.3,
            'lipides': 0.2,
            'glucides': 14,
            'personal_db': personal_db_id
        }
        response = self.client.post(foods_url, food_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 5. personal database check
        response = self.client.get(f"{personal_db_url}{personal_db_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], personal_db_data['title'])
        
        # 5.2 foods check
        response = self.client.get(foods_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        
        foods = response.data
        if isinstance(foods, dict) and 'results' in foods:
            foods = foods['results']
            
        found_food = False
        for food in foods:
            if food['alim_nom_fr'] == food_data['alim_nom_fr']:
                found_food = True
                self.assertEqual(food['energie_reg_ue_kcal'], food_data['energie_reg_ue_kcal'])
                self.assertEqual(food['proteines'], food_data['proteines'])
                self.assertEqual(food['lipides'], food_data['lipides'])
                self.assertEqual(food['glucides'], food_data['glucides'])
                break
                
        self.assertTrue(found_food, "L'aliment ajouté n'a pas été trouvé dans la liste")
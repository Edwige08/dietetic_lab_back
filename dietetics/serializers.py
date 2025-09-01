from rest_framework import serializers
from .models import Users, PersonnalDatabases, Foods, Meals, FoodForMeals, Commentaries
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'mail'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplace username par mail
        del self.fields['username']
        self.fields['mail'] = serializers.EmailField()

class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Users
        fields = ['id', 'firstname', 'lastname', 'gender', 'mail', 'is_dietetician', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PersonnalDatabasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonnalDatabases
        fields = ['id', 'title', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']

class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ['id', 'title', 'calories_kcal', 'proteins', 'fats', 'carbohydrates', 
                 'sugars', 'fibers', 'ags', 'agmi', 'agpi', 'cholesterol', 'alcohol',
                 'sodium', 'potassium', 'phosphorus', 'iron', 'calcium', 'vitamin_d', 'personal_db']

class FoodForMealsSerializer(serializers.ModelSerializer):
    food_title = serializers.CharField(source='food.title', read_only=True)
    
    class Meta:
        model = FoodForMeals
        fields = ['id', 'quantity', 'food', 'food_title', 'meal']

class MealsSerializer(serializers.ModelSerializer):
    food_items = FoodForMealsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meals
        fields = ['id', 'title', 'user', 'food_items']

class CommentariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaries
        fields = ['id', 'description', 'user', 'is_visible', 'created_at']
        read_only_fields = ['id', 'created_at']
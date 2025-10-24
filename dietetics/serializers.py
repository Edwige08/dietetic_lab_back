from rest_framework import serializers
from .models import Users, PersonnalDatabases, Foods, Commentaries, ImcHistories, DejHistories, UndernutritionAdultHistories, UndernutritionSeniorHistories
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

class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ['id', 'alim_nom_fr', 'energie_reg_ue_kcal', 'proteines', 'lipides', 'glucides', 
                 'sucres', 'fibres', 'ags', 'agmi', 'agpi', 'cholesterol', 'alcool',
                 'sodium', 'potassium', 'phosphore', 'fer', 'calcium', 'vitamine_d', 'personal_db']

class PersonnalDatabasesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonnalDatabases
        fields = ['title']

class PersonnalDatabasesSerializer(serializers.ModelSerializer):
    foods = FoodsSerializer(many = True, read_only=True)

    class Meta:
        model = PersonnalDatabases
        # fields = ['id', 'title', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
        exclude = ['user']

class CommentariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaries
        # fields = ['id', 'description', 'user', 'is_visible', 'created_at']
        read_only_fields = ['id', 'created_at']
        exclude = ['user']

class ImcHistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImcHistories
        fields = ['weight', 'height', 'created_at']

class DejHistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DejHistories
        fields = ['weight', 'height', 'age', 'nap', 'gender', 'created_at']

class UndernutritionAdultHistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UndernutritionAdultHistories
        fields = ['weight', 'height', 'previous_weight', 'previous_weight_date', 'albuminemia', 'sarcopenia', 'etiological_food_intakes', 'etiological_absorption', 'etiological_agression', 'created_at']

class UndernutritionSeniorHistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UndernutritionSeniorHistories
        fields = ['weight', 'height', 'previous_weight', 'previous_weight_date', 'albuminemia', 'sarcopenia', 'etiological_food_intakes', 'etiological_absorption', 'etiological_agression', 'created_at']
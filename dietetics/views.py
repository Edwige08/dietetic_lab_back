from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import Users, PersonnalDatabases, Foods, Meals, FoodForMeals, Commentaries
from .serializers import (
    UsersSerializer, PersonnalDatabasesSerializer, FoodsSerializer, 
    MealsSerializer, FoodForMealsSerializer, CommentariesSerializer, CustomTokenObtainPairSerializer
)

class CustomLoginView(APIView):
    """
    Vue de connexion personnalisée utilisant l'email
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        mail = request.data.get('mail')
        password = request.data.get('password')
        
        if not mail or not password:
            return Response(
                {'error': 'Email et mot de passe requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = Users.objects.get(mail=mail)
            if user.check_password(password):
                if not user.is_active:
                    return Response(
                        {'error': 'Compte désactivé'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Génère les tokens JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'mail': user.mail,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'is_dietetician': user.is_dietetician
                    }
                })
            else:
                return Response(
                    {'error': 'Email ou mot de passe incorrect'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except Users.DoesNotExist:
            return Response(
                {'error': 'Email ou mot de passe incorrect'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Un utilisateur ne peut voir que son propre profil (sauf admin)
        if self.request.user.is_superuser:
            return Users.objects.all()
        return Users.objects.filter(id=self.request.user.id)

class PersonnalDatabasesViewSet(viewsets.ModelViewSet):
    queryset = PersonnalDatabases.objects.all()
    serializer_class = PersonnalDatabasesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Un utilisateur ne voit que ses propres bases
        return PersonnalDatabases.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Associe automatiquement la base à l'utilisateur connecté
        serializer.save(user=self.request.user)

class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Un utilisateur ne voit que les aliments de ses bases
        return Foods.objects.filter(personal_db__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_database(self, request):
        """
        Endpoint personnalisé : /api/v1/foods/by_database/?db_id=1
        """
        db_id = request.query_params.get('db_id')
        if db_id:
            foods = Foods.objects.filter(
                personal_db_id=db_id, 
                personal_db__user=request.user
            )
            serializer = self.get_serializer(foods, many=True)
            return Response(serializer.data)
        return Response({"error": "db_id parameter required"}, status=400)

class MealsViewSet(viewsets.ModelViewSet):
    queryset = Meals.objects.all()
    serializer_class = MealsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Un utilisateur ne voit que ses propres repas
        return Meals.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Associe automatiquement le repas à l'utilisateur connecté
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_food(self, request, pk=None):
        """
        Endpoint personnalisé pour ajouter un aliment à un repas
        POST /api/v1/meals/{id}/add_food/
        Body: {"food_id": 1, "quantity": 100}
        """
        meal = self.get_object()
        food_id = request.data.get('food_id')
        quantity = request.data.get('quantity')
        
        if not food_id or not quantity:
            return Response({"error": "food_id and quantity required"}, status=400)
        
        try:
            food = Foods.objects.get(id=food_id, personal_db__user=request.user)
            food_for_meal, created = FoodForMeals.objects.get_or_create(
                meal=meal,
                food=food,
                defaults={'quantity': quantity}
            )
            
            if not created:
                food_for_meal.quantity = quantity
                food_for_meal.save()
            
            serializer = FoodForMealsSerializer(food_for_meal)
            return Response(serializer.data)
            
        except Foods.DoesNotExist:
            return Response({"error": "Food not found"}, status=404)

class CommentariesViewSet(viewsets.ModelViewSet):
    queryset = Commentaries.objects.all()
    serializer_class = CommentariesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Commentaries.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Associe automatiquement le commentaire à l'utilisateur connecté
        serializer.save(user=self.request.user)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Utilisateur créé avec succès", 
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     serializer = UsersSerializer(data=request.data)
    #     if serializer.is_valid():
    #         validated_data = serializer.validated_data
    #         if 'password' in request.data:
    #             validated_data['password'] = make_password(request.data['password'])
            
    #         user = Users.objects.create(**validated_data)
    #         return Response(
    #             {"message": "Utilisateur créé avec succès", "user_id": user.id}, 
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
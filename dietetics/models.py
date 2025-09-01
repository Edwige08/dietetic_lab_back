from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsersManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle Users qui utilise l'email au lieu du username
    """
    def create_user(self, mail, password=None, **extra_fields):
        if not mail:
            raise ValueError('L\'adresse email est obligatoire')
        
        mail = self.normalize_email(mail)
        user = self.model(mail=mail, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, mail, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_dietetician', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        
        return self.create_user(mail, password, **extra_fields)

class Users(AbstractUser):
    username = None  # Supprime le champ username
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    mail = models.EmailField(unique=True)
    is_dietetician = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UsersManager()  # Utilise le manager personnalisé
    
    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = ['firstname', 'lastname']

class PersonnalDatabases(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='personal_databases')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Base de données personnelle"
        verbose_name_plural = "Bases de données personnelles"

class Foods(models.Model):
    title = models.CharField(max_length=255)
    calories_kcal = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    sugars = models.FloatField(default=0)
    fibers = models.FloatField(default=0)
    ags = models.FloatField(default=0)
    agmi = models.FloatField(default=0)
    agpi = models.FloatField(default=0)
    cholesterol = models.FloatField(default=0)
    alcohol = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    vitamin_d = models.FloatField(default=0)
    personal_db = models.ForeignKey(PersonnalDatabases, on_delete=models.CASCADE, 
                                   related_name='foods')

class Meals(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='meals')

class FoodForMeals(models.Model):
    quantity = models.FloatField(help_text="Quantité en grammes")
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE, related_name='food_items')

    class Meta:
        unique_together = ('food', 'meal')

class Commentaries(models.Model):
    description = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='commentaries')
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']
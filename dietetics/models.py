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

class Foodbases(models.Model):
    title = models.CharField(max_length=255)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='personal_databases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Base alimentaire personnelle"
        verbose_name_plural = "Bases alimentaires personnelles"
        ordering = ['-created_at']

class Foods(models.Model):
    alim_nom_fr = models.CharField(max_length=255)
    energie_reg_ue_kcal = models.FloatField(default=0)
    proteines = models.FloatField(default=0)
    lipides = models.FloatField(default=0)
    glucides = models.FloatField(default=0)
    sucres = models.FloatField(default=0)
    fibres = models.FloatField(default=0)
    ags = models.FloatField(default=0)
    agmi = models.FloatField(default=0)
    agpi = models.FloatField(default=0)
    cholesterol = models.FloatField(default=0)
    alcool = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    phosphore = models.FloatField(default=0)
    fer = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    vitamine_d = models.FloatField(default=0)
    personal_db = models.ForeignKey(Foodbases, on_delete=models.CASCADE, 
                                   related_name='foods')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Aliment"
        verbose_name_plural = "Aliments"

class Comments(models.Model):
    description = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comments')
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']

class ImcHistories(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class DejHistories(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    age = models.FloatField()
    nap = models.FloatField()
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class UndernutritionAdultHistories(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    previous_weight = models.FloatField()
    previous_weight_date = models.CharField(max_length=24)
    albuminemia = models.FloatField()
    sarcopenia = models.BooleanField(default=False)
    etiological_food_intakes = models.BooleanField(default=False)
    etiological_absorption = models.BooleanField(default=False)
    etiological_agression = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class UndernutritionSeniorHistories(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    previous_weight = models.FloatField()
    previous_weight_date = models.CharField(max_length=24)
    albuminemia = models.FloatField()
    sarcopenia = models.BooleanField(default=False)
    etiological_food_intakes = models.BooleanField(default=False)
    etiological_absorption = models.BooleanField(default=False)
    etiological_agression = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class SriHistories(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    previous_weight = models.FloatField()
    low_ingesta_five_days = models.BooleanField(default=False)
    low_ingesta_ten_days = models.BooleanField(default=False)
    potassium = models.FloatField()
    phosphorus = models.FloatField()
    magnesium = models.FloatField()
    atcd = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
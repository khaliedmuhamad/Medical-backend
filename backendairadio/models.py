from django.db import models
import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.conf import settings


class Case (models.Model):
    sex_male = 'M'
    sex_female = 'W'
    sex_divers = 'D'
    casename = models.CharField(max_length=5, unique= True)
    verdacht_diagnose = models.CharField(max_length=255)
    körper_teil = models.CharField(max_length=255)

    sex_select = [
        (sex_male,'Männlich'),
        (sex_female,'Weiblich'),
        (sex_divers,'Divers')
    ]
    sex = models.CharField(max_length=1, choices=sex_select)

    def save(self, *args, **kwargs):
        if not self.casename:
            self.casename = self.generate_casename()
        super().save(*args, **kwargs)

    def generate_casename(self):
        letter = random.choice(string.ascii_uppercase)
        numbers = ''.join(random.choices(string.digits, k=3))
        return f'{letter}{numbers}'

    def __str__(self):
        return self.casename

    

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    institiut = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'institiut']

    def __str__(self):
        return self.username

class RadioInfo (models.Model):
        
    POS_CHOICES = [
    ('anterior', 'anterior'),
    ('posterior', 'posterior'),
    ('superior', 'superior'),
    ('inferior', 'inferior '),
    ('dexter', 'dexter '),
    ('sinister', 'sinister ')
]
 
    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    position = models.CharField(max_length= 25, choices=POS_CHOICES)
    size =models.DecimalField(max_digits=5, decimal_places=2)

class RadioImage(models.Model):
    radio_Info = models.OneToOneField(RadioInfo, on_delete=models.CASCADE)
    image = models.FileField(upload_to= 'images/')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


    
class Docker (models.Model):
    description = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=100)
    docker_ip = models.CharField(max_length=100)
    docker_port = models.CharField(max_length=100)

    
class AnalysisResult (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    docker = models.ForeignKey(Docker, on_delete=models.CASCADE)
    radioInfo = models.OneToOneField(RadioInfo,on_delete=models.CASCADE)
    result = models.CharField(max_length= 255)
    date_analysis = models.DateField(auto_now_add=True)
    time_analysis = models.TimeField(auto_now_add=True)

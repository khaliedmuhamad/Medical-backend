from rest_framework import serializers
from .models import *
from .models import MyUserManager
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import pydicom

# Serializer für die Registrierung eines neuen Benutzers
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'institiut', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            institiut=validated_data['institiut'],
            password=validated_data['password']
        )
        return user

# Serializer für das Erstellen eines JWT-Tokens
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        User = get_user_model()
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise InvalidToken({'detail': 'Kein aktives Konto mit den angegebenen Anmeldedaten gefunden'})

        if not user.is_active:
            raise InvalidToken({'detail': 'Benutzerkonto ist nicht aktiv'})

        data = super().validate(attrs)
        data['username'] = user.username  # Benutzername zur Antwort hinzufügen
        data['is_staff'] = user.is_staff  # is_staff zur Antwort hinzufügen
        return data

# Serializer für die Benutzeranmeldung
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# Serializer für die Benutzerprofilaktualisierung
class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'institiut']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.institiut = validated_data.get('institiut', instance.institiut)

        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and request.method == 'GET':
            ret.pop('password', None)
        
        return ret

# Serializer für Fallinformationen
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'casename', 'sex', 'verdacht_diagnose', 'körper_teil']
        read_only_fields = ['casename']

# Serializer für die Ergebnisdarstellung eines Falls
class CaseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['casename']

# Serializer für Radiologieinformationen
class RadioInfoSerializer(serializers.ModelSerializer):
    case = serializers.SlugRelatedField(queryset=Case.objects.all(), slug_field='casename')

    class Meta:
        model = RadioInfo
        fields = ['id', 'case', 'position', 'size']

# Serializer für Radiologiebilder
class RadioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioImage
        fields = ['id', 'image']
    
    def validate_image(self, value):
        if not value.name.endswith('.dcm'):
            raise ValidationError("Nur DICOM-Dateien sind erlaubt.")
        
        try:
            pydicom.dcmread(value)
        except Exception as e:
            raise ValidationError("Die Datei ist keine gültige DICOM-Datei.")
        
        return value

# Serializer für Docker-Informationen
class DockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docker
        fields = ['description', 'name', 'path', 'docker_ip', 'docker_port', 'id']

# Serializer für Analyseergebnisse
class AnalysisResultSerializer(serializers.ModelSerializer):
    radioInfo = serializers.SlugRelatedField(queryset=RadioInfo.objects.all(), slug_field='id')
    docker = serializers.PrimaryKeyRelatedField(queryset=Docker.objects.all())
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')

    class Meta:
        model = AnalysisResult
        fields = ['result', 'radioInfo', 'docker', 'user']

# Serializer für die vollständige Darstellung von Analyseergebnissen
class AnalysisResultAllSerializer(serializers.ModelSerializer):
    docker = serializers.PrimaryKeyRelatedField(queryset=Docker.objects.all())
    user = serializers.StringRelatedField()
    radioImage = serializers.SerializerMethodField()
    case = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisResult
        fields = ['id', 'result', 'date_analysis', 'docker', 'user', 'radioImage', 'case']

    def get_radioImage(self, obj):
        radio_info = obj.radioInfo
        radio_image = RadioImage.objects.filter(radio_Info=radio_info).first()
        if radio_image:
            return RadioImageSerializer(radio_image).data
        return None

    def get_case(self, obj):
        radio_info = obj.radioInfo
        case = radio_info.case
        return CaseResultSerializer(case).data if case else None

# Serializer für die Darstellung aller aktiven und inaktiven Benutzer
class AllActivAndNotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'institiut']

# Serializer für die Aktualisierung des Benutzerstatus
class UpdateUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']

from rest_framework import serializers
from .models import *
from .models import MyUserManager
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model


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

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        User = get_user_model()
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise InvalidToken({'detail': 'No active account found with the given credentials'})

        if not user.is_active:
            raise InvalidToken({'detail': 'User account is not active'})

        data = super().validate(attrs)
        data['username'] = user.username  
        data['is_staff'] = user.is_staff  
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Passwort ist nur für Schreiboperationen erforderlich

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'institiut']

    def update(self, instance, validated_data):
        # Wenn das Passwort im aktualisierten Daten vorhanden ist, setze es neu
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        
        # Update der anderen Felder
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.institiut = validated_data.get('institiut', instance.institiut)
        
        # Speichern der Änderungen am Benutzerobjekt
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        
        # Passwort nicht in GET-Anfragen anzeigen
        if request and request.method == 'GET':
            ret.pop('password', None)
        
        return ret

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id','casename','sex','verdacht_diagnose','körper_teil']
        read_only_fields = ['casename']


class CaseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['casename']
        

class RadioInfoSerializer(serializers.ModelSerializer):
    # Hier verwenden wir einen SlugRelatedField, um auf den Fallnamen zu verweisen
    case = serializers.SlugRelatedField(queryset=Case.objects.all(), slug_field='casename')

    class Meta:
        model = RadioInfo
        fields = ['id','case', 'position', 'size']

        
class RadioImageSerializer(serializers.ModelSerializer):
    #radioInfo = RadioInfoSerializer

    class Meta:
        model = RadioImage
        fields = ['id','image']





class DockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docker
        fields = ['description','name','path','docker_ip','docker_port']

class AnalysisResultSerializer(serializers.ModelSerializer):
    radioInfo = serializers.SlugRelatedField(queryset=RadioInfo.objects.all(), slug_field='id')
    docker = serializers.PrimaryKeyRelatedField(queryset=Docker.objects.all())
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')
    #user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = AnalysisResult
        fields = ['result', 'radioInfo','docker','user']



class AnalysisResultAllSerializer(serializers.ModelSerializer):
    #radioInfo = RadioInfoSerializer()
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
    
class AllActivAndNotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'institiut']

class UpdateUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']
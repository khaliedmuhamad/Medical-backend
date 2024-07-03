# The above code defines Django API views for handling cases, radio images, and radio information with
# CRUD operations.
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from .models import *
from .serializers import ( CaseSerializer, 
                          RadioImageSerializer, 
                          RadioInfoSerializer,
                           DockerSerializer, 
                          RegistrationSerializer,
                          LoginSerializer,
                            AnalysisResultSerializer,
                          AnalysisResultAllSerializer,
                           ProfileSerializer, 
                           AllActivAndNotUserSerializer, 
                           UpdateUserStatusSerializer,
                             )

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, RetrieveDestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action



class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

        
class CaseList(ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    
    
    
class CaseDetail(RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    
class RadioInfoList(ListCreateAPIView):
    serializer_class = RadioInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case_pk = self.kwargs['case_pk']
        return RadioInfo.objects.filter(case_id=case_pk)

    def perform_create(self, serializer):
        case_pk = self.kwargs['case_pk']
        serializer.save(case_id=case_pk)

class RadioInfoDetail(RetrieveUpdateDestroyAPIView):
    queryset = RadioInfo.objects.all()
    serializer_class = RadioInfoSerializer
    permission_classes = [IsAuthenticated]

class RadioImageList(ListCreateAPIView):
    serializer_class = RadioImageSerializer
    permission_classes = [IsAuthenticated]
   

    def get_queryset(self):
        radioinfo_pk = self.kwargs['radioinfo_pk']
        return RadioImage.objects.filter(radio_Info_id=radioinfo_pk)
    

    def perform_create(self, serializer):
        radioinfo_pk = self.kwargs['radioinfo_pk']
        serializer.save(radio_Info_id=radioinfo_pk)

class RadioImageDetail(RetrieveUpdateDestroyAPIView):
    queryset = RadioImage.objects.all()
    serializer_class = RadioImageSerializer
    permission_classes = [IsAuthenticated]

class ListDockerContainersView(APIView):
    def get(self, request, radioinfo_pk, pk):
        docker_containers = Docker.objects.all()
        serializer = DockerSerializer(docker_containers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendDICOMToDockerView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, radioinfo_pk, pk, docker_id):
        try:
            docker = Docker.objects.get(id=docker_id)
        except Docker.DoesNotExist:
            return Response("Der ausgewählte Docker wurde nicht gefunden", status=status.HTTP_404_NOT_FOUND)

        # Docker-URL basierend auf den Daten des ausgewählten Docker-Objekts erstellen
        docker_url = f'http://{docker.docker_ip}:{docker.docker_port}/analyze'

        try:
            radio_image = RadioImage.objects.get(pk=pk)
        except RadioImage.DoesNotExist:
            return Response("Das angeforderte Bild wurde nicht gefunden", status=status.HTTP_404_NOT_FOUND)

        dicom_image_path = radio_image.image.path  

        try:
            with open(dicom_image_path, 'rb') as dicom_file:
                files = {'dicom': dicom_file}
                response = requests.post(docker_url, files=files)

                if response.status_code == 200:
                    response_data = response.text
                    user = request.user.id

                    

                    analysis_result_data = {
                        'radioInfo': radioinfo_pk,
                        'result': response_data,
                        'docker': docker_id,
                        'user' : user,
                    }
                    print(user, "KK")
                    
                    analysis_result_serializer = AnalysisResultSerializer(data=analysis_result_data)
                    if analysis_result_serializer.is_valid():
                        analysis_result_serializer.save()
                        return Response("Das DICOM-Bild wurde erfolgreich analysiert und das Ergebnis wurde gespeichert", status=status.HTTP_200_OK)
                    else:
                        return Response("Fehler beim Speichern des Analyseergebnisses", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Fehler beim Senden des DICOM-Bildes an den Docker-Container", status=response.status_code)
        except Exception as e:
            return Response(f"Fehler beim Senden des DICOM-Bildes an den Docker-Container: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class CaseRadioInfoAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id  # Annahme: Der Benutzer ist authentifiziert und die ID kann abgerufen werden
        analysis_results = AnalysisResult.objects.filter(user_id=user_id).select_related('radioInfo__case', 'docker')
        serializer = AnalysisResultAllSerializer(analysis_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CaseRadioInfoAnalysisView_result(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id  # Annahme: Der Benutzer ist authentifiziert und die ID kann abgerufen werden
        # Das letzte Analyseergebnis des Benutzers abrufen
        analysis_result = AnalysisResult.objects.filter(user_id=user_id).select_related('radioInfo__case', 'docker').order_by('-date_analysis').first()
        
        if analysis_result:
            serializer = AnalysisResultAllSerializer(analysis_result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No analysis results found.'}, status=status.HTTP_404_NOT_FOUND)



class CaseRadioInfoAnalysisViewEdit(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultAllSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class MyProfileEdit(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class UserManagment(APIView):
    def get(self, request, *args, **kwargs):
        active_users = User.objects.filter(is_active=True)
        serializer = AllActivAndNotUserSerializer(active_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserManagmenNotActive(APIView):
    def get(self, request, *args, **kwargs):
        active_users = User.objects.filter(is_active=False)
        serializer = AllActivAndNotUserSerializer(active_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserStatusView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserStatusSerializer

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Debugging-Ausgabe: Überprüfen Sie die empfangenen Daten
        print("Empfangene Daten:", request.data)

        # Überprüfen Sie, ob 'is_active' im empfangenen Daten vorhanden ist
        if 'is_active' not in request.data:
            return Response({"detail": "Missing 'is_active' field in request data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # Debugging-Ausgabe: Überprüfen Sie die validierten Daten
            print("Validierte Daten:", serializer.validated_data)
            
            # Direkte Attributzuweisung und Speicherung
            user.is_active = serializer.validated_data.get('is_active', user.is_active)
            user.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Debugging-Ausgabe: Überprüfen Sie die Fehler
            print("Validierungsfehler:", serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
class AnalysisResultCreateView(CreateAPIView):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

'''
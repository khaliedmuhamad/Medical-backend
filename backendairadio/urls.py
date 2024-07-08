from django.urls import path
from .views import (
    CaseList, CaseDetail, RadioImageList, RadioImageDetail, 
    RadioInfoList, RadioInfoDetail, SendDICOMToDockerView, 
    ListDockerContainersView, RegisterView, MyTokenObtainPairView, 
    CaseRadioInfoAnalysisView, CaseRadioInfoAnalysisViewEdit, 
    MyProfileEdit, UserManagment, UpdateUserStatusView, 
    UserManagmenNotActive, CaseRadioInfoAnalysisView_result
)
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# URL-Konfiguration für die Django-App
urlpatterns = [
    # Authentifizierungsrouten
    path('auth/register/', RegisterView.as_view(), name='register'),  # Route für die Registrierung neuer Benutzer
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Route für die Anmeldung und Token-Erstellung
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Route für das Aktualisieren des JWT-Tokens

    # Profilverwaltung
    path('myProfile/', MyProfileEdit.as_view(), name='my-Profile'),  # Route zur Bearbeitung des eigenen Profils

    # Fallverwaltung
    path('createCase/', CaseList.as_view(), name='case-list'),  # Route zum Erstellen und Auflisten von Fällen
    path('createCase/<int:pk>/', CaseDetail.as_view(), name='case-detail'),  # Route zum Anzeigen, Bearbeiten und Löschen eines spezifischen Falls
    path('createCase/<int:case_pk>/radioinfos/', RadioInfoList.as_view(), name='case-radioinfo-list'),  # Route zum Hinzufügen und Auflisten von Radiologie-Informationen zu einem spezifischen Fall
    path('createCase/<int:case_pk>/radioinfos/<int:pk>/', RadioInfoDetail.as_view(), name='case-radioinfo-detail'),  # Route zum Anzeigen, Bearbeiten und Löschen spezifischer Radiologie-Informationen

    # Radiologie-Bilder
    path('radioinfos/<int:radioinfo_pk>/radioimages/', RadioImageList.as_view(), name='radioinfo-radioimage-list'),  # Route zum Hinzufügen und Auflisten von Radiologie-Bildern
    path('radioinfos/<int:radioinfo_pk>/radioimages/<int:pk>/', RadioImageDetail.as_view(), name='radioinfo-radioimage-detail'),  # Route zum Anzeigen, Bearbeiten und Löschen spezifischer Radiologie-Bilder
    path('radioinfos/<int:radioinfo_pk>/radioimages/<int:pk>/dockerselect/', ListDockerContainersView.as_view(), name='docker-select'),  # Route zur Auswahl eines Docker-Containers für ein Radiologie-Bild
    path('radioinfos/<int:radioinfo_pk>/radioimages/<int:pk>/dockerselect/<int:docker_id>/send_to_docker/', SendDICOMToDockerView.as_view(), name='send_dicom_to_docker'),  # Route zum Senden eines Radiologie-Bildes an einen Docker-Container

    # Historie und Analyse
    path('historie/', CaseRadioInfoAnalysisView.as_view(), name='case_radio_info_analysis'),  # Route zum Anzeigen der Fallhistorie und Analysen
    path('historie/<int:pk>/', CaseRadioInfoAnalysisViewEdit.as_view(), name='case_radio_info_analysis_Edit'),  # Route zum Bearbeiten spezifischer Analysen in der Historie
    path('result/', CaseRadioInfoAnalysisView_result.as_view(), name='case_radio_info_analysis1'),  # Route zum Anzeigen der Analyseergebnisse

    # Benutzermanagement
    path('usermanagment/', UserManagment.as_view(), name='Userverwaltung'),  # Route zur Verwaltung aller Benutzer
    path('usermanagment/<int:pk>/', UpdateUserStatusView.as_view(), name='User_delet'),  # Route zum Aktualisieren des Benutzerstatus (aktiv/inaktiv) eines spezifischen Benutzers
    path('registerRequestes/', UserManagmenNotActive.as_view(), name='Regisiterungsanfragen'),  # Route zum Anzeigen der Registrierungsanfragen nicht aktiver Benutzer
    path('registerRequestes/<int:pk>/', UpdateUserStatusView.as_view(), name='Regisiterungsanfragen'),  # Route zum Aktualisieren des Benutzerstatus bei Registrierungsanfragen
]

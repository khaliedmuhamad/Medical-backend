from django.urls import path
from .views import CaseList, CaseDetail, RadioImageList, RadioImageDetail, RadioInfoList, RadioInfoDetail, SendDICOMToDockerView, ListDockerContainersView, RegisterView, MyTokenObtainPairView, CaseRadioInfoAnalysisView, CaseRadioInfoAnalysisViewEdit, MyProfileEdit, UserManagment, UpdateUserStatusView, UserManagmenNotActive
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('myProfile/', MyProfileEdit.as_view(), name='my-Profile'),
    path('createCase/', CaseList.as_view(), name='case-list'),
    path('createCase/<int:pk>/', CaseDetail.as_view(), name='case-detail'),
    path('createCase/<int:case_pk>/radioinfos/', RadioInfoList.as_view(), name='case-radioinfo-list'),
    path('createCase/<int:case_pk>/radioinfos/<int:pk>/', RadioInfoDetail.as_view(), name='case-radioinfo-detail'),
    path('radioinfos/<int:radioinfo_pk>/radioimages/', RadioImageList.as_view(), name='radioinfo-radioimage-list'),
    path('radioinfos/<int:radioinfo_pk>/radioimages/<int:pk>/', RadioImageDetail.as_view(), name='radioinfo-radioimage-detail'),
    path('radioinfos/<int:radioinfo_pk>/radioimages/<int:pk>/dockerselect/', ListDockerContainersView.as_view(), name='docker-select'),
    path('radioinfos/<int:radioinfo_pk>/radioimages/<int:pk>/dockerselect/<int:docker_id>/send_to_docker/', SendDICOMToDockerView.as_view(), name='send_dicom_to_docker'),
    path('historie/', CaseRadioInfoAnalysisView.as_view(), name='case_radio_info_analysis'),
    path('historie/<int:pk>/', CaseRadioInfoAnalysisViewEdit.as_view(), name='case_radio_info_analysis_Edit'),
    path('usermanagment/', UserManagment.as_view(), name='Userverwaltung'),
    path('usermanagment/<int:pk>/', UpdateUserStatusView.as_view(), name='User_delet'),
    path('registerRequestes/', UserManagmenNotActive.as_view(), name='Regisiterungsanfragen'),
    path('registerRequestes/<int:pk>/', UpdateUserStatusView.as_view(), name='Regisiterungsanfragen'),

]
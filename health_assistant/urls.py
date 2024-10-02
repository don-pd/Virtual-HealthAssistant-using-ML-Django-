from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('diagnose/', views.diagnose, name='diagnose'),
    path('result/<int:patient_id>/', views.result, name='result'),
    path('patients/', views.all_patients_view, name='all_patients'),
]

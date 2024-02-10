from django.urls import path
from accountsAPI import views

from .views import Home, logout_view

from .views import (
    ownerAPIView,
    technicianAPIView,
    UserLogoutAPIView,
    index,
)

urlpatterns = [
    path('addowner/', ownerAPIView.as_view(), name="add_owner"),
    path('addtechnician/', technicianAPIView.as_view(), name="add_technician"),
    path('owner/login/', views.owner_login, name="owner_login"),
    path('owner/registration/', views.owner_registration, name="owner_registration"),
    path('owner/dashboard/', views.owner_dashboard, name="owner_dashboard"),
    path('logout/', logout_view, name='logout'),

    path('user/logout/', UserLogoutAPIView.as_view(), name="logout_user"),
    path('login/', index, name="index"),
    path('', Home, name='Home'),
    
]

from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='app-home'),
    path('dashboard/', views.dashboard, name='app-dashboard'),
    path('firms_registration_list/', views.user_firm, name='app-user-firms-list' ),
]

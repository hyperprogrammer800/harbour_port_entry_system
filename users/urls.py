from . import views
from django.urls import path

urlpatterns = [
    path('persons_list/', views.person_list, name='app-persons-list' ),
    path('person_registration/', views.person_register, name='app-person-register' ),
    path('person_registration/<person_id>', views.person_register, name='app-person-register' ),
]

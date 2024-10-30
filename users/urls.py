from . import views
from django.urls import path

urlpatterns = [
    path('persons_list/', views.person_list, name='app-persons-list' ),
    path('person_registration/', views.person_register, name='app-person-register' ),
    path('person_registration/<person_id>', views.person_register, name='app-person-register' ),

    path('permission_management', views.permission_management, name='permission-management' ),
    path('permission_management/<int:user_id>/', views.permission_management, name='permission_management_with_user'),

    path('roles_add', views.group_role_creation, name='roles-creation' ),
    path('roles_add/<int:role_id>/', views.group_role_creation, name='roles-creation' ),
    path('assign_role/', views.assign_user_role, name='assign-role' ),
]

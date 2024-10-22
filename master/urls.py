from . import views
from django.urls import path

urlpatterns = [
    path('<str:app_name>/<str:model_name>/', views.dynamic_model_list_view, name='app-dynamic-model'),
    path('<str:app_name>/<str:model_name>/add/', views.dynamic_model_register, name='app-dynamic-model-creation'),
    path('<str:app_name>/<str:model_name>/add/<int:id>/', views.dynamic_model_register, name='app-dynamic-model-creation'),
]

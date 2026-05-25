from django.urls import path
from . import views

app_name = 'api_services'

urlpatterns = [
    path('weather/', views.weather, name='weather'),
    path('recipes/', views.recipes, name='recipes'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('refresh/', views.refresh_token, name='refresh'),
    path('', views.login, name='login'),
    #path('refresh/', views.token_refresh, name='token_refresh'),
]
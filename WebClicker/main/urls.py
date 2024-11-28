from . import views
from django.urls import path


urlpatterns = [
    path('clicker/v1/', views.index, name='home'),
]

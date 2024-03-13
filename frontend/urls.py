from django.urls import path, include
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]

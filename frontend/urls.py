from django.urls import path, include
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('', views.list_detail, name='list_detail'),
]

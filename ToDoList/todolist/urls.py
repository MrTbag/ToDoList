from django.urls import path

from . import views

app_name = 'todolist'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:list_id>/', views.detail, name='detail'),
]

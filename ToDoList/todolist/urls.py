from django.urls import path

from . import views

app_name = 'todolist'

urlpatterns = [
    path('', views.index, name='index'),
    path('lists/<int:list_id>/', views.list_detail, name='list_detail'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/create/<int:list_id>/', views.task_create, name='task_create'),
    path('tasks/form/<int:list_id>/', views.task_form, name='task_form'),
]

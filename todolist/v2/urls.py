from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from todolist.v2 import views

app_name = 'todolist'

urlpatterns = [
    path('lists/', views.TodolistList.as_view(), name='todolist-list'),
    path('lists/<int:pk>/', views.TodolistDetail.as_view(), name='todolist-detail'),
    path('tasks/', views.TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    path('tasks/<int:pk>/export/', views.TaskExport.as_view(), name='task-export'),
    path('lists/<int:pk>/import/', views.TaskImport.as_view(), name='task-export'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

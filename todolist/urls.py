from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'todolist'

urlpatterns = [
    path('lists/', views.todolist_list, name='todolist_list'),
    path('lists/<int:list_id>/', views.todolist_detail, name='todolist_detail'),
    path('lists/<int:list_id>/import/', views.task_import, name='task_import'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/export/', views.task_export, name='task_export'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
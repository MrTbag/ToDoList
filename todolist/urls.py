from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'todolist'

urlpatterns = [
    path('lists/', views.todolist_list, name='todolist-list'),
    path('lists/<int:list_id>/', views.todolist_detail, name='todolist-detail'),
    path('lists/<int:list_id>/import/', views.task_import, name='task-import'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
    path('tasks/<int:task_id>/export/', views.task_export, name='task-export'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

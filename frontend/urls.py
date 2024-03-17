from django.urls import path, include
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('todolists/', views.todolist_list, name='todolist_list'),
    path('todolists/create/', views.todolist_create, name='todolist_create'),
    path('todolists/created-successfully/', views.created_successfully, name='successful'),
    path('todolists/<int:list_id>/', views.todolist_detail, name='todolist_detail'),
    path('todolists/<int:list_id>/edit', views.todolist_edit, name='todolist_edit'),
    path('todolists/<int:list_id>/import', views.task_import, name='task_import'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/export', views.task_export, name='task_export'),
    path('shorten/', views.url_shortener, name='url_shortener'),
]

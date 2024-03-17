from django.urls import path, include
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('todolists/', views.IndexView.as_view(), name='index'),
    path('todolists/create/', views.list_create, name='list_create'),
    path('todolists/created-successfully/', views.created_successfully, name='successful'),
    path('todolists/<int:list_id>/', views.list_detail, name='list_detail'),
    path('todolists/<int:list_id>/edit', views.list_edit, name='list_edit'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit', views.task_edit, name='task_edit'),
]

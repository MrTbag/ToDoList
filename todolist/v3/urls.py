from rest_framework.routers import DefaultRouter

from todolist.v3.views import TodolistViewSet, TaskViewSet

app_name = 'todolist'

router = DefaultRouter()

router.register(r'todo_lists', TodolistViewSet, basename='todolist')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls

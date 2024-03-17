from django.shortcuts import render

from frontend.forms import TaskForm


def task_create(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, "frontend/task_form_create.html", {"form": form})

    return render(request, 'frontend/wrong_method.html')

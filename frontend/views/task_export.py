from django.shortcuts import render, get_object_or_404

from todolist.models import Task


def task_export(request, task_id=None):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'frontend/task_export.html', {'task': task})

    return render(request, 'frontend/wrong_method.html')

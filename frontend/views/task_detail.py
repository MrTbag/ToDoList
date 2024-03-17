from django.shortcuts import render, get_object_or_404

from todolist.models import Task


def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'frontend/task_detail.html', {'task': task})

    return render(request, 'frontend/wrong_method.html')

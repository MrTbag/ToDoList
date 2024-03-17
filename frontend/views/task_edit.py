from django.shortcuts import render, get_object_or_404

from todolist.models import Task
from frontend.forms import TaskForm


def task_edit(request, task_id):
    if request.method == 'GET':
        prev_task = get_object_or_404(Task, id=task_id)
        form = TaskForm({'name': prev_task.name, 'deadline': prev_task.deadline, 'importance': prev_task.importance,
                         'file': prev_task.file, 'image': prev_task.image, 'done': prev_task.done})
        return render(request, 'frontend/task_form_edit.html', {"form": form, "task_id": task_id})

    return render(request, 'frontend/wrong_method.html')

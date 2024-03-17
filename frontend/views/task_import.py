from django.shortcuts import render

from frontend.forms import TaskImportForm


def task_import(request, list_id):
    if request.method == 'GET':
        form = TaskImportForm()
        return render(request, 'frontend/task_import.html', {'list_id': list_id, 'form': form})

    return render(request, 'frontend/wrong_method.html')

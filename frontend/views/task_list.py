from django.shortcuts import render


def task_list(request):
    if request.method == 'GET':
        return render(request, 'frontend/task_list.html')

    return render(request, 'frontend/wrong_method.html')

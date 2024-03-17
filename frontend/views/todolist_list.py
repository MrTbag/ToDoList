from django.shortcuts import render
from django.views.generic import View

from todolist.models import CustomUser


def todolist_list(request):
    if request.method == 'GET':
        user: CustomUser = request.user
        lists = user.todolist_set.all()
        context = {
            'lists': lists,
            'user': request.user.username
        }
        return render(request, 'frontend/todolist_list.html', context)

    return render(request, 'frontend/wrong_method.html')

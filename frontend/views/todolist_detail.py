from django.shortcuts import render, get_object_or_404

from todolist.models import CustomUser, TodoList


def todolist_detail(request, list_id):
    if request.method == 'GET':
        current_list = get_object_or_404(TodoList, id=list_id)
        user: CustomUser = request.user
        if user.todolist_set.contains(current_list):
            return render(request, 'frontend/todolist_detail.html', {'list': current_list})
        else:
            return render(request, 'frontend/access_denied.html')

    return render(request, 'frontend/wrong_method.html')

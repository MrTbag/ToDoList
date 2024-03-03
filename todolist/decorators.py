from .models import CustomUser
from django.shortcuts import render
from functools import wraps


def authorize(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        user: CustomUser = request.user
        if user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'todolist/error_login.html')

    return inner

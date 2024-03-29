from django.shortcuts import render
from django.http import HttpRequest


def authenticate(get_response):
    def middleware(request):
        request: HttpRequest = request
        if request.get_full_path().startswith('/todolist/'):
            if request.user.is_authenticated:
                response = get_response(request)
                return response
            else:
                return render(request, 'todolist/error_login.html')

        return get_response(request)

    return middleware

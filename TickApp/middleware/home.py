from django.shortcuts import redirect
from django.http import HttpRequest


def home(get_response):
    def middleware(request):
        request: HttpRequest = request
        if request.get_full_path() == '/':
            if request.user.is_authenticated:
                return redirect('frontend:index')

        return get_response(request)

    return middleware

from django.shortcuts import render


def index(request):
    if request.method == "GET":
        return render(request, 'frontend/index.html')

    return render(request, 'frontend/wrong_method.html')

from django.shortcuts import render


def created_successfully(request):
    if request.method == 'GET':
        return render(request, 'frontend/create_successful.html')

    return render(request, 'frontend/wrong_method.html')

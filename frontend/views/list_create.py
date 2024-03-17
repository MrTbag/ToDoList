from django.shortcuts import render

from frontend.forms import TodolistForm


def list_create(request):
    if request.method == 'GET':
        form = TodolistForm
        return render(request, "frontend/list_form_create.html", {"form": form})

    return render(request, 'frontend/wrong_method.html')

from unittest import loader

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic
from .models import List


# Create your views here.

def index(request):
    lists = List.objects.all()
    context = {
        'lists': lists,
    }
    return render(request, 'todolist/index.html', context)


def detail(request, list_id):
    name = List.objects.get(id=list_id).name
    return HttpResponse("You're at the todolist named %s." % name)

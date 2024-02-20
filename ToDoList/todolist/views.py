from unittest import loader

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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
    li = get_object_or_404(List, pk=list_id)
    return render(request, 'todolist/detail.html', {'li': li})


def do_task(request, list_id):
    return HttpResponse("You are changing the status of list: %s." % list_id)

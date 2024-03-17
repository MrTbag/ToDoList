from django.shortcuts import render

from frontend.forms import TaskImportForm


def url_shortener(request):
    if request.method == 'GET':
        form = TaskImportForm()
        return render(request, 'frontend/url_shortener.html', {'form': form})

    return render(request, 'frontend/wrong_method.html')

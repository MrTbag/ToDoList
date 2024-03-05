from django.shortcuts import render
from .forms import UrlForm
from .models import UrlDict


def index(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['original_url']
            if not UrlDict.objects.filter(original_url=url).exists():
                hashed = str(abs(hash(url)))[:10]
                shortened_url = 'http://' + request.get_host() + request.get_full_path() + hashed
                while UrlDict.objects.filter(key=shortened_url).exists():
                    hashed = str(abs(hash(url)))[:10]
                    shortened_url = 'http://' + request.get_host() + request.get_full_path() + hashed
                dict_obj = UrlDict(key=shortened_url, original_url=url)
                dict_obj.save()

            else:
                shortened_url = UrlDict.objects.get(original_url=url).key

            return render(request, 'url_shortener/shortened_url_detail.html', {'url': shortened_url})

    elif request.method == 'GET':
        form = UrlForm()
        return render(request, 'url_shortener/url_form.html', {'form': form})
    else:
        return render(request, 'url_shortener/wrong_method.html')

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from todolist.models import Task
from todolist.serializers import TaskImportSerializer

from url_shortener.models import UrlDict


class Shorten(CreateAPIView):
    serializer_class = TaskImportSerializer
    queryset = Task.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']

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

            return Response({'url': shortened_url}, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import mimetypes
import os

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from transliterate import translit

# Create your views here.
from key_manual.models import Manual


def show_by_id(request, pk):
    manual = get_object_or_404(Manual, pk=pk)
    return render(request, 'key_manual/manual_detail.html', {
        'manual': manual
    })


def get_by_id(request, pk):
    manual = get_object_or_404(Manual, pk=pk)
    path = manual.path
    file_name = os.path.basename(path).lower()
    file_name = translit(file_name.replace(' ', '_'), 'ru', reversed=True)
    _type = mimetypes.guess_type(file_name)[0]
    if path and os.path.isfile(path):
        with open(path, 'rb') as file:
            response = HttpResponse(file, content_type=_type)
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response
    return HttpResponseNotFound()


def show_all(request):
    manuals = Manual.objects.all()
    return render(request, 'key_manual/manuals_list.html', {
        'manuals': manuals
    })

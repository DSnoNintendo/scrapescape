from django.shortcuts import render
from . import scraper
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
import mimetypes

def home(request):
    return render(request, 'scrapescape/home.html')

def run(request):
    scraper.run(request.POST['search_term'])
    path = 'file.zip'
    zip_file = open(path, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'images.zip'

    return response
    #download(requem  iist)

def download(request):
    path = 'file.zip'
    filename = 'file.zip'
    fl = open(path, 'r')
    mime_type, _ = mimetypes.guess_type(path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

from django.shortcuts import render
from . import scraper
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.middleware.csrf import get_token
import mimetypes
from scrapescape.models import Search

def home(request):
    return render(request, 'scrapescape/home.html')

def run(request):
    token = get_token(request)
    search_term = request.POST['search_term']
    #run function returns number of pictures found
    size = scraper.run(search_term, token)
    path = '%s.zip' % token
    zip_file = open(path, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % '%s.zip' % token

    Search.objects.create(keyword=search_term, output=size)
    print("Model created\nSearch Term: %s\nSize: %s" % (search_term, size))
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

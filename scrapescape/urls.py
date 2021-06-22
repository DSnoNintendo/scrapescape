from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='ScrapeScape'),
    path('run', views.run, name='script'),
]
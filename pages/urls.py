from django.urls import path
from . import views
from listings.views import search

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
]

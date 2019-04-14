from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bookscore", views.bookscore, name="bookscore"),
    path("addscore", views.bookscore, name="addscore"),
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete')
]

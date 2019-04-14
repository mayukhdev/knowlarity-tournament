from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bookscore", views.bookscore, name="bookscore"),
    path("addscore", views.addscore, name="addscore"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path('leaderboard/<int:sport_id>', views.leaderboard, name="leaderboard"),
    path('leaderboard/<int:sport_id>/<int:offset>/', views.leaderboard, name="leaderboard"),
    path('leaderboard/<int:sport_id>/<int:offset>/<int:limit>/', views.leaderboard, name="leaderboard"),
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete')
]

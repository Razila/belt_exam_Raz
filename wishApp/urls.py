from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("logout", views.logout),
    path("wishes", views.wishes),
    path("wishes/new", views.new),
    path("new_wish", views.new_wish),
    path("wishes/<int:wish_id>/edit", views.edit_wish),
    path("<int:wish_id>/update", views.update_wish),
    path("remove_wish", views.remove_wish),
    path("grant_wish", views.grant_wish),
    path("like", views.like_wish),
    path("wishes/stats", views.wish_stats)
]
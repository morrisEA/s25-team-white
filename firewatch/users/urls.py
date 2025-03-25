from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("manage_watch/", views.manage_watch, name="manage_watch"),
]

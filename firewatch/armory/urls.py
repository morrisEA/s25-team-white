from django.urls import path

from . import views

app_name = 'armory'

urlpatterns = [
    path("", views.index, name="index"),
    path('checkin/<int:watch_id>/', views.checkin, name='checkin'),
]

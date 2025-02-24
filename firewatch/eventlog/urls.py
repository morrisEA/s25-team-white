from django.urls import path

from . import views

urlpatterns = [
    path("", views.eventlog_view, name="eventlog")
]

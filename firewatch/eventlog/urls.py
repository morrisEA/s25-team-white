from django.urls import path

from . import views


app_name = 'eventlog'
urlpatterns = [
    path("", views.eventlog_view, name="eventlog")
]

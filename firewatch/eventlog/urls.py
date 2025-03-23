from django.urls import path

from . import views

app_name = 'eventlog'

urlpatterns = [
    # Existing event log view
    path("", views.eventlog_view, name="eventlog"),
]

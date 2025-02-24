from django.urls import path
from . import views


app_name = 'eventlog'
urlpatterns = [
    path("", views.eventlog_view, name="eventlog"),
    path("scan/", views.scan_rfid, name="scan_rfid"), # endpoint for simulating RFID scan
    path("scan_log", views.get_scan_log, name="scan_log"), # endpoint for retrieving scan history
    
]

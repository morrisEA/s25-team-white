from django.urls import path

from . import views

from .views import RFIDScanListCreateView


app_name = 'eventlog'

urlpatterns = [
    # Existing event log view
    path("", views.eventlog_view, name="eventlog"),

    # New API endpoint for storing and retrieving RFID scan data
    path("api/rfid-scans/", RFIDScanListCreateView.as_view(), name="rfid-scan-list-create"),
    
]

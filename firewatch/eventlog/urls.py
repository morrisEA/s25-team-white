from django.urls import path
from .views import eventlog_view, simulate_rfid_scan

from . import views

from .views import RFIDScanListCreateView


app_name = 'eventlog'

urlpatterns = [
    # Existing event log view
    path("", views.eventlog_view, name="eventlog"),

    # Route that triggers the simulated RFID scan view and show the modal form
    path("simulate-rfid-scan/", views.simulate_rfid_scan, name="simulate-rfid-scan"),
]

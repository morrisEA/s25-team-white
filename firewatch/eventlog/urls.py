from django.urls import path
from .views import eventlog_view, rfid_scan_entry, rfid_modal_simulation_view

from . import views


app_name = 'eventlog'

urlpatterns = [
    # Existing event log view
    path("", views.eventlog_view, name="eventlog"),

    # Route that triggers the simulated RFID scan view and show the modal form
    path("rfid-scan-entry/", views.rfid_scan_entry, name="rfid-scan-entry"),

    # New: Route for modal-bassed RFID simulation
    path("rfid-modal-sim/", views.rfid_modal_simulation_view, name="rfid-modal-sim"),
]

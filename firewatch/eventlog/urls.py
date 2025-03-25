from django.urls import path
from .views import eventlog_view, simulate_rfid_scan, rfid_modal_simulation_view

from . import views


app_name = 'eventlog'

urlpatterns = [
    # Existing event log view
    path("", views.eventlog_view, name="eventlog"),

    # Route that triggers the simulated RFID scan view and show the modal form
    path("simulate-rfid-scan/", views.simulate_rfid_scan, name="simulate-rfid-scan"),

    # New: Route for modal-bassed RFID simulation
    path("rfid-modal-sim/", views.rfid_modal_simulation_view, name="rfid-modal-sim"),
]

from django.shortcuts import render

from armory.models import Watch

# HTML view for the event log page
def eventlog_view(request):
    watches = Watch.objects.all().order_by('-check_in')
    return render(request, "eventlog/eventlog.html", {
        'watches': watches
    })  

# View for the RFID scan simulation form
import random
from .forms import RFIDScanForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Django form-based view to simulate RFID scan
def rfid_scan_entry(request):
    """
    View to simulate RFID scan via a Django form.
    Generates a random serial number and submits it using a Django form.
    """
    from .rfid_reader import RFIDReader

    reader = RFIDReader()
    generated_serial = reader.generate_serial_number()
    encoded_bytes = reader.encode_ndef(generated_serial)
    decoded_serial = reader.decode_ndef(encoded_bytes)

    if request.method == "POST":
        form = RFIDScanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("eventlog:eventlog"))
    else:
        # This ensures generating a compliant serial, encoding/decoding as real NDEF
        form = RFIDScanForm(initial={'serial_number': decoded_serial})

    return render(request, "eventlog/rfid_scan_entry.html", {
        "form": form
        })

# Standalone page to simulate RFID modal without affecting logs page
def rfid_modal_simulation_view(request):
    return render(request, "eventlog/rfid_modal_simulation.html")

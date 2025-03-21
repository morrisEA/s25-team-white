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

def simulate_rfid_scan(request):
    """
    View to simulate RFID scan via a Django form.
    Generates a random serial number and submits it using a Django form.
    """
    gernerated_serial = f"FW-{random.randint(10000, 99999)}"

    if request.method == "POST":
        form = RFIDScanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("eventlog:eventlog"))
    else:
        form = RFIDScanForm(initial={'serial_number': gernerated_serial})

    return render(request, "eventlog/simulate_rfid_scan.html", {
        "form": form
        })


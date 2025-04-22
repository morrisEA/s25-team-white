from django.shortcuts import render

from armory.models import Watch, Magazine

# HTML view for the event log page
def eventlog_view(request):
    watches = Watch.objects.all().order_by('-check_in')
    
    try:
        magazines = Magazine.objects.all()
    except:
        magazines = None
    return render(request, "eventlog/eventlog.html", {
        'watches': watches,
        'magazines' : magazines,
    })  

# View for the RFID scan simulation form
import random
from .forms import RFIDScanForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from armory.models import Firearm 
import datetime

# Django form-based view to simulate RFID scan
def rfid_scan_entry(request):
    from .rfid_reader import RFIDReader
    from armory.models import Firearm, Magazine

    reader = RFIDReader()
    generated_serial = reader.generate_serial_number()
    encoded_bytes = reader.encode_ndef(generated_serial)
    decoded_serial = reader.decode_ndef(encoded_bytes)

    magazines = Magazine.objects.all()
    firearm_choices = ["M9", "M4A1", "M240B"]
    error_message = None  # new

    if request.method == "POST":
        form = RFIDScanForm(request.POST)
        firearm_type = request.POST.get("firearm_type")
        magazine_id = request.POST.get("magazine")

        if form.is_valid():
            serial_number = form.cleaned_data["serial_number"]

            # 🔍 Check if firearm already exists
            if Firearm.objects.filter(serial_number=serial_number).exists():
                error_message = f"A firearm with serial number '{serial_number}' already exists."
            else:
                firearm = Firearm(
                    firearm_type=firearm_type,
                    serial_number=serial_number,
                    maintenance_date=datetime.datetime.now(),
                    available=True,
                    magazine_id=Magazine.objects.filter(id=magazine_id).first()
                )
                firearm.save()
                return render(request, "eventlog/rfid_scan_entry.html", {
                    "form": form,
                    "magazines": magazines,
                    "firearm_choices": firearm_choices,
                    "success_message": f"Firearm {serial_number} added to inventory.",
                })

    else:
        form = RFIDScanForm(initial={'serial_number': decoded_serial})

    return render(request, "eventlog/rfid_scan_entry.html", {
        "form": form,
        "magazines": magazines,
        "firearm_choices": firearm_choices,
        "error_message": error_message,  # pass the message
    })



# Standalone page to simulate RFID modal without affecting logs page
def rfid_modal_simulation_view(request):
    return render(request, "eventlog/rfid_modal_simulation.html")

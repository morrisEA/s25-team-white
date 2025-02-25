from django.shortcuts import render
from django.http import JsonResponse
from .rfid_reader import RFIDReader # Import RFIDReader module

# Create an instance of the RFID reader
rfid_reader = RFIDReader()

# Create your views here.
def eventlog_view(request):
    return render(request, "eventlog/eventlog.html")

def scan_rfid(request):
    """Simulate an RFID scan event and return the scanned tag details."""
    scan_event = rfid_reader.generate_fake_scan()
    return JsonResponse(scan_event)

def get_scan_log(request):
    """Retrieve all past RFID scan events."""
    return JsonResponse({"scan_log": rfid_reader.get_scan_log()}) 


from django.shortcuts import render

# HTML view for the event log page
def eventlog_view(request):
    return render(request, "eventlog/eventlog.html")

# REST API imports and view
from rest_framework import generics
from .models import RFIDScan
from .serializers import RFIDScanSerializer

class RFIDScanListCreateView(generics.ListCreateAPIView):
    """
    API view to handle GET and POST requests for RFID scans.
    GET: Returns a list of all RFID scans.
    POST: Stores a new RFID scan entry.
    """
    queryset = RFIDScan.objects.all()
    serializer_class = RFIDScanSerializer  



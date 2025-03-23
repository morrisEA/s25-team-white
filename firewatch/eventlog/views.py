from django.shortcuts import render
from armory.models import Watch

# Create your views here.
def eventlog_view(request):
    watches = Watch.objects.all().order_by('-check_in')
    return render(request, "eventlog/eventlog.html", {
        'watches': watches
    })  


from django.shortcuts import render

# Create your views here.
def eventlog_view(request):
    return render(request, "eventlog/eventlog.html")  


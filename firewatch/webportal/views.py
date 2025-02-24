from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Hardcoded credentials for testing login
        if username == "username" and password == "password":
            # Redirect to login on successful login, to admin/main page
            return redirect('main')  
        else:
            error_message = "Invalid username or password"
            return render(request, "webportal/login.html", {'error_message': error_message})
    
    return render(request, "webportal/login.html")

#main page
def main_view(request):
    return render(request, "webportal/main.html")

#inventory page
def inventory_view(request):
    return render(request, "webportal/inventory.html")  

#scanning RFID page
def scan_view(request):
    return render(request, "webportal/scan.html")  

#Log viewing page
def logs_view(request):
    return render(request, "webportal/logs.html")  

#notifications page
def notifications_view(request):
    return render(request, "webportal/notifications.html") 
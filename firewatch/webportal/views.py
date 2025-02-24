from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Hardcoded credentials for testing
        if username == "username" and password == "password":
            # Redirect to login on successful login
            return redirect('main')  
        else:
            error_message = "Invalid username or password"
            return render(request, "webportal/login.html", {'error_message': error_message})
    
    return render(request, "webportal/login.html")

def main_view(request):
    return render(request, "webportal/main.html")
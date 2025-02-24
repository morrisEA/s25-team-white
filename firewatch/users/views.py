from django.shortcuts import render, redirect

# Create your views here.
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
            return render(request, "users/login.html", {'error_message': error_message})
    
    return render(request, "users/login.html")




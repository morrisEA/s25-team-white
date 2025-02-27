from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login")) 
    return render(request, "users/dashboard.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "users/login.html")

def logout_view(request):
    user = request.user.username
    logout(request)
    return render(request, "users/login.html", {
        "message": f"{user} has logged out."
    })





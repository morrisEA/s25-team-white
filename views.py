from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # ✅ Add this line
from armory.models import Watch  # Import the Watch model

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login")) 
    return render(request, "users/dashboard.html")

@login_required
def dashboard(request):
    """Display user's active watches"""
    watches = Watch.objects.filter(member_id=request.user.servicemember)
    return render(request, "users/dashboard.html", {"watches": watches})

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





import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

logger = logging.getLogger("core")


def homepage(request):
    logger.info("Homepage accessed")
    return render(request, "core/homepage.html")


def register(request):
    if request.method == "POST":
        logger.info("Processing new user registration")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in right after registering
            logger.info(f"New user registered successfully: {user.username}")
            messages.success(request, "Account created successfully!")
            return redirect("homepage")  # Redirect to your homepage or desired page
        else:
            logger.warning(f"Registration failed: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, "core/register.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            logger.info(f"User {username} logged out")
        return redirect("homepage")
    return render(request, "registration/logout.html")

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
    logger.info("=== Register view accessed ===")
    if request.method == "POST":
        logger.info("Processing new user registration")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user registered successfully: {user.username}")
            messages.success(request, "Account created successfully!")
            return redirect("homepage")
        else:
            logger.warning(f"=== Registration failed with errors: {form.errors} ===")
            for field, errors in form.errors.items():
                logger.warning(f"Field '{field}' errors: {errors}")
    else:
        logger.info("=== Displaying registration form ===")
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

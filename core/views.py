from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm


def homepage(request):
    return render(request, "core/homepage.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in right after registering
            messages.success(request, "Account created successfully!")
            return redirect("homepage")  # Redirect to your homepage or desired page
    else:
        form = CustomUserCreationForm()
    return render(request, "core/register.html", {"form": form})

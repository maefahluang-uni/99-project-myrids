from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.\

def signup (request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("matching:home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form":form})
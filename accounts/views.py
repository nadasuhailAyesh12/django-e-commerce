from django.contrib import messages
from django.shortcuts import render
from django.views import View

from .forms import SignUpForm

# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return render(request, "accounts/register.html", {"form": form})
        else:
            messages.error(
                request, "Error creating account,please see the error below!"
            )
            return render(request, "accounts/register.html", {"form": form})

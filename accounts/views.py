from django.contrib import auth, messages
from django.shortcuts import redirect, render
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


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return render(request, "home.html")
        else:
            messages.error(request, "Invalid email or password!")
            return render(request, "accounts/login.html")


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("login")

from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from accounts.models import Account

from .forms import SignUpForm


def sendEmail(request, user, subject, template):
    current_site = get_current_site(request)
    message = render_to_string(
        template,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    send_email = EmailMessage(subject=subject, body=message, to=[to_email])
    send_email.send()


class RegisterView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = user.email
            print(user.email)

            sendEmail(
                request,
                user,
                "Activate your account",
                "accounts/account_verification_email.html",
            )  # Send email verification link to user

            # messages.success(request, "Account created successfully!")
            return redirect("/accounts/login/?command=verification&email=" + email)
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
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            user = None

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, "Login successful!")
                return render(request, "accounts/dashboard.html")
            else:
                return redirect("/accounts/login/?command=verification&email=" + email)
        else:
            messages.error(request, "Invalid email or password!")
            return render(request, "accounts/login.html")


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("login")


class ActivateView(View):
    def get(self, request, *args, **kwargs):
        uid64 = kwargs.get("uidb64")
        token = kwargs.get("token")
        print(uid64, token, "nada")

        try:
            uid = urlsafe_base64_decode(uid64)
            user = Account._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully!")
            return render(request, "accounts/login.html")
        else:
            messages.error(request, "Invalid activation link!")
            return redirect("register")


class DashboardView(LoginRequiredMixin, View):
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):
        return render(request, "accounts/dashboard.html")


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, "accounts/forgot_password.html")

    def post(self, request):
        email = request.POST["email"]
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            user = None

        if user is not None:
            sendEmail(
                request,
                user,
                "Reset Password",
                "accounts/password_reset_email.html",
            )  # Send password reset link to user
            messages.success(request, "Password reset link sent to your email!")
            return render(request, "accounts/login.html")
        else:
            messages.error(request, "Invalid email!")
            return render(request, "accounts/forgot_password.html")


class ResetPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")

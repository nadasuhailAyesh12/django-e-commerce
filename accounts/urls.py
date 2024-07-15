from django.urls import path

from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>/", views.ActivateView.as_view(), name="activate"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("forgotPassowrd/", views.ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "resetPassword/<uidb64>/<token>/",
        views.ResetPasswordView.as_view(),
        name="reset_password_validate",
    ),
    path("", views.DashboardView.as_view(), name="dashboard"),
]

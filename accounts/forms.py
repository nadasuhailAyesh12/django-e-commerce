from django.contrib.auth.forms import UserCreationForm

from .models import Account


class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    error_messages = {
        "password_mismatch": ("The two password fields didn't match."),
        "unique": {
            "email": ("A user with that email already exists."),
            "username": ("A user with that username already exists."),
        },
    }

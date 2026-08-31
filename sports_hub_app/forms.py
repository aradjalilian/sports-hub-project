from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from sports_hub_app.models import User, Product


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ["name", "email"]

        labels = {
            "name": "Full Name",
            "email": "Email Address",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if (
            password
            and password_confirm
            and password != password_confirm
        ):
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]

        labels = {
            "name": "Full Name",
            "email": "Email Address",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid email or password."
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "category",
            "description",
            "image",
            "price",
            "stock",
            "status"
        ]

        widgets = {
            "product_id": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }
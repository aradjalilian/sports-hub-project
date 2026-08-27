from django import forms
from sports_hub_app.models import User, Product

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "image", "price", "stock", "status"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
        }
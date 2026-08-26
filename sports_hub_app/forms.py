from django import forms
from sports_hub_app.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]

from django.shortcuts import render

def home(request):
    return render(request, "sports_hub_app/home.html")
from django.shortcuts import render

def returns(request):
    return render(request, "sports_hub_app/return_list.html")
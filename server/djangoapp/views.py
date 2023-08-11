from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages
from .models import CarDealer
from .restapis import get_dealers_from_cf

def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

def logout_request(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"Logged out: {username}")
    return redirect('djangoapp:index')

def registration_request(request):
    return render(request, 'djangoapp/registration.html')

def get_dealerships(request):
    if request.method == "GET":
        url = "your-cloud-function-domain/dealerships/dealer-get"
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)

def get_dealer_details(request, dealer_id):
    return HttpResponse(dealer_id)

def add_review(request, dealer_id):
    pass

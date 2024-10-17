from django.shortcuts import render, redirect
from django.contrib.auth.forms import *
from .models import Restaurant, Table, Booking

def index(request):
    restaurants = Restaurant.objects.all()
    tables = Table.objects.all()

    context = {
        'restaurants': restaurants,
        'tables': tables
    }

    return render(
        request,
        'index.html',
        context=context
    )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
        
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
        

def restaurant(request, restaurant_id):
    cur_res = Restaurant.objects.filter(id=restaurant_id).first()

    context = {
        'restaurant': cur_res
    }

    return render(
        request,
        'restaurant.html',
        context=context
    )

def table(request, table_id):
    cur_tab = Table.objects.filter(id=table_id).first()

    context = {
        'table': cur_tab
    }

    print(Table.objects.all())

    return render(
        request,
        'table.html',
        context=context
    )

def booking_list(request):
    bookings = Booking.objects.all()
    
    context = {
        'bookings': bookings
    }
    return render(request, 'booking.html', context)
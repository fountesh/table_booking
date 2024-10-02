from django.shortcuts import render
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

    return render(
        request,
        'table.html',
        context=context
    )

def booking(request):
    booking = Booking.objects.all()

    context = {
        'booking': booking
    }

    return render(
        request,
        'booking.html',
        context=context    
    )
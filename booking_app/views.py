from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Table, Booking
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
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

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправлення на сторінку, з якої користувач прийшов
                next_page = request.GET.get('next', 'index')
                return redirect(next_page)
            else:
                messages.error(request, 'Невірний логін або пароль')
        else:
            messages.error(request, 'Невірний логін або пароль')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
        
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
         
@login_required
def restaurant(request, restaurant_id):
    cur_res = Restaurant.objects.filter(id=restaurant_id).first()

    if request.method == "POST":
        table_id = request.POST.get("table_id")
        data = request.POST.get("data")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        # Перевірка конфліктів
        existing_bookings = Booking.objects.filter(
            table_id=table_id,
            data=data,
            start_time__lt=end_time,  # Час початку існуючого бронювання раніше закінчення нового
            end_time__gt=start_time   # Час закінчення існуючого бронювання пізніше початку нового
        )

        if existing_bookings.exists():
            messages.error(request, "Цей столик вже заброньовано на вибраний час!")
            return redirect('restaurant', restaurant_id=restaurant_id)

        # Створення бронювання
        user = request.user
        Booking.objects.create(
            res_name=cur_res,
            table_id=Table.objects.get(pk=table_id),
            user_id=user,
            data=data,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(request, "Столик успішно заброньовано!")
        return redirect('restaurant', restaurant_id=restaurant_id)

    context = {
        'restaurant': cur_res
    }

    return render(
        request,
        'restaurant.html',
        context=context
    )

@login_required
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
@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    
    context = {
        'bookings': bookings
    }
    return render(request, 'booking.html', context)

@login_required
def booking_page(request):
    table_id = request.GET.get('table_id')
    restaurant_id = request.GET.get('restaurant_id')

    # Отримуємо ресторан і перевіряємо, чи столик належить йому
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    selected_table = restaurant.tables.filter(table_id=table_id).first()

    if not selected_table:
        messages.error(request, "Обраний столик не належить цьому ресторану.")
        return redirect('restaurant', restaurant_id=restaurant_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not all([table_id, date, start_time, end_time]):
            messages.error(request, "Усі поля обов'язкові для заповнення.")
        else:
            conflict = Booking.objects.filter(
                table_id=table_id,
                data=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if conflict:
                messages.error(request, "Столик уже заброньовано на цей час.")
            else:
                Booking.objects.create(
                    res_name=restaurant,
                    table_id=selected_table,
                    user_id=request.user,
                    data=date,
                    start_time=start_time,
                    end_time=end_time,
                )
                messages.success(request, "Ваше бронювання успішно створено!")
                return redirect('restaurant', restaurant_id=restaurant_id)

    return render(request, 'booking_page.html', {
        'selected_table': selected_table,
        'restaurant': restaurant,
    })

@login_required
def update_booking_status(request, booking_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Доступ заборонено")

    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.BOOKING_STATUS).keys():
            booking.status = new_status
            booking.save()
            messages.success(request, f"Статус бронювання оновлено до '{new_status}'")
        else:
            messages.error(request, "Недійсний статус")
    return redirect('booking')

@login_required
def delete_booking(request, booking_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Доступ заборонено")

    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Бронювання успішно видалено")
    return redirect('booking')
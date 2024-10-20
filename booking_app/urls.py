from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/<int:restaurant_id>', views.restaurant, name='restaurant'),
    path('table/<int:table_id>', views.table, name='table'),
    path('booking', views.booking_list, name='booking'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
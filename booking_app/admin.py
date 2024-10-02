from django.contrib import admin
from .models import Restaurant, Table, Booking

# Register your models here.

@admin.register(Restaurant)
class RestourantAdmin(admin.ModelAdmin):
    list_display = ('title', 'adress')
    search_fields = ('title', 'adress')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'res_name', 'price', 'num', 'status')
    list_filter = ('res_name', 'status')
    search_fields = ('res_name__title', 'num')

@admin.register(Booking)
class BoolingAdmin(admin.ModelAdmin):
    list_display = ('res_name', 'table_id', 'user_id', 'data', 'status')
    list_filter = ('res_name', 'status', 'data')
    search_fields = ('res_name__title', 'user_id__username')
    date_hierarchy = 'data'
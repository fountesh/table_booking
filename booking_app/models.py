from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Restaurant(models.Model):
    title = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.title} знаходиться на: {self.adress}"

class Table(models.Model):
    TABLE_STATUS = [
        ('вільний', 'Вільний'),
        ('зайнятий', 'Зайнятий'),
        ('в очікуванні', 'В очікуванні'),
    ]
    
    table_id = models.AutoField(primary_key=True)
    res_name = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    price = models.IntegerField()
    num = models.IntegerField()
    status = models.CharField(max_length=20, choices=TABLE_STATUS, default='вільний')

    def __str__(self) -> str:
        return f"столик {self.num} коштує {self.price}, знаходиться у {self.res_name} і має статус {self.get_status_display()}"

class Booking(models.Model):
    BOOKING_STATUS = [
        ('Прийшов', 'Прийшов'),
        ('В очікуванні', 'В очікуванні'),
        ('Неприйшов', 'Неприйшов'),
    ]

    res_name = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookings')
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    start_time = models.TimeField(default=timezone.now())  # Час початку бронювання
    end_time = models.TimeField(default=timezone.now())    # Час завершення бронювання
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='В очікуванні')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'Прийшов':
            self.table_id.status = 'зайнятий'
        elif self.status == 'В очікуванні':
            self.table_id.status = 'в очікуванні'
        else:
            self.table_id.status = 'вільний'
        self.table_id.save()

    def __str__(self):
        return f"{self.res_name}, {self.table_id}, {self.status}"
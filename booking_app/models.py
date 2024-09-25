from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Restourant(models.Model):
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
    res_name = models.ForeignKey(Restourant, on_delete=models.CASCADE)
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
    
    res_name = models.ForeignKey(Restourant, on_delete=models.CASCADE)
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
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
""" Файл описывает структуру таблицы в базе данных с помощью ORM"""
from django.db import models

class Flight(models.Model):
    """
    Модель описывает структуру таблицы, в которой хранятся данные о рейсах.
    """

    flight_id = models.CharField(max_length=50, unique=True)
    airline = models.CharField(max_length=100) # авиакомпания

    origin_airport = models.CharField(max_length=10) # из
    destination_airport = models.CharField(max_length=10) # в
    departure_delay_min = models.IntegerField(default=0) # задержка
    # Потом дописать атрибуты для ост. структур данных

    def __str__(self):
        return f"{self.flight_id} - {self.airline}"

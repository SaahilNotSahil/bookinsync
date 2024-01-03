from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Route(models.Model):
    id = models.AutoField(primary_key=True)
    src = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="routes_with_src",
        related_query_name="route_with_src"
    )
    dst = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="routes_with_dst",
        related_query_name="route_with_dst"
    )

    class Meta:
        verbose_name_plural = "Routes"

    def __str__(self):
        return self.src.name + " - " + self.dst.name


class Bus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    capacity = models.IntegerField()
    occupancy = models.IntegerField()
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="buses",
        related_query_name="bus"
    )

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return self.name

    @property
    def remaining_seats(self):
        return self.capacity - self.occupancy

    @property
    def is_full(self):
        return self.occupancy == self.capacity


class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name="seats",
        related_query_name="seat"
    )
    booked = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seats",
        related_query_name="seat",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Seats"

    def __str__(self):
        return str(self.bus.name) + " - " + str(self.number)

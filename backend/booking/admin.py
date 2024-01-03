from django.contrib import admin

from .models import Bus, City, Route, Seat


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    class Meta:
        model = City


class RouteAdmin(admin.ModelAdmin):
    list_filter = ('src__name', 'dst__name')
    search_fields = ('src__name', 'dst__name')

    class Meta:
        model = Route


class BusAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'number',
        'capacity',
        'occupancy',
        'route',
        'is_full',
        'remaining_seats'
    )
    list_filter = ('route',)
    search_fields = ('name', 'number', 'route__src__name', 'route__dst__name')

    class Meta:
        model = Bus


class SeatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'bus', 'booked', 'user')
    list_filter = ('bus__name', 'booked', 'user')
    search_fields = ('bus__name', 'booked', 'user')

    class Meta:
        model = Seat


admin.site.register(City, CityAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Seat, SeatAdmin)

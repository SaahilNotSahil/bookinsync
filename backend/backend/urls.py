from django.contrib import admin
from django.urls import include, path

from booking.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authn.urls')),
    path('', index, name='index'),
    path("api/booking/", include("booking.urls")),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('warehouse.urls')),
    path('api/', include('warehouse.api_urls')),
    path('warehouse/', include('warehouse.urls')),

]


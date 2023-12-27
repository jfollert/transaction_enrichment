from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("categories/", include("categories.urls", namespace='categories')),
    path("merchants/", include("merchants.urls", namespace='merchants')),
    path("keywords/", include("keywords.urls", namespace='keywords')),
]

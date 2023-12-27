from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.create_category, name="create_category"),
]
from django.urls import path
from . import views

app_name = 'merchants'

urlpatterns = [
    path("", views.merchants_view, name="merchants"),
    path('<uuid:id>/', views.merchant_detail, name='merchant_detail'),
]
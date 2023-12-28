from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path("", views.transactions_view, name="transactions"),
    # path('<uuid:id>/', views.merchant_detail, name='merchant_detail'),
]
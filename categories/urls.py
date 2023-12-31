from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path("", views.categories_view, name="categories"),
    path('<uuid:id>/', views.category_detail, name='category_detail'),
]
from django.urls import path
from . import views

app_name = 'keywords'

urlpatterns = [
    path("", views.keywords_view, name="keywords"),
    path('<uuid:id>/', views.keyword_detail, name='keyword_detail'),
]
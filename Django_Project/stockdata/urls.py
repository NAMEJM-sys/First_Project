from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stock_data_view, name='stock_list'),
]
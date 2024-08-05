from django.urls import path
from .views import login_view, stock_data_view, signup_view

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('stocks/', stock_data_view, name='stock_list'),
]
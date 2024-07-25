from django.shortcuts import render
from .models import StockData

def stock_list(request):
    stocks = StockData.objects.all()
    return render(request, 'stockdata/stock_list.html', {'stocks': stocks})
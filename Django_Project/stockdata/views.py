from django.shortcuts import render
from .models import StockData

def stock_data_view(request):
    stocks = StockData.objects.values('stock_code', 'stock_name').distinct()
    stock_list = None
    selected_stock = request.GET.get('stock_name')

    if selected_stock:
        stock_code = stocks.filter(stock_name=selected_stock).values_list('stock_code', flat=True).first()
        if stock_code:
            stock_list = StockData.objects.filter(stock_code=stock_code).order_by('-date')

    return render(request, 'stockdata/stock_list.html', {
        'stock_list': stock_list,
        'stocks': stocks,
        'selected_stock': selected_stock
    })
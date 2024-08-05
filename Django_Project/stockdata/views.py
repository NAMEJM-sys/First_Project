from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import StockData
from .collect_data import collect_stock_data

def login_view(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        user = authenticate(username=id, password=password)
        if user:
            login(request, user)
            collect_stock_data()
            return redirect('stock_list')
        else:
            return render(request, 'stockdata/login.html', {'error': 'Invalid credentials'})
    return render(request, 'stockdata/login.html')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'stockdata/signup.html')



def stock_data_view(request):
    stocks = StockData.objects.values('stock_code', 'stock_name').distinct()
    stock_list = None
    selected_stock = request.GET.get('stock_name')

    if selected_stock:
        stock_code = stocks.filter(stock_name=selected_stock).values_list('stock_code', flat=True).first()
        if stock_code:
            stock_list = StockData.objects.filter(stock_code=stock_code).order_by('-date').values_list('date', 'close_price')

    return render(request, 'stockdata/stock_list.html', {
        'stock_list': stock_list,
        'stocks': stocks,
        'selected_stock': selected_stock
    })
import sys
from .kiwoom import KiwoomAPI
from datetime import datetime, timedelta
from .models import StockData
import django
django.setup()



def collect_stock_data():
    kiwoom = KiwoomAPI()
    stock_codes = ["005930", "000660", "066570", "105560"]  # 예시 주식 코드
    stock_list = kiwoom.collect_data(stock_codes)

    # 데이터베이스에 저장
    for code, data in stock_list.items():
        for date, price in data:
            stock, created = StockData.objects.update_or_create(
                stock_code=code,
                date=datetime.strptime(date, '%Y%m%d').date(),
                defaults={'close_price': price}
            )
            if created:
                print(f"Created new record for {stock}")
            else:
                print(f"Updated record for {stock}")
    return stock_list

if __name__ == "__main__":
    collect_stock_data()
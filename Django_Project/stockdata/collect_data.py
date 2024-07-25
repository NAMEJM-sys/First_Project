from .models import StockData
from .kiwoom import KiwoomAPI


def collect_data():
    kiwoom = KiwoomAPI()
    stock_codes = ["005930", "000660", "066570", "105560"]  # 삼성전자, SK하이닉스
    stock_data_list = kiwoom.collect_data(stock_codes)

    for data in stock_data_list:
        StockData.objects.update_or_create(
            stock_code=data["종목코드"],
            defaults={
                "stock_name": data["종목명"],
                "current_price": data["현재가"],
                "trading_volume": data["거래량"],
                "date": "2024-07-25"  # 실제로는 현재 날짜를 사용
            }
        )
import sys
import pythoncom
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget
from datetime import datetime

class KiwoomAPI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect()")
        self.ocx.OnEventConnect.connect(self._event_connect)  # 시그널 연결
        self.ocx.OnReceiveTrData.connect(self._receive_tr_data)  # 시그널 연결
        self.login_event_loop = QEventLoop()
        self.data_event_loop = QEventLoop()
        self.data = []
        self.current_code = None
        self.start_date = None
        self.end_date = None

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        try:
            if err_code == 0:
                print("로그인 성공")
            else:
                print("로그인 실패")
        except Exception as e:
            print(f"Error in _event_connect: {e}")
        finally:
            self.login_event_loop.exit()

    def get_stock_data(self, code, start_date):
        self.data = []
        self.current_code = code
        self.start_date = start_date.strftime("%Y%m%d")
        self._request_stock_data(self.current_code, self.end_date)

    def _request_stock_data(self, code, date):
        try:
            self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
            self.ocx.dynamicCall("SetInputValue(QString, QString)", "시작일자", date)
            self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "일별거래상세요청", "opt10015", 0, "0101")
            self.data_event_loop.exec_()
        except Exception as e:
            self.data_event_loop.exit()

    def _receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        try:
            if rqname == "일별거래상세요청":
                data_count = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
                for i in range(data_count):
                    close_price = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종가").strip()
                    date = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "일자").strip()
                    self.data.append((date, abs(int(close_price))))

                if prev_next == "2":  # 연속 조회 처리
                    last_date = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, data_count - 1, "일자").strip()
                    if last_date < self.start_date or last_date > self.end_date:
                        self.data_event_loop.exit()
                    else:
                        self._request_stock_data(self.current_code, last_date)
                else:
                    self.data_event_loop.exit()
        except Exception as e:
            self.data_event_loop.exit()

    def collect_data(self, codes):
        pythoncom.CoInitialize()
        self.login()
        all_stock_data = {}
        start_date = datetime.now()
        try:
            for code in codes:
                self.get_stock_data(code, start_date)
                all_stock_data[code] = self.data
        except Exception as e:
            print(f"Error in collect_data: {e}")
        finally:
            pythoncom.CoUninitialize()
        return all_stock_data

if __name__ == "__main__":
    kiwoom = KiwoomAPI()
    try:
        stock_data = kiwoom.collect_data(["005930", "000660", "066570", "105560"])
        for code, data in stock_data.items():
            for date, price in data:
                print(f"Date: {date}, Close price: {price}")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        QApplication.exit()
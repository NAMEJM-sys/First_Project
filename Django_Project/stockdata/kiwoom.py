import sys
import pythoncom
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget


class KiwoomAPI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._event_connect)
        self.ocx.OnReceiveTrData.connect(self._receive_tr_data)
        self.login_event_loop = QEventLoop()
        self.data_event_loop = QEventLoop()
        self.data = None

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
        else:
            print("로그인 실패")
        self.login_event_loop.exit()

    def get_stock_data(self, code):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, "0101")
        self.data_event_loop.exec_()
        return self.data

    def _receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "주식기본정보요청":
            self.data = {
                "종목코드": self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "종목코드").strip(),
                "종목명": self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "종목명").strip(),
                "현재가": abs(int(self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "현재가").strip())),
                "거래량": int(self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "거래량").strip())
            }
            self.data_event_loop.exit()

    def collect_data(self, codes):
        pythoncom.CoInitialize()
        self.login()
        stock_data = []
        for code in codes:
            data = self.get_stock_data(code)
            stock_data.append(data)
        pythoncom.CoUninitialize()
        return stock_data

if __name__ == "__main__":
    kiwoom = KiwoomAPI()
    stock_data = kiwoom.collect_data(["005930", "000660", "066570", "105560"])
    for data in stock_data:
        print(data)

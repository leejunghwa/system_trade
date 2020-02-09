#-*- coding:utf-8 -*-

import sys
import time
import schedule
import datetime
import logging
import argparse

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton,\
    QLineEdit, QTextEdit
from PyQt5.QAxContainer import QAxWidget

from pprint import pformat, pprint

# for slacker
from slacker import Slacker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdlr = logging.FileHandler('system_trader.log')
hdlr.setLevel(logging.INFO)
logger.addHandler(hdlr)

# for error Handling
sys._excepthook = sys.excepthook

def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook


class KiwoomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_kiwoom_transaction()
        self._init_kiwoom_window()
        self._init_slacker()

    def _init_kiwoom_transaction(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # Kiwoom OpenAPI Login
        self.kiwoom.dynamicCall("CommConnect()")

        self.kiwoom.OnEventConnect.connect(self.login_evt_hdr)
        self.kiwoom.OnReceiveTrData.connect(self.rcv_tr_evt_hdr)

    def _init_kiwoom_window(self):
        # Use: setGeometry(x, y, width, height)
        # Main Window Make
        self.setWindowTitle("System Trading HTS")
        self.setGeometry(300, 300, 300, 150)

        # Main Window Stock Code label Init
        stock_code_label = QLabel('종목코드: ', self)
        stock_code_label .setGeometry(20, 20, 60, 30)

        # Main Window Code Input LineEdit Init
        self.stock_code_edit = QLineEdit(self)
        self.stock_code_edit.setGeometry(80, 20, 100, 30)
        self.stock_code_edit.setText("030200")

        # Main Window Lookup Button Init
        lookup_button = QPushButton("조회", self)
        lookup_button.setGeometry(190, 20, 100, 30)
        lookup_button.clicked.connect(self.lookup_button_clicked_evt_hdr)

        # Main Window Result TextEdit Init
        self.tr_res_edit = QTextEdit(self)
        self.tr_res_edit.setGeometry(10, 60, 280, 80)
        self.tr_res_edit.setEnabled(False)

    def _init_slacker(self):
        # add Slack Bot Auth Token
        self.slack = Slacker("xoxb-XXXX")
        self.slack_channel = "system_trade"

    def slack_messages(self, messages):
        self.slack.chat.post_message(self.slack_channel, messages)

    def MsgSlack(self, post, color):
        attachments = []
        for post_key, post_value in post.items():
            att_dic = {}
            att_dic["title"] = post_key
            att_dic["title_link"] = post_value
            att_dic["color"] = color
            attachments.append(att_dic)

        return attachments


    def login_evt_hdr(self, err_code):
        print("this is event connect")
        if err_code == 0:
            self.tr_res_edit.append("Login Success")

    def rcv_tr_evt_hdr(self, screen_no, rqname, trcode, recordname,
                       prev_next, data_len, err_code, msg1, msg2):
        print("this is receive transaction handler")
        if rqname == "opt10001_req":
            name = self.kiwoom.dynamicCall(*self.mk_str(
                "get", [trcode, "", rqname, 0, "종목명"]))
            volume = self.kiwoom.dynamicCall(*self.mk_str(
                "get", [trcode, "", rqname, 0, "거래량"]))
            current_price= self.kiwoom.dynamicCall(*self.mk_str(
                "get", [trcode, "", rqname, 0, "시가"]))
            high_for_the_year = self.kiwoom.dynamicCall(*self.mk_str(
                "get", [trcode, "", rqname, 0, "연중최고"]))
            low_for_the_year = self.kiwoom.dynamicCall(*self.mk_str(
                "get", [trcode, "", rqname, 0, "연중최저"]))

            self.slack_messages("입력하신 종목명: {}".format(name.strip()))
            self.slack_messages("입력하신 종목의 현재 가격: {}".format(current_price.strip()[1:]))
            self.slack_messages("입력하신 종목의 연중 최고 가격: {}".format(high_for_the_year.strip()[1:]))
            self.slack_messages("입력하신 종목의 연중 최저 가격: {}".format(low_for_the_year.strip()[1:]))
            self.slack_messages("입력하신 종목의 거래량: {}".format(volume.strip()))

    def lookup_button_clicked_evt_hdr(self):
        print("this is lookup button clicked evt hdr")
        code = self.stock_code_edit.text()
        self.tr_res_edit.append("종목코드: " + code)

        # SetInputValue (Make Input Data)
        self.kiwoom.dynamicCall(
            *self.mk_str("set", ["종목코드", code]))

        # CommRqData (Send Transaction to Kiwoom OpenAPI+)
        self.kiwoom.dynamicCall(
            *self.mk_str("req", ["opt10001_req", "opt10001", 0, "0101"]))

    def mk_str(self, abb_func_name, func_args):
        if abb_func_name == "set":
            func_name = "SetInputValue"
        elif abb_func_name == "req":
            func_name = "CommRqData"
        elif abb_func_name == "get":
            func_name = "CommGetData"

        func_type_str = str()
        func_args_list = list()

        func_args_len = len(func_args)
        func_args_list.extend(func_args)

        func_type_str += '{func_name}('.format(func_name=func_name)
        for arg_idx, func_arg in enumerate(func_args):
            if isinstance(func_arg, str):
                func_type_str += 'QString'
            elif isinstance(func_arg, int):
                func_type_str += 'int'

            if arg_idx < func_args_len - 1:
                func_type_str += ', '
            else:
                func_type_str += ')'

        func_args_list.insert(0, func_type_str)

        print("func args list is {}".format(func_args_list))
        return func_args_list

    def event_exception(self, error_code):
        if error_code == 0:
            print("Login Success")
        elif error_code == 100:
            print("Failed User Inform transaction")
        elif error_code == 101:
            print("Failed Server Connection")
        elif error_code == 102:
            print("Failed Version Control")



if __name__ == "__main__":
    kiwoom_app = QApplication(sys.argv)
    kiwoom_window = KiwoomWindow()
    kiwoom_window.show()
    kiwoom_app.exec_()

#-*- coding:utf-8 -*-

import time
import schedule
import datetime
import logging
import argparse

import sys
from PyQt5.QtWidgets import QApplication, QLabel

# from HQ_bot.Slack.rssParse import *
from pprint import pformat, pprint

# for slacker
from slacker import Slacker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdlr = logging.FileHandler('system_trader.log')
hdlr.setLevel(logging.INFO)
logger.addHandler(hdlr)


class SystemTrader(object):
    def __init__(self):
        pass

    def init_trader(self):
        self.slack = Slacker(self.opt.token)
        self.slack_channel = self.opt.channel

    def parse_options(self):
        parser = argparse.ArgumentParser(
            description='''\
            Program for System Trading

              Example:
                  Execute Crawling
                       python trader_main.py -t xoxb-240213934096-877230619267-RhhlfWgo0n0aGohid9OK8UY6 -c #general
            ''', formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('-t', '--token',
                            dest="token", action="store",
                            metavar="Slack_Token",
                            default="xoxb-240213934096-877230619267-RhhlfWgo0n0aGohid9OK8UY6",
                            help="Slack Token ID")

        parser.add_argument('-c', '--channel',
                            dest="channel", action="store",
                            metavar="Slack_Channel",
                            default="#test",
                            help="Slack Channel ID")
        self.opt = parser.parse_args()

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

    def main(self, current_time):
        print("hello this is default test time is {}".format(current_time))

    def run(self):
        self.parse_options()
        self.init_trader()
        self.main(datetime.datetime.now())

        # schedule.every().day.at("14:30").do(self.main, datetime.datetime.now())

        # while True:
        #     schedule.run_pending()
        #     time.sleep(5)

        # for GUI
        print (github sync test)
        app = QApplication([])
        label = QLabel('Hello World!')
        label.show()
        app.exec_()

if __name__ == "__main__":
    system_trader = SystemTrader()
    system_trader.run()


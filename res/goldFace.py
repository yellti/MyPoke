import time
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from ui.gold import Ui_Form


from lib.pokeFun import PokeFun
from lib.appFun import AppFun
from lib.until import UntilFun


class GoldInterface(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setupUi(self)

        self.until = UntilFun()
        self.appFun = AppFun()

        self.gold_foot_start.clicked.connect(self.start_btn)
        self.gold_foot_end.clicked.connect(self.end_btn)
        self.gold_foot_end.setEnabled(False)
        self.updata_time = QTimer(self)

    def start_btn(self):
        print("start!!")
        start_time = time.time()

        self.gold_foot_start.setEnabled(False)
        self.gold_foot_end.setEnabled(True)
        # 定时
        self.updata_time.timeout.connect(lambda: self.update_time(start_time))
        self.updata_time.start(1000)

        self.start_init()

    def end_btn(self):
        self.gold_foot_start.setEnabled(True)
        self.gold_foot_end.setEnabled(False)
        self.updata_time.stop()

    def start_init(self):
        PokeFun()
        self.appFun.clear_gold_item()
        self.updata_page_item_num(0)
        self.updata_page_text()
        self.until.w_conf("poke", "gold_page_item", "times", "1")

    def updata_page_item_num(self, start_time):
        poke_conf = self.until.r_conf("poke")
        gold_num = int(poke_conf["gold_page_item"]["gold_num"])
        bead_num = poke_conf["gold_page_item"]["bead_num"]
        paw_num = poke_conf["gold_page_item"]["paw_num"]
        times_num = poke_conf["gold_page_item"]["times"]
        shine_num = poke_conf["gold_page_item"]["shine"]
        self.gold_foot_item_top_gold_num.setText(str(gold_num))
        self.gold_foot_item_top_paw_num.setText(paw_num)
        self.gold_foot_item_top_bead_num.setText(bead_num)
        self.gold_foot_item_bottom_times_num.setText(times_num)
        self.gold_foot_item_bottom_shine_num.setText(shine_num)
        speed = round(gold_num / ((time.time() - start_time) / 3600), 1)
        self.gold_foot_item_bottom_speed_num.setText("{}/h".format(speed))

    def updata_page_text(self):
        poke_str = self.until.r_log("poke")
        self.gold_text.setText(poke_str)
        self.gold_text.moveCursor(self.gold_text.textCursor().End)

    def update_time(self, start_time):
        current_time = time.time()
        use_time = current_time - start_time
        if int(use_time/3600) > 0:
            time_str = "{}小时{}分{}秒".format(int(use_time/3600), int(use_time % 3600/60), int(use_time % 60))
        else:
            time_str = "{}分{}秒".format(int(use_time % 3600 / 60), int(use_time % 60))
        self.gold_title_wrap_time.setText(time_str)

        poke_ini_last_change_time = os.path.getmtime("{}\\poke.ini".format(self.until.conf_path))
        poke_log_last_change_time = os.path.getmtime("{}\\poke.log".format(self.until.log_path))
        if (current_time - poke_ini_last_change_time) < 1:
            print("poke ini变了, 更新page")
            self.updata_page_item_num(start_time)
        if (current_time - poke_log_last_change_time) < 1:
            print("poke log变了, 更新page")
            self.updata_page_text()
            

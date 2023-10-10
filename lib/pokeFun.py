from lib.appFun import AppFun
from lib.dmFun import DmFun
from res.ui.gold import Ui_Form


class PokeFun(object):
    def __init__(self):
        self.dmFun = DmFun()
        self.dm = self.dmFun.dm
        self.appFun = AppFun()
        self.gold_page = Ui_Form()
        self.work_path = self.appFun.work_path
        self.res_path = "{}\\res".format(self.work_path)
        self.dm_path = "{}\\dm".format(self.res_path)
        self.img_path = "{}\\img".format(self.res_path)
        self.font_path = "{}\\font".format(self.res_path)

        # self.go_to_tree()
        # self.add_item_num("gold_num")

    def miaomiao(self):
        sweet_skill = self.dmFun.click_sweet_skill()

    def fight(self, x, y):
        # 点击战斗
        self.dm.MoveTo(230, 496)
        self.dmFun.d300()
        self.dm.LeftClick()
        self.dmFun.d300()
        # 点击小偷
        self.dm.MoveTo(230, 496)
        self.dmFun.d300()
        self.dm.LeftClick()
        self.dmFun.d300()
        # 点喵喵
        self.dm.MoveTo(x, y)
        self.dmFun.d300()
        self.dm.LeftClick()
        self.dmFun.d300()

    def what_item(self):
        item_name_path = "{}\\name.bmp".format(self.img_path)
        self.dm.MoveTo(440, 331)
        self.dmFun.d300()
        self.dm.LeftClick()
        self.dmFun.d300()
        self.dm.MoveTo(975, 280)
        self.dmFun.d300()
        self.dm.LeftClick()
        self.dmFun.d300()
        self.dmFun.cut_scerrn(801, 326, 951, 359, item_name_path)
        cut_tree_msg = self.appFun.ocr(item_name_path)
        self.dm.MoveTo(880, 344)
        self.dmFun.d300()
        self.dm.LeftClick()
        self.dmFun.d300()
        if cut_tree_msg == "取下护符金币":
            self.add_item_num("gold_num")
            print("护符金币")
        elif cut_tree_msg == "取下先制之爪":
            self.add_item_num("paw_num")
            print("先制之爪")
        else:
            self.add_item_num("bead_num")
            print("金珠")

    def add_item_num(self, key):
        poke_conf = self.appFun.r_conf("poke")
        num = int(poke_conf["gold_page_item"][key])
        num = str(num + 1)
        self.appFun.w_conf("poke", "gold_page_item", key, num)

    def whether_get_it(self):
        color1 = self.dm.FindColor(990, 278, 997, 282, "ececec-000000", 0.9, 0)[2]
        color2 = self.dm.FindColor(990, 280, 998, 285, "4faf18-000000", 0.9, 0)[2]
        color3 = self.dm.FindColor(990, 283, 998, 287, "9fb7be-000000", 0.9, 0)[2]
        if color1 == 1 or color2 == 1 or color3 == 1:
            print("偷到了")
            return True     # 偷到了
        else:
            print("没偷到")
            return False    # 没偷到

    def find_item(self):
        color1 = self.dm.FindColor(122, 423, 380, 438, "ce6c20-000000", 1.0, 0)[2]
        color2 = self.dm.FindColor(122, 423, 380, 438, "d27529-000000", 1.0, 0)[2]
        color3 = self.dm.FindColor(122, 423, 380, 438, "db863d-000000", 1.0, 0)[2]
        color4 = self.dm.FindColor(122, 423, 380, 438, "e59b52-000000", 1.0, 0)[2]
        color5 = self.dm.FindColor(122, 423, 380, 438, "f2b56f-000000", 1.0, 0)[2]
        if color1 == 1 or color2 == 1 or color3 == 1 or color4 == 1 or color5 == 1:
            self.appFun.w_log("poke", "发现物品！")
            return True
        else:
            return False

    def whether_miaomiao(self):
        name_img = "{}\\name.bmp".format(self.img_path)
        self.dmFun.cut_scerrn(145, 75, 187, 96, name_img)
        name = self.appFun.ocr(name_img)
        if name == "喵喵":
            self.appFun.w_log("poke", "遇见喵喵！")
            return True
        else:
            return False

    def cut_tree(self):
        img_path = "{}\\cut_tree.bmp".format(self.img_path)
        self.dm.KeyPress(32)
        self.dmFun.d500()
        for i in range(60):
            self.dmFun.cut_scerrn(246, 44, 495, 86, img_path)
            cut_tree_msg = self.appFun.ocr(img_path)
            if cut_tree_msg == "这棵树看上去能被砍掉":
                for n in range(60):
                    color1 = self.dm.FindColor(498, 406, 512, 430, "6e5747-000000", 0.8, 0)[2]
                    color2 = self.dm.FindColor(498, 406, 512, 430, "a57e47-000000", 0.8, 0)[2]
                    color3 = self.dm.FindColor(498, 406, 512, 430, "1f1f1f-000000", 0.9, 0)[2]
                    if color1 == 0 or color2 == 0 or color3 == 0:
                        break
                    else:
                        self.dm.KeyPress(32)
                        self.dmFun.d500()
                break
            else:
                self.dmFun.d1000()

    def go_to_tree(self):
        self.dmFun.click_bicycle_skill()
        self.dm.KeyPress(37)    # 左
        self.dmFun.d500()
        self.dm.KeyPress(37)
        self.dmFun.d500()
        self.dm.KeyPress(37)
        self.dmFun.d500()
        self.dm.KeyPress(37)
        self.dmFun.d500()
        self.dm.KeyPress(40)
        self.dmFun.d500()
        self.dm.KeyDown(40)    # 下
        self.dm.Delay(2000)
        self.dm.KeyUp(40)
        self.dmFun.d500()
        self.dm.KeyPress(39)  # 右
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(39)
        self.dmFun.d500()
        self.dm.KeyPress(40)
        self.dmFun.d500()

    def go_to_grass(self):
        self.dm.KeyDown(40)  # 下
        self.dm.Delay(3000)
        self.dm.KeyUp(40)

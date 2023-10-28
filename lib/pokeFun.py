from lib.dmFun import DM


class PokeFun(object):
    def __init__(self):
        self.DM = DM()
        self.dm = self.DM.dm
        self.until = self.DM.until

        self.poke_conf = self.until.r_conf("poke")

    def add_item_num(self, item, key):
        name = None
        if item == "gold":
            name = "gold_page_item"
        poke_conf = self.until.r_conf("poke")
        num = int(poke_conf[name][key])
        num = str(num + 1)
        self.until.w_conf("poke", name, key, num)

    def click_bicycle_skill(self):
        move_xy = self.poke_conf["position"]["bicycle"].split(",")
        self.dm.MoveTo(int(move_xy[0]), int(move_xy[1]))
        self.DM.d100()
        self.dm.LeftClick()
        self.DM.d500()

    def click_move_skill(self):
        move_xy = self.poke_conf["position"]["move"].split(",")
        self.dm.MoveTo(int(move_xy[0]), int(move_xy[1]))
        self.DM.d100()
        self.dm.LeftClick()
        self.DM.d1000()

    def whether_shine(self):
        color = self.dm.FindColor(58, 116, 900, 151, "fd0000-000000", 1.0, 0)[2]
        if color == 1:
            num = str(int(self.until.r_conf("poke")["gold_page_item"]["shine"]) + 1)
            self.until.w_log("poke", "**************闪了**************")
            self.until.w_conf("poke", "gold_page_item", "shine", num)
            return False
        else:
            return True


class PokeGoldFun(object):
    def __init__(self):
        self.pokeF = PokeFun()
        self.DM = self.pokeF.DM
        self.dm = self.pokeF.dm

        self.until = self.pokeF.until

        self.poke_conf = self.pokeF.poke_conf
        self.work_path = self.until.work_path
        self.res_path = "{}\\res".format(self.work_path)
        self.dm_path = "{}\\dm".format(self.res_path)
        self.img_path = "{}\\img".format(self.res_path)
        self.font_path = "{}\\font".format(self.res_path)

        # self.go_to_tree()
        # self.add_item_num("gold_num")

    def miaomiao(self):
        sweet_skill = self.click_sweet_skill()

    def fight(self, x, y):
        # 点击战斗
        self.dm.MoveTo(230, 496)
        self.DM.d300()
        self.dm.LeftClick()
        self.DM.d300()
        # 点击小偷
        self.dm.MoveTo(230, 496)
        self.DM.d300()
        self.dm.LeftClick()
        self.DM.d300()
        # 点喵喵
        self.dm.MoveTo(x, y)
        self.DM.d300()
        self.dm.LeftClick()
        self.DM.d300()

    def what_item(self):
        item_name_path = "{}\\name.bmp".format(self.img_path)
        self.dm.MoveTo(440, 331)
        self.DM.d300()
        self.dm.LeftClick()
        self.DM.d300()
        self.dm.MoveTo(975, 280)
        self.DM.d300()
        self.dm.LeftClick()
        self.DM.d300()
        self.DM.cut_scerrn(801, 326, 951, 359, item_name_path)
        cut_tree_msg = self.until.ocr(item_name_path)
        self.dm.MoveTo(880, 344)
        self.DM.d300()
        self.dm.LeftClick()
        self.DM.d300()
        if cut_tree_msg == "取下护符金币":
            self.pokeF.add_item_num("gold", "gold_num")
            print("护符金币")
        elif cut_tree_msg == "取下先制之爪":
            self.pokeF.add_item_num("gold", "paw_num")
            print("先制之爪")
        else:
            self.pokeF.add_item_num("gold", "bead_num")
            print("金珠")

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
            self.until.w_log("poke", "发现物品！")
            return True
        else:
            return False

    def whether_miaomiao(self):
        name_img = "{}\\name.bmp".format(self.img_path)
        self.DM.cut_scerrn(145, 75, 187, 96, name_img)
        name = self.until.ocr(name_img)
        if name == "喵喵":
            self.until.w_log("poke", "遇见喵喵！")
            return True
        else:
            return False

    def cut_tree(self):
        img_path = "{}\\cut_tree.bmp".format(self.img_path)
        self.dm.KeyPress(32)
        self.DM.d500()
        for i in range(60):
            self.DM.cut_scerrn(246, 44, 495, 86, img_path)
            cut_tree_msg = self.until.ocr(img_path)
            if cut_tree_msg == "这棵树看上去能被砍掉":
                for n in range(60):
                    color1 = self.dm.FindColor(498, 406, 512, 430, "6e5747-000000", 0.8, 0)[2]
                    color2 = self.dm.FindColor(498, 406, 512, 430, "a57e47-000000", 0.8, 0)[2]
                    color3 = self.dm.FindColor(498, 406, 512, 430, "1f1f1f-000000", 0.9, 0)[2]
                    if color1 == 0 or color2 == 0 or color3 == 0:
                        break
                    else:
                        self.dm.KeyPress(32)
                        self.DM.d500()
                break
            else:
                self.DM.d1000()

    def go_to_tree(self):
        self.pokeF.click_bicycle_skill()
        self.dm.KeyPress(37)    # 左
        self.DM.d500()
        self.dm.KeyPress(37)
        self.DM.d500()
        self.dm.KeyPress(37)
        self.DM.d500()
        self.dm.KeyPress(37)
        self.DM.d500()
        self.dm.KeyPress(40)
        self.DM.d500()
        self.dm.KeyDown(40)    # 下
        self.dm.Delay(2000)
        self.dm.KeyUp(40)
        self.DM.d500()
        self.dm.KeyPress(39)  # 右
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(39)
        self.DM.d500()
        self.dm.KeyPress(40)
        self.DM.d500()

    def go_to_grass(self):
        self.dm.KeyDown(40)  # 下
        self.dm.Delay(3000)
        self.dm.KeyUp(40)

    def whether_use_pp(self, x1, y1):
        self.dm.LeftClick()
        self.DM.d1000()
        self.dm.MoveTo(x1, y1)
        self.DM.d200()
        self.dm.LeftClick()
        self.DM.d200()

    def whether_monster_grass(self):
        """进草丛遇怪"""
        color1 = self.dm.FindColor(378, 65, 399, 88, "000000-000000", 1.0, 0)[2]
        color2 = self.dm.FindColor(910, 289, 922, 347, "000000-000000", 1.0, 0)[2]
        color3 = self.dm.FindColor(502, 602, 509, 609, "000000-000000", 1.0, 0)[2]
        if color1 == 1 and color2 == 1 and color3 == 1:
            fight_page = self.whether_fight_page()
            shine = self.pokeF.whether_shine()
            if fight_page and shine:
                self.click_escape()
                for i in range(60):
                    if self.whether_leave_fight():
                        self.until.w_log("poke", "进草丛遇怪已逃跑")
                        break
                    else:
                        self.DM.d1000()

    def whether_hospital_page(self):
        color1 = self.dm.FindColor(459, 116, 474, 132, "eee69f-000000", 0.9, 0)[2]
        color2 = self.dm.FindColor(301, 175, 330, 201, "f67f6f-000000", 0.9, 0)[2]
        color3 = self.dm.FindColor(520, 121, 555, 140, "4f4f67-000000", 0.9, 0)[2]
        num = int(self.until.r_conf("poke")["gold_page_item"]["times"]) + 1
        if color1 == 1 and color2 == 1 and color3 == 1:
            self.until.w_conf("poke", "gold_page_item", "times", num)
            return True
        else:
            return False

    def come_back_blood(self):
        img_path_blood = "{}\\come_back_blood.bmp".format(self.img_path)
        self.dm.KeyPress(32)
        self.DM.d1000()
        for i in range(120):
            self.DM.cut_scerrn(248, 45, 447, 87, img_path_blood)
            come_back_blood_msg = self.until.ocr(img_path_blood)
            if come_back_blood_msg == "希望能再次见到您":
                self.dm.KeyPress(32)
                color1 = self.dm.FindColor(715, 28, 758, 46, "000000-000000", 0.9, 0)[2]
                if color1 == 1:
                    self.until.w_log("poke", "加血")
                    break
            else:
                self.dm.KeyPress(32)
                self.DM.d500()

    def go_out_hospital(self):
        self.dm.KeyDown(40)
        self.dm.Delay(2000)
        self.dm.KeyUp(40)

    def whether_leave_hospital(self):
        for i in range(60):
            color1 = self.dm.FindColor(142, 429, 237, 449, "000000-000000", 1.0, 0)[2]
            color2 = self.dm.FindColor(692, 634, 740, 671, "000000-000000", 1.0, 0)[2]
            color3 = self.dm.FindColor(454, 619, 526, 668, "000000-000000", 1.0, 0)[2]
            if color1 == 0 and color2 == 0 and color3 == 0:
                break
            else:
                self.DM.d500()

    def click_sweet_skill(self):
        # True 战斗   False 加血
        sweet_xy = self.poke_conf["position"]["sweet"].split(",")
        img_path_top = "{}\\after_sweet_top.bmp".format(self.img_path)
        img_path_betton = "{}\\after_sweet_betton.bmp".format(self.img_path)
        self.dm.MoveTo(int(sweet_xy[0]), int(sweet_xy[1]))
        self.DM.d100()
        self.dm.LeftClick()
        self.DM.d1000()
        self.DM.cut_scerrn(501, 42, 659, 87, img_path_top)
        self.DM.cut_scerrn(447, 625, 552, 650, img_path_betton)
        after_sweet_top_msg = self.until.ocr(img_path_top)
        after_sweet_betton_msg = self.until.ocr(img_path_betton)
        if after_sweet_top_msg or after_sweet_betton_msg:
            if after_sweet_top_msg:
                pp = self.poke_conf["custom"]["pp"]
                if pp == "True":
                    self.whether_use_pp(505, 390)
                    self.until.w_log("poke", "使用pp果！")
                    return True
                else:
                    self.until.w_log("poke", "回医院！")
                    self.whether_use_pp(505, 530)
                    return False
            if after_sweet_betton_msg:
                self.until.w_log("poke", "回医院！")
                return False
        else:
            return True

    def whether_fight_page(self):
        img_bag = "{}\\bag.bmp".format(self.img_path)
        res = False
        for i in range(60):
            self.DM.cut_scerrn(427, 539, 463, 556, img_bag)
            img_bag_msg = self.until.ocr(img_bag)
            if img_bag_msg == "逃跑":
                res = True
                break
            self.dm.Delay(1000)
        return res

    def click_escape(self):
        self.dm.MoveTo(450, 550)
        self.DM.d200()
        self.dm.LeftClick()
        self.DM.d1000()

    def whether_leave_fight(self):
        color1 = self.dm.FindColor(195, 124, 206, 134, "a0f8b0-000000", 1.0, 0)[2]
        color2 = self.dm.FindColor(628, 613, 687, 636, "000000-000000", 1.0, 0)[2]
        color3 = self.dm.FindColor(58, 223, 86, 332, "000000-000000", 1.0, 0)[2]
        color4 = self.dm.FindColor(272, 610, 363, 634, "000000-000000", 1.0, 0)[2]
        color5 = self.dm.FindColor(161, 153, 192, 190, "000000-000000", 1.0, 0)[2]
        if color1 == 1 and color2 == 1 and color3 == 1 and color4 == 1 and color5 == 1:
            return False
        else:
            return True

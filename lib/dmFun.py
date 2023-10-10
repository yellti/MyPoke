from lib.appFun import AppFun
import ctypes
import os
from lib.appFun import AppFun
from comtypes.client import CreateObject
from win32com.client import Dispatch


class DmFun(object):
    def __init__(self):
        self.appFun = AppFun()
        self.dm_conf = self.appFun.r_conf("dm")
        self.poke_conf = self.appFun.r_conf("poke")
        self.work_path = self.appFun.work_path
        self.res_path = "{}\\res".format(self.work_path)
        self.dm_path = "{}\\dm".format(self.res_path)
        self.img_path = "{}\\img".format(self.res_path)
        self.font_path = "{}\\font".format(self.res_path)

        self.dm = self.init()

    def init(self):
        dm = self.reg_dm()
        hwnd = self.bind_window(dm)
        win_size = self.set_window_size(dm, hwnd)
        if dm and hwnd and win_size:
            self.appFun.w_log("app", "窗口初始化完成！")
            return dm
        else:
            self.appFun.w_log("error", "窗口初始化失败！")
            return False

    def __reg_dm_to_sys(self):
        try:
            dm = Dispatch("dm.dmsoft")
            self.appFun.w_log("app", "注册调用大漠插件 版本号：{}".format(dm.ver()))
            return dm
        except:
            dm_reg_dll_path = "{}\\DmReg.dll".format(self.dm_path)
            dm_dll_path = "{}\\dm.dll".format(self.dm_path)
            dms = ctypes.windll.LoadLibrary(dm_reg_dll_path)
            dms.SetDllPathW(dm_dll_path, 0)
            dm = CreateObject('dm.dmsoft')
            self.appFun.w_log("app", "免注册调用大漠插件 版本号：{}".format(dm.ver()))
            return dm

    def reg_dm(self):
        """收费注册"""
        dm = self.__reg_dm_to_sys()
        dm_vip = dm.Reg(self.dm_conf["dm"]["reg_code"], self.dm_conf["dm"]["ver_info"])
        if dm_vip == 1:
            print("收费注册成功，返回值：{}, 版本号：{}".format(dm_vip, dm.ver()))
            self.appFun.w_log("app", "收费注册成功，返回值：{}".format(dm_vip))
            return dm
        else:
            re_msg = self.dm_conf["info"][str(dm_vip)]
            print("收费注册失败，返回值：{}, 版本号：{} {}".format(dm_vip, dm.ver(), re_msg))
            self.appFun.w_log("app", "收费注册返回值：{} {}".format(dm_vip, re_msg))
            return False

    def bind_window(self, dm):
        """绑定窗口"""
        hwnd = dm.FindWindow("GLFW30", "")
        bind = dm.BindWindowEx(hwnd, "gdi2", "windows",
                               "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api|dx.keypad.raw.input",
                               "dx.public.fake.window.min|dx.public.active.api2|dx.public.disable.window.show", 0)
        if hwnd and bind:
            if bind != 1:
                print("窗口：{} 绑定失败，返回值：{}".format(hwnd, bind))
                self.appFun.w_log("error", "窗口：{} 绑定失败，返回值：{}".format(hwnd, bind))
                return False
            else:
                print("窗口：{} 绑定成功，返回值：{}".format(hwnd, bind))
                self.appFun.w_log("app", "窗口：{} 绑定成功，返回值：{}".format(hwnd, bind))
                return hwnd
        else:
            self.appFun.w_log("error", "窗口：{} 绑定失败，返回值：{}".format(hwnd, bind))
            return False

    def set_window_size(self, dm, hwnd):
        """设置窗口大小"""
        window_width = self.poke_conf["window"]["width"]
        window_height = self.poke_conf["window"]["height"]
        if hwnd:
            dm.SetWindowSize(hwnd, int(window_width), int(window_height))
            return True
        else:
            return False

    def cut_scerrn(self, x1, y1, x2, y2, img_path):
        """截屏"""
        screen_msg = self.dm.Capture(x1, y1, x2, y2, img_path)
        if screen_msg:
            return True
        else:
            self.appFun.w_log("error", "截屏错误：\"{}\"".format(img_path))
            return False

    def d100(self):
        self.dm.Delay(100)

    def d200(self):
        self.dm.Delay(200)

    def d300(self):
        self.dm.Delay(300)

    def d500(self):
        self.dm.Delay(500)

    def d1000(self):
        self.dm.Delay(1000)

    def whether_use_pp(self, x1, y1):
        self.dm.LeftClick()
        self.d1000()
        self.dm.MoveTo(x1, y1)
        self.d200()
        self.dm.LeftClick()
        self.d200()

    def whether_monster_grass(self):
        """进草丛遇怪"""
        color1 = self.dm.FindColor(378, 65, 399, 88, "000000-000000", 1.0, 0)[2]
        color2 = self.dm.FindColor(910, 289, 922, 347, "000000-000000", 1.0, 0)[2]
        color3 = self.dm.FindColor(502, 602, 509, 609, "000000-000000", 1.0, 0)[2]
        if color1 == 1 and color2 == 1 and color3 == 1:
            fight_page = self.whether_fight_page()
            shine = self.whether_shine()
            if fight_page and shine:
                self.click_escape()
                for i in range(60):
                    if self.whether_leave_fight():
                        self.appFun.w_log("poke", "进草丛遇怪已逃跑")
                        break
                    else:
                        self.d1000()

    def click_bicycle_skill(self):
        move_xy = self.poke_conf["position"]["bicycle"].split(",")
        self.dm.MoveTo(int(move_xy[0]), int(move_xy[1]))
        self.d100()
        self.dm.LeftClick()
        self.d500()

    def click_move_skill(self):
        move_xy = self.poke_conf["position"]["move"].split(",")
        self.dm.MoveTo(int(move_xy[0]), int(move_xy[1]))
        self.d100()
        self.dm.LeftClick()
        self.d1000()

    def whether_hospital_page(self):
        color1 = self.dm.FindColor(459, 116, 474, 132, "eee69f-000000", 0.9, 0)[2]
        color2 = self.dm.FindColor(301, 175, 330, 201, "f67f6f-000000", 0.9, 0)[2]
        color3 = self.dm.FindColor(520, 121, 555, 140, "4f4f67-000000", 0.9, 0)[2]
        num = int(self.appFun.r_conf("poke")["gold_page_item"]["times"]) + 1
        if color1 == 1 and color2 == 1 and color3 == 1:
            self.appFun.w_conf("poke", "gold_page_item", "times", num)
            return True
        else:
            return False

    def come_back_blood(self):
        img_path_blood = "{}\\come_back_blood.bmp".format(self.img_path)
        self.dm.KeyPress(32)
        self.d1000()
        for i in range(120):
            self.cut_scerrn(248, 45, 447, 87, img_path_blood)
            come_back_blood_msg = self.appFun.ocr(img_path_blood)
            if come_back_blood_msg == "希望能再次见到您":
                self.dm.KeyPress(32)
                color1 = self.dm.FindColor(715, 28, 758, 46, "000000-000000", 0.9, 0)[2]
                if color1 == 1:
                    self.appFun.w_log("poke", "加血")
                    break
            else:
                self.dm.KeyPress(32)
                self.d500()

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
                self.d500()

    def click_sweet_skill(self):
        # True 战斗   False 加血
        sweet_xy = self.poke_conf["position"]["sweet"].split(",")
        img_path_top = "{}\\after_sweet_top.bmp".format(self.img_path)
        img_path_betton = "{}\\after_sweet_betton.bmp".format(self.img_path)
        self.dm.MoveTo(int(sweet_xy[0]), int(sweet_xy[1]))
        self.d100()
        self.dm.LeftClick()
        self.d1000()
        self.cut_scerrn(501, 42, 659, 87, img_path_top)
        self.cut_scerrn(447, 625, 552, 650, img_path_betton)
        after_sweet_top_msg = self.appFun.ocr(img_path_top)
        after_sweet_betton_msg = self.appFun.ocr(img_path_betton)
        if after_sweet_top_msg or after_sweet_betton_msg:
            if after_sweet_top_msg:
                pp = self.poke_conf["custom"]["pp"]
                if pp == "True":
                    self.whether_use_pp(505, 390)
                    self.appFun.w_log("poke", "使用pp果！")
                    return True
                else:
                    self.appFun.w_log("poke", "回医院！")
                    self.whether_use_pp(505, 530)
                    return False
            if after_sweet_betton_msg:
                self.appFun.w_log("poke", "回医院！")
                return False
        else:
            return True

    def whether_fight_page(self):
        img_bag = "{}\\bag.bmp".format(self.img_path)
        res = False
        for i in range(60):
            self.cut_scerrn(427,539,463,556, img_bag)
            img_bag_msg = self.appFun.ocr(img_bag)
            if img_bag_msg == "逃跑":
                res = True
                break
            self.dm.Delay(1000)
        return res

    def click_escape(self):
        self.dm.MoveTo(450, 550)
        self.d200()
        self.dm.LeftClick()
        self.d1000()

    def whether_leave_fight(self):
        color1 = self.dm.FindColor(195,124,206,134, "a0f8b0-000000", 1.0, 0)[2]
        color2 = self.dm.FindColor(628, 613, 687, 636, "000000-000000", 1.0, 0)[2]
        color3 = self.dm.FindColor(58, 223, 86, 332, "000000-000000", 1.0, 0)[2]
        color4 = self.dm.FindColor(272, 610, 363, 634, "000000-000000", 1.0, 0)[2]
        color5 = self.dm.FindColor(161, 153, 192, 190, "000000-000000", 1.0, 0)[2]
        if color1 == 1 and color2 == 1 and color3 == 1 and color4 == 1 and color5 == 1:
            return False
        else:
            return True

    def whether_shine(self):
        color = self.dm.FindColor(58, 116, 900, 151, "fd0000-000000", 1.0, 0)[2]
        if color == 1:
            num = str(int(self.appFun.r_conf("poke")["gold_page_item"]["shine"]) + 1)
            self.appFun.w_log("poke", "**************闪了**************")
            self.appFun.w_conf("poke", "gold_page_item", "shine", num)
            return False
        else:
            return True













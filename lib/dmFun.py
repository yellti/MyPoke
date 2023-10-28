import ctypes
from lib.until import UntilFun
from comtypes.client import CreateObject
from win32com.client import Dispatch


class DM(object):
    def __init__(self):
        dm_win = SetWindow()
        self.dm = dm_win.init()

        self.until = dm_win.until
        self.dm_conf = self.until.r_conf("dm")
        self.poke_conf = self.until.r_conf("poke")

        self.work_path = self.until.work_path
        self.res_path = "{}\\res".format(self.work_path)
        self.dm_path = "{}\\dm".format(self.res_path)
        self.img_path = "{}\\img".format(self.res_path)
        self.font_path = "{}\\font".format(self.res_path)

    def cut_scerrn(self, x1, y1, x2, y2, img_path):
        """截屏"""
        screen_msg = self.dm.Capture(x1, y1, x2, y2, img_path)
        if screen_msg:
            return True
        else:
            self.until.w_log("error", "截屏错误：\"{}\"".format(img_path))
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


class SetWindow(object):
    def __init__(self):
        self.until = UntilFun()

        self.dm_conf = self.until.r_conf("dm")
        self.poke_conf = self.until.r_conf("poke")

        self.work_path = self.until.work_path
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
            self.until.w_log("app", "窗口初始化完成！")
            return dm
        else:
            self.until.w_log("error", "窗口初始化失败！")
            return False

    def __reg_dm_to_sys(self):
        try:
            dm = Dispatch("dm.dmsoft")
            self.until.w_log("app", "注册调用大漠插件 版本号：{}".format(dm.ver()))
            return dm
        except:
            dm_reg_dll_path = "{}\\DmReg.dll".format(self.dm_path)
            dm_dll_path = "{}\\dm.dll".format(self.dm_path)
            dms = ctypes.windll.LoadLibrary(dm_reg_dll_path)
            dms.SetDllPathW(dm_dll_path, 0)
            dm = CreateObject('dm.dmsoft')
            self.until.w_log("app", "免注册调用大漠插件 版本号：{}".format(dm.ver()))
            return dm

    def reg_dm(self):
        """收费注册"""
        dm = self.__reg_dm_to_sys()
        dm_vip = dm.Reg(self.dm_conf["dm"]["reg_code"], self.dm_conf["dm"]["ver_info"])
        if dm_vip == 1:
            print("收费注册成功，返回值：{}, 版本号：{}".format(dm_vip, dm.ver()))
            self.until.w_log("app", "收费注册成功，返回值：{}".format(dm_vip))
            return dm
        else:
            re_msg = self.dm_conf["info"][str(dm_vip)]
            print("收费注册失败，返回值：{}, 版本号：{} {}".format(dm_vip, dm.ver(), re_msg))
            self.until.w_log("app", "收费注册返回值：{} {}".format(dm_vip, re_msg))
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
                self.until.w_log("error", "窗口：{} 绑定失败，返回值：{}".format(hwnd, bind))
                return False
            else:
                print("窗口：{} 绑定成功，返回值：{}".format(hwnd, bind))
                self.until.w_log("app", "窗口：{} 绑定成功，返回值：{}".format(hwnd, bind))
                return hwnd
        else:
            self.until.w_log("error", "窗口：{} 绑定失败，返回值：{}".format(hwnd, bind))
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

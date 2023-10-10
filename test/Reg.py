import os
import win32com.client
from .RWconfig import PokeConfig


class PokeReg(object):
    def __init__(self):
        self.Rconfig = PokeConfig
        self.config = self.Rconfig().r_config()
        self.registration_code = self.config["damo"]["registration_code"]
        self.additional_code = self.config["damo"]["additional_code"]
        self.work_path = self.config["init"]["work_path"]
        self.window_width = self.config["window"]["window_width"]
        self.window_height = self.config["window"]["window_height"]

    @staticmethod
    def bind_hwnd(dm):
        hwnd = dm.FindWindow("GLFW30", "")
        bind = dm.BindWindowEx(hwnd, "gdi2", "windows",
                               "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api|dx.keypad.raw.input",
                               "dx.public.fake.window.min|dx.public.active.api2|dx.public.disable.window.show", 0)
        return hwnd, bind

    def set_path(self, dm):
        dm.SetPath(self.work_path)
        dm.SetDict(0, "res\\font\\Font.txt")
        dm.UseDict(0)

    def reg_dm_to_sys(self):
        try:
            dm_1 = win32com.client.Dispatch('dm.dmsoft')
        except Exception:
            os.system(r'regsvr32 /s %s\dm.dll' % "{}\\res\\plugins".format(self.work_path))
            dm_1 = win32com.client.Dispatch('dm.dmsoft')
        return dm_1

    def set_window_size(self, dm, hwnd):
        dm.SetWindowSize(hwnd, int(self.window_width), int(self.window_height))

    def get_dm_obj(self):
        if not self.reg_dm_to_sys():
            # ToDo 添加注册错误日志
            return False
        dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件,获取大漠对象
        dm_vip = dm.Reg(self.registration_code, self.additional_code)
        self.set_path(dm)
        if dm_vip != 1:
            # ToDo 添加注册错误日志
            print(f'收费注册失败，返回值：{dm_vip}，版本号：{dm.ver()}')
            return False
        else:
            print(f'收费注册成功，返回值：{dm_vip}，版本号：{dm.ver()}')
        hwnd, bind = self.bind_hwnd(dm)
        if hwnd and bind:
            if bind != 1:
                # ToDo 添加注册错误日志
                print(f'窗口:{hwnd}绑定失败，返回值：{bind}')
                return False
            else:
                print(f'窗口:{hwnd}绑定成功，返回值：{bind}')
                self.set_window_size(dm, hwnd)
        return dm, hwnd

    def run(self):
        self.get_dm_obj()


if __name__ == "__main__":
    reg = PokeReg()
    reg.run()

from .ocr import OCR
from .RWconfig import PokeConfig

class DmFun(object):
    def __init__(self, dm):
        self.dm = dm

        self.OCR = OCR

        self.poke_config = PokeConfig
        self.config = self.poke_config().r_config()
        self.work_path = self.config["init"]["work_path"]
        self.screen_path = self.config["init"]["screen_path"]

    def cut_screen(self, x1, y1, x2, y2):
        dm_ret = self.dm.Capture(x1, y1, x2, y2, "{}\\1.bmp".format(self.screen_path))
        if not dm_ret:
            # ToDo 添加注册错误日志
            return False

    def ocr_img(self):
        str_res = self.OCR().get_ocr()
        return str_res

    def run(self):
        pass


if __name__ == "__main__":
    dm_fun = DmFun()
    dm_fun.run()

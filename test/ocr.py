from rapidocr_onnxruntime import RapidOCR
from .RWconfig import PokeConfig
import time


class OCR(object):
    def __init__(self):
        self.Rconfig = PokeConfig
        self.screen_path = self.Rconfig().r_config()["init"]["screen_path"]
        self.img_path = "{}\\1.bmp".format(self.screen_path)

    def ocr_ing(self):
        rapid_ocr = RapidOCR()
        result, elapse = rapid_ocr(self.img_path)
        if result:
            return result
        else:
            return False

    def get_ocr(self):
        start_time = time.time()
        res = self.ocr_ing()
        if res:
            res = res[0][1]
            end_time = time.time()
            user_time = round(end_time - start_time, 2)
            return res
        else:
            # TODO 失败原因
            return False

# class OCR(object):
#     def __init__(self):
#         self.Rconfig = PokeConfig
#         self.img_path = self.Rconfig().r_config()["init"]["screen_path"]
#         self.img_file_path = "{}\\1.bmp".format(self.img_path)
#
#     def get_ocr(self):
#         start_time = time.time()
#         rapid_ocr = RapidOCR()
#         res = []
#         result, elapse = rapid_ocr(self.img_file_path)
#         if not result:
#             # ToDo 添加注册错误日志
#             print("没找到字体")
#             return False
#         end_time = time.time()
#         user_time = round(end_time - start_time, 2)
#         str_res = result[0][1]
#         res[0] = str_res
#         res[1] = user_time
#         return res
#
    def run(self):
        self.get_ocr()


if __name__ == "__main__":
    poke_OCR = OCR()
    poke_OCR.run()

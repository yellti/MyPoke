import configparser
import os
import time

from rapidocr_onnxruntime import RapidOCR


class UntilFun(object):
    def __init__(self):
        # configparser
        self.conf = configparser.ConfigParser()
        # ocr
        self.rapid_ocr = RapidOCR()

        # set path
        self.work_path = self.get_work_path()
        self.conf_path = "{}\\conf".format(self.work_path)
        self.log_path = "{}\\log".format(self.work_path)

    @staticmethod
    def get_work_path():
        path = os.getcwd()
        work_path = "\\".join(path.split("\\")[:-1])
        return work_path

# configparser
    def r_conf(self, file_name):
        res = {}
        file_path = "{}\\{}.ini".format(self.conf_path, file_name)
        self.conf.clear()
        self.conf.read(file_path, encoding='utf-8')
        sections = self.conf.sections()
        if not sections == "[]":
            for section in sections:
                res[section] = {}
                option = self.conf.items(section)
                if option:
                    for item in option:
                        key = item[0]
                        value = item[1]
                        res[section][key] = value
        return res

    def w_conf(self, file_name, section, key, value):
        file_path = "{}\\{}.ini".format(self.conf_path, file_name)
        self.conf.clear()
        self.conf.read(file_path, encoding='utf-8')
        sections = self.conf.sections()
        if not (section in sections):
            self.conf.add_section(section)
        value_str = str(value)
        self.conf.set(section, key, value_str)
        with open(file_path, 'w') as f:
            self.conf.write(f)

# logging
    def w_log(self, file_name, str_con, mode="a"):
        """"向指定log文件中写信息"""
        date_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        file_path = "{}\\{}.log".format(self.log_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, mode) as wf:
                wf.writelines("{}\t\t{}\n".format(date_time, str_con))
        else:
            with open("{}\\error.log".format(self.log_path), "a") as wf:
                wf.writelines("{}\t\terror: No file {}\t\"{}\"\n".format(date_time, file_path, str_con))

    def r_log(self, file_name):
        file_path = "{}\\{}.log".format(self.log_path, file_name)
        with open(file_path, "r", encoding="utf-8") as rf:
            poke_log_str = rf.read()
        return poke_log_str

# ORC
    def ocr(self, img_path):
        img_msg, elapse = self.rapid_ocr(img_path)
        if img_msg:
            res = img_msg[0][1]
            return res
        else:
            self.w_log("error", "ocr失败！ \"{}\"".format(img_path))
            return False

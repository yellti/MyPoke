from lib.dmFun import DmFun
from lib.appFun import AppFun
from rapidocr_onnxruntime import RapidOCR

# dmFun = DmFun()
#
# dmFun.bind_window(dmFun.reg_dm())


import os

w = os.getcwd()

a = "\\".join(w.split("\\")[:-1])

print(a)

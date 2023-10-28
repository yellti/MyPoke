from lib.until import UntilFun


class AppFun(object):
    def __init__(self):
        self.until = UntilFun()

        self.work_path = self.until.work_path
        self.conf_path = self.until.conf_path
        self.log_path = self.until.log_path

# setNum
    def clear_gold_item(self):
        poke_conf = self.until.r_conf("poke")
        keys = poke_conf["gold_page_item"].keys()
        for name in keys:
            self.until.w_conf("poke", "gold_page_item", name, 0)
        with open("{}\\poke.log".format(self.log_path), "a+", encoding="utf-8") as wf:
            wf.truncate(0)
            

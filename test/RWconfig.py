import configparser
import os


class PokeConfig(object):
    def __init__(self):
        self.work_path = self.get_work_path()
        self.init_file_path = "{}\\res\\init.txt".format(self.work_path)
        self.config = self.init_config()
        self.set_path()

    def set_path(self):
        self.w_config("init", "work_path", self.work_path)
        self.w_config("init", "init_file_path", self.init_file_path)
        self.w_config("init", "screen_path", "{}\\res\\screenshot".format(self.work_path))

    def w_config(self, section, key, value):
        config = self.config
        sections = config.sections()
        if not (section in sections):
            config.add_section(section)
        config.set(section, key, value)
        with open(self.init_file_path, 'w') as f:
            config.write(f)

    def r_config(self):
        config = self.config
        res = {}
        sections = config.sections()
        for section in sections:
            res[section] = {}
            option = config.items(section)
            if option:
                for item in option:
                    key = item[0]
                    value = item[1]
                    res[section][key] = value
        return res

    @staticmethod
    def get_work_path():
        work_path = os.getcwd()
        return work_path

    def init_config(self):
        conf = configparser.ConfigParser()
        conf.read(self.init_file_path)
        return conf

    def run(self):
        config = self.config


if __name__ == "__main__":
    init_config = PokeConfig()
    init_config.run()

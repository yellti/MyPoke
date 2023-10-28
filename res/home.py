import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import SplitFluentWindow, FluentIcon, NavigationAvatarWidget, NavigationItemPosition
from goldFace import GoldInterface


class Demo(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PokeMoMo")
        self.setMaximumSize(720, 620)
        self.setMinimumSize(560, 400)
        self.setWindowIcon(QIcon("./img/pokeball_b.png"))
        self.focusInterface = GoldInterface(self)
        self.addSubInterface(self.focusInterface, FluentIcon.ROBOT, "护符金币")

        self.navigationInterface.addItem(
            routeKey='setting',
            icon=FluentIcon.SETTING,
            text='设置',
            position=NavigationItemPosition.BOTTOM
        )


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()

import hashlib
import sys
import os
import string

import ui.MainWindow
import ui.Setting
import ui.About
import ui.SuperSetting
from PyQt5 import QtCore, QtGui, QtWidgets

class MyMainWindow(QtWidgets.QMainWindow):
    setting = {'window': "3"}
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.setting['window'] != "2":
            self.setWindowOpacity(1)
        super().enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.setting['window'] in ("2", "3"):
            self.setWindowOpacity(0.3)
        super().leaveEvent(a0)

def get_setting():
    with open('sjch.setting', encoding='utf-8') as file:
        s = file.readlines()
    setting = {}
    for i in s:
        if i.strip().startswith('#') or (not i.strip()):
            continue
        l, r = i.strip().split('=')
        setting[l] = r
    setting['out'] = list([int(i) for i in setting['out'].split(',')]) if setting['out'] else []
    left = list(range(1, int(setting['max'])+1))
    for i in setting['out']:
        if i in left:
            left.remove(i)
    setting['left'] = left
    return setting

def save_setting(setting):
    setting = setting.copy()
    setting['out'] = ','.join([str(i) for i in setting['out']])
    s = []
    for k in setting:
        if k == 'left':
            continue
        v = setting[k]
        s.append('='.join([k, v]))
    s = '\n'.join(s)
    with open('sjch.setting', 'w', encoding='utf-8') as file:
        file.write(s)

def check_setting():
    default = {
        "max": "65",
        "animation": "Open",
        "window": "3",
        "pwd-md5": hashlib.md5('000000'.encode('utf-8')).hexdigest(),
        "put-back": "2",
        "out": []
    }
    try:
        setting = get_setting()
    except FileNotFoundError:
        save_setting(default)
        return
    for k in default:
        setting[k] = setting.get(k, default[k])
    save_setting(setting)

def open_setting(mainwindow, setting):
    settingwindow = QtWidgets.QMainWindow()
    settingui = ui.Setting.Ui_MainWindow()
    settingui.setupUi(settingwindow, setting, open_about, None, save_setting)
    settingui.setting_to_ui()
    settingwindow.show()

def open_about(mainwindow):
    aboutwindow = QtWidgets.QMainWindow()
    aboutui = ui.About.Ui_MainWindow()
    aboutui.setupUi(aboutwindow)
    aboutwindow.show()

def main():
    check_setting()
    setting = get_setting()
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MyMainWindow()
    mainui = ui.MainWindow.Ui_MainWindow()
    mainui.setupUi(mainwindow, setting, app, open_setting, save_setting)
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # pass

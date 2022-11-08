from mainui import Ui_MainWindow
from func import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import * 
import sys
import json
class WindowGui(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(WindowGui,self).__init__()

        self.setupUi(self)
        self.qsettings = QSettings("config.ini")
        #涂鸦
        self.tuya_check.setChecked(self.qsettings.value('tuyaCheckState',type=bool))
        self.tuya_choice.setCurrentIndex(self.qsettings.value('tuyaChoice',type=int))
        self.tuya_dif.setCurrentIndex(self.qsettings.value('tuyaDif',type=int))
        self.tuya_times.setText(self.qsettings.value('tuyaTimes'))
        #钓鱼
        self.fishing_check.setChecked(self.qsettings.value('fishingCheckState',type=bool))
        self.fishing_point.setCurrentIndex(self.qsettings.value('fishingPoint',type=int))
        self.fishing_times.setText(self.qsettings.value('fishingTimes'))

        self.data = None
        self.load_data.clicked.connect(self.loadData)
        self.save.clicked.connect(self.saveSettings)
        self.confirm.clicked.connect(self.taskConfirm)
    def saveSettings(self):
        self.qsettings.setValue('tuyaCheckState', self.tuya_check.isChecked())
        self.qsettings.setValue('fishingCheckState', self.tuya_check.isChecked())

        self.qsettings.setValue("tuyaChoice",self.tuya_choice.currentIndex())
        self.qsettings.setValue("tuyaDif",self.tuya_dif.currentIndex())
        self.qsettings.setValue("tuyaTimes",self.tuya_times.text())

        self.qsettings.setValue("fishingPoint",self.fishing_point.currentIndex())
        self.qsettings.setValue("fishingTimes",self.fishing_times.text())

    def taskConfirm(self):
        if self.tuya_check.isChecked():
            tya = tuya(self.tuya_choice.currentIndex(),self.tuya_dif.currentIndex(),int(self.tuya_times.text()))
            tya.stuya()
        if self.fishing_check.isChecked():
            diaoyu = fishing(int(self.fishing_times.text()),self.fishing_point.currentIndex())
            diaoyu.fishing()

            tya = tuya(self.tuya_choice.currentIndex(),self.tuya_dif.currentIndex(),int(self.tuya_times.text()),self.data)
            tya.stuya()
        if self.fishing_check.isChecked():
            diaoyu = fishing(int(self.fishing_times.text()),self.fishing_point.currentIndex(),self.data)
            diaoyu.fishing()

    def loadData(self):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except:
            raise FileExistsError('配置文件不存在')
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = WindowGui()
    window.show() 
    sys.exit(app.exec()) 

from io import BytesIO
import time
from PIL import Image
import win32api ,win32con, win32gui, win32ui
import ddddocr
import cv2 as cv
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import * 
class util:
    def __init__(self):
        self.ocr = ddddocr.DdddOcr()
        hwnd = win32gui.FindWindow(None,"ld")
        self.hwnd = win32gui.FindWindowEx(hwnd,None,None,None)
        x_1, y_1, x_2, y_2 = win32gui.GetWindowRect(hwnd)
        self.width = x_2 - x_1
        self.height = y_2 - y_1

    def cvRead(self,img_path):
        return cv.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)

    def mouseDown(self,x:int, y:int):
        press_pos = win32api.MAKELONG(x,y)
        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, press_pos)

    def mouseUp(self,x:int, y:int):
        press_pos = win32api.MAKELONG(x,y)
        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON, press_pos)

    def mouseClick(self,x:int, y:int):
        press_pos = win32api.MAKELONG(x,y)
        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, press_pos)
        time.sleep(0.2)
        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,None, press_pos)

    def doubleClick(self,x:int, y:int):
        self.mouseClick(x, y)
        time.sleep(0.1)
        self.mouseClick(x, y)

    def swipeDown(self):
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYDOWN,win32con.VK_SPACE,0)
        time.sleep(1.2)
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYUP,win32con.VK_SPACE,0)

    def swipeLeft(self):
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYDOWN,win32con.VK_CONTROL,0)
        time.sleep(1.1)
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYUP,win32con.VK_CONTROL,0)

    def capWindow(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height), dcObj, (0, 0), win32con.SRCCOPY)
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(bmpstr, dtype='uint8')
        img.shape = (self.height,self.width, 4)
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return img

    def capWindowPos(self, x:int, y:int, x1:int, y1:int):
        w = x1 - x
        h = y1 - y
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x,y), win32con.SRCCOPY)
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(bmpstr, dtype='uint8')
        img.shape = (h, w, 4)
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return img

    def OCR(self,x,y,x1,y1):
        w = x1 - x
        h = y1 - y
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x,y), win32con.SRCCOPY)
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        img_byte = BytesIO()  
        img.save(img_byte, format='PNG')
        img_info = img_byte.getvalue()
        result = self.ocr.classification(img_info)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return result

    def clickPic(self,tmp:str, threshold:float):
        _scr = self.capWindow()
        _tp = self.cvRead(tmp)
        tp = cv.cuda_GpuMat(_tp)
        scr = cv.cuda_GpuMat(_scr)
        matcher = cv.cuda.createTemplateMatching(cv.CV_8UC1, cv.TM_CCORR_NORMED)
        result = matcher.match(scr, tp)
        result = result.download()
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val < threshold:
            print(tmp, max_val, max_loc)
            return False
        #print(tmp, max_val, max_loc)
        self.mouseDown(int(max_loc[0]) + int(_tp.shape[1]/2), int(max_loc[1]) + int(_tp.shape[0]/2))
        time.sleep(0.5)
        self.mouseUp(int(max_loc[0]) + int(_tp.shape[1]/2), int(max_loc[1]) + int(_tp.shape[0]/2))
        return True
        
    def findPic(self, x:int, y:int, x1:int, y1:int, tmp:str, threshold:float):
        scr = self.capWindowPos(x,y,x1,y1)
        tp = self.cvRead(tmp)
        tp = cv.cuda_GpuMat(tp)
        scr = cv.cuda_GpuMat(scr)
        matcher = cv.cuda.createTemplateMatching(cv.CV_8UC1, cv.TM_CCORR_NORMED)
        result = matcher.match(scr, tp)
        result = result.download()
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val < threshold:
            print(tmp, max_val, max_loc)
            return False
        print(tmp, max_val, max_loc)
        return True

    def toHome(self):
        while 1:
            text = self.OCR(539,683,587,709) 
            if text != '其它':
                self.doubleClick(54,35)
                time.sleep(2)
            else: 
                time.sleep(1)
                break


util = util()
class fishing:
    def __init__(self,ftimes,fpoint):
        self.times = ftimes
        self.point = fpoint
    def addCheck(self):
        while 1:
            if util.OCR(46,258,95,287) == '图鉴':
                a = util.OCR(1184,208,1208,226)  
                b = util.OCR(1184,299,1209,318)  
                c = util.OCR(1217,389,1243,408)  
                d = util.OCR(1217,480,1243,500)  
                e = util.OCR(1118,665,1173,686)  
                if e == '0':
                    return 0
                if (a, b, c, d).count('0') == True:
                    util.mouseClick(1211,187)  
                    time.sleep(1.5)
                    util.mouseClick(913,643)  
                    time.sleep(1)
                    util.mouseClick(1197,283)
                    time.sleep(1)
                    util.mouseClick(913,643)  
                    time.sleep(1)
                    if c == '0':
                        util.doubleClick(1194,403)  
                        time.sleep(1)
                        util.doubleClick(918,636)  
                        for i in range(4):
                            util.doubleClick(1001,463)
                        time.sleep(1)
                        util.doubleClick(1020,530)
                        time.sleep(1)
                        util.doubleClick(895,497)
                    if d == '0':
                        util.doubleClick(1197,522)  
                        time.sleep(1)
                        util.doubleClick(918,636)  
                        for i in range(4):
                            util.doubleClick(1001,463)
                        time.sleep(1)
                        util.doubleClick(1020,530)
                        time.sleep(1)
                        util.doubleClick(895,497)
                    util.doubleClick(54,35)
                if (a,b,c,d).count('0') == False:
                    break

    def pull(self):
        self.addCheck()
        time.sleep(1)
        util.doubleClick(1156,592)
        time.sleep(1.3)
        util.doubleClick(1156,592)

    def drag(self):
        while 1:
            if util.findPic(466,109,634,151,'钓鱼\\蓝色.bmp',0.98):
                util.mouseDown(1156,592)
            elif util.findPic(740,98,811,170,'钓鱼\\绿色.bmp',0.99):
                util.mouseDown(1156,592)
            elif util.findPic(901,155,941,229,'钓鱼\\红色.bmp',0.97):
                util.mouseUp(1156,592)   
            if util.OCR(572,639,704,671) == '点击屏幕继续':
                time.sleep(0.5)
                util.doubleClick(639,651)
                time.sleep(3)
                util.doubleClick(639,651)
                time.sleep(3)
                util.doubleClick(796,650)  
                if util.OCR(543,127,602,161) == '来自':
                    time.sleep(2)
                    util.doubleClick(663,348)
                    time.sleep(4)
                    util.doubleClick(658,589)
                break
            if util.OCR(581,159,752,209) == '鱼儿跑了':
                time.sleep(2)
                break

    def fjoin(self, point):
        util.toHome()
        time.sleep(1.5)
        util.doubleClick(736,665)
        time.sleep(2)
        points = [
            '钓鱼\\1湖湾公园.bmp',
            '钓鱼\\2汇湾海滨.bmp',
            '钓鱼\\3白金海岸.bmp',
            '钓鱼\\4牧森湖.bmp',
            '钓鱼\\5斯皮亚水库.bmp',
            '钓鱼\\6云霞群岛.bmp'
        ]
        result = util.findPic(480,48,1260,686,points[point],0.98)
        if result:
            util.clickPic(points[point],0.99)
        else:
            time.sleep(2)
            util.swipeDown()
            time.sleep(4)
            util.clickPic(points[point],0.99)

    def fishing(self):
        _times = 0
        self.fjoin(self.point)
        time.sleep(2)
        while _times < self.times:
            self.pull()
            time.sleep(2)
            self.drag()
            _times += 1
class tuya(object):
    def __init__(self,tchoice,tdif,ttimes):
        self.choice = tchoice
        self.dif = tdif
        self.times = ttimes
        self.choiceLoc = [
            (175,220),
            (331,243),
            (503,191),
            (681,205)
        ]
        self.difLoc = [
            (1034,180),
            (1041,263),
            (1043,318),
            (1043,389)
            ]
    
    def bt(self):
        _times = 0
        
        while _times < self.times:
            text = util.OCR(982,152,1179,213)
            if text == '战斗胜利':
                _times += 1
                time.sleep(2)
                util.doubleClick(916,624)
            elif text == '战斗失败':
                time.sleep(2)
                util.doubleClick(1094,640)  #退出
                time.sleep(5)
                util.doubleClick(1139,636)  #开始挑战
                time.sleep(2)
                util.doubleClick(1121,664)  #确认

    def tjoin(self):
        util.toHome()
        time.sleep(2)
        util.doubleClick(1083,651)  #点行动
        time.sleep(2)
        util.doubleClick(975,518)   #涂鸦
        time.sleep(2)
        cloc_x, cloc_y = self.choiceLoc[self.choice]
        dloc_x, dloc_y = self.difLoc[self.dif]
        util.doubleClick(cloc_x, cloc_y )
        time.sleep(2)
        util.doubleClick(dloc_x, dloc_y )
        time.sleep(2)
        util.clickPic("涂鸦\三倍.bmp",0.99)
        time.sleep(1)
        util.doubleClick(1135,634)
        time.sleep(2)
        util.clickPic("涂鸦\自动作战.bmp", 0.99)
        time.sleep(1)
        util.doubleClick(1114,661)

    def stuya(self):
        self.tjoin()
        self.bt()


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(QtCore.QSize(600, 400))
        MainWindow.setMaximumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 971, 721))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.fishing_check = QtWidgets.QCheckBox(self.tab_3)
        self.fishing_check.setGeometry(QtCore.QRect(330, 50, 131, 61))
        self.fishing_check.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.fishing_check.setFont(font)
        self.fishing_check.setObjectName("fishing_check")
        self.tuya_check = QtWidgets.QCheckBox(self.tab_3)
        self.tuya_check.setGeometry(QtCore.QRect(90, 50, 141, 61))
        self.tuya_check.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.tuya_check.setFont(font)
        self.tuya_check.setObjectName("tuya_check")
        self.confirm = QtWidgets.QPushButton(self.tab_3)
        self.confirm.setGeometry(QtCore.QRect(70, 150, 181, 81))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.confirm.setFont(font)
        self.confirm.setObjectName("confirm")
        self.save = QtWidgets.QPushButton(self.tab_3)
        self.save.setGeometry(QtCore.QRect(310, 150, 181, 81))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.save.setFont(font)
        self.save.setObjectName("save")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tuya_dif = QtWidgets.QComboBox(self.tab)
        self.tuya_dif.setGeometry(QtCore.QRect(290, 120, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.tuya_dif.setFont(font)
        self.tuya_dif.setObjectName("tuya_dif")
        self.tuya_dif.addItem("")
        self.tuya_dif.addItem("")
        self.tuya_dif.addItem("")
        self.tuya_dif.addItem("")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(90, 120, 171, 71))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(170, 210, 91, 71))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tuya_times = QtWidgets.QLineEdit(self.tab)
        self.tuya_times.setGeometry(QtCore.QRect(290, 210, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.tuya_times.setFont(font)
        self.tuya_times.setObjectName("tuya_times")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(90, 20, 171, 91))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tuya_choice = QtWidgets.QComboBox(self.tab)
        self.tuya_choice.setGeometry(QtCore.QRect(290, 30, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.tuya_choice.setFont(font)
        self.tuya_choice.setObjectName("tuya_choice")
        self.tuya_choice.addItem("")
        self.tuya_choice.addItem("")
        self.tuya_choice.addItem("")
        self.tuya_choice.addItem("")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(130, 180, 111, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.fishing_point = QtWidgets.QComboBox(self.tab_2)
        self.fishing_point.setGeometry(QtCore.QRect(280, 90, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.fishing_point.setFont(font)
        self.fishing_point.setObjectName("fishing_point")
        self.fishing_point.addItem("")
        self.fishing_point.addItem("")
        self.fishing_point.addItem("")
        self.fishing_point.addItem("")
        self.fishing_point.addItem("")
        self.fishing_point.addItem("")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(90, 80, 151, 81))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.fishing_times = QtWidgets.QLineEdit(self.tab_2)
        self.fishing_times.setGeometry(QtCore.QRect(280, 180, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.fishing_times.setFont(font)
        self.fishing_times.setObjectName("fishing_times")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CatBot"))
        self.fishing_check.setText(_translate("MainWindow", "钓鱼"))
        self.tuya_check.setText(_translate("MainWindow", "涂鸦"))
        self.confirm.setText(_translate("MainWindow", "确定"))
        self.save.setText(_translate("MainWindow", "保存设置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "开始"))
        self.tuya_dif.setItemText(0, _translate("MainWindow", "8"))
        self.tuya_dif.setItemText(1, _translate("MainWindow", "9"))
        self.tuya_dif.setItemText(2, _translate("MainWindow", "10"))
        self.tuya_dif.setItemText(3, _translate("MainWindow", "11"))
        self.label.setText(_translate("MainWindow", "涂鸦难度："))
        self.label_2.setText(_translate("MainWindow", "次数："))
        self.tuya_times.setText(_translate("MainWindow", "1"))
        self.label_4.setText(_translate("MainWindow", "涂鸦副本："))
        self.tuya_choice.setItemText(0, _translate("MainWindow", "1"))
        self.tuya_choice.setItemText(1, _translate("MainWindow", "2"))
        self.tuya_choice.setItemText(2, _translate("MainWindow", "3"))
        self.tuya_choice.setItemText(3, _translate("MainWindow", "4"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "涂鸦"))
        self.label_9.setText(_translate("MainWindow", "次数："))
        self.fishing_point.setItemText(0, _translate("MainWindow", "湖湾公园"))
        self.fishing_point.setItemText(1, _translate("MainWindow", "汇湾海滨"))
        self.fishing_point.setItemText(2, _translate("MainWindow", "白金海岸"))
        self.fishing_point.setItemText(3, _translate("MainWindow", "牧森湖"))
        self.fishing_point.setItemText(4, _translate("MainWindow", "斯皮亚水库"))
        self.fishing_point.setItemText(5, _translate("MainWindow", "云霞群岛"))
        self.label_10.setText(_translate("MainWindow", "钓鱼点："))
        self.fishing_times.setText(_translate("MainWindow", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "钓鱼"))

import sys
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
            tya = tuya(self.tuya_choice.currentIndex(),self.tuya_dif.currentIndex(),int(self.tuya_times.text().strip()))
            tya.stuya()
        if self.fishing_check.isChecked():
            diaoyu = fishing(int(self.fishing_times.text().strip()),self.fishing_point.currentIndex())
            diaoyu.fishing()

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = WindowGui()
    window.show() 
    sys.exit(app.exec())
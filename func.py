from pickletools import uint1
import time
from utility import *



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

<<<<<<< HEAD
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
=======
import time
from utility import util
import json
# try:
#     with open('self.data.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
# except:
#     raise FileExistsError('配置文件不存在')

class fishing:
    def __init__(self,ftimes,fpoint,data):
        self.data = data
        self.times = ftimes
        self.point = fpoint
        self.util = util(self.data)
        self.fingshing_point_x,self.fingshing_point_y = self.data['DEFAULT']['钓鱼场']
        self.back_x,self.back_y = self.data['DEFAULT']['返回']
        self.start_btn_x,self.start_btn_y = self.data['FISHING']['开始钓鱼按钮']
        self.duration = self.data['FISHING']['篮圈点击延迟']

        self.diaoshou_x0, self.diaoshou_y0, self.diaoshou_x1, self.diaoshou_y1 = self.data['FISHING']['钓手信息']
        self.a_x0,self.a_y0, self.a_x1, self.a_y1 =  self.data['FISHING']['钓竿']
        self.b_x0,self.b_y0, self.b_x1, self.b_y1 =  self.data['FISHING']['线轮']
        self.c_x0,self.c_y0, self.c_x1, self.c_y1 =  self.data['FISHING']['鱼线']
        self.d_x0,self.d_y0, self.d_x1, self.d_y1 =  self.data['FISHING']['鱼饵']
        self.e_x0,self.e_y0, self.e_x1, self.e_y1 =  self.data['FISHING']['鱼票']
        self.diaogan_x,self.diaogan_y = self.data['FISHING']['购买位置']['钓竿位置']['pos']
        self.xianlun_x,self.xianlun_y = self.data['FISHING']['购买位置']['线轮位置']['pos']
        self.yuxian_x,self.yuxian_y = self.data['FISHING']['购买位置']['鱼线位置']['pos']
        self.yu_er_x,self.yu_er_y = self.data['FISHING']['购买位置']['鱼饵位置']['pos']
        self.fix_x, self.fix_y = self.data['FISHING']['购买位置']['维修']['pos']
        self.add_x, self.add_y = self.data['FISHING']['购买位置']['鱼线和鱼饵购买位置']['数量增加按钮']
        self.purchase_x, self.purchase_y= self.data['FISHING']['购买位置']['鱼线和鱼饵购买位置']['购买按钮']
        self.confirm_x, self.confirm_y = self.data['FISHING']['购买位置']['鱼线和鱼饵购买位置']['确定购买按钮']

    
    def addCheck(self):
        while 1:
            if self.util.OCR(self.diaoshou_x0, self.diaoshou_y0, self.diaoshou_x1, self.diaoshou_y1) == '钓手信息':
                a = self.util.OCR(self.a_x0,self.a_y0, self.a_x1, self.a_y1)
                b = self.util.OCR(self.b_x0,self.b_y0, self.b_x1, self.b_y1)
                c = self.util.OCR(self.c_x0,self.c_y0, self.c_x1, self.c_y1)
                d = self.util.OCR(self.d_x0,self.d_y0, self.d_x1, self.d_y1)
                e = self.util.OCR(self.e_x0,self.e_y0, self.e_x1, self.e_y1)
                if e == '0':
                    return 0
                if (a, b, c, d).count('0') == True:
                    self.util.mouseClick(self.diaogan_x,self.diaogan_y)
                    time.sleep(1.5)
                    self.util.mouseClick(self.fix_x, self.fix_y)
                    time.sleep(1)
                    self.util.mouseClick(self.xianlun_x,self.xianlun_y)
                    time.sleep(1)
                    self.util.mouseClick(self.fix_x, self.fix_y)
                    time.sleep(1)
                    if c == '0':
                        self.util.doubleClick(self.yuxian_x,self.yuxian_y)
                        time.sleep(1)
                        self.util.doubleClick(self.fix_x, self.fix_y)
                        for _ in range(4):
                            self.util.doubleClick(self.add_x, self.add_y)
                        time.sleep(1)
                        self.util.doubleClick(self.purchase_x, self.purchase_y)
                        time.sleep(1)
                        self.util.doubleClick(self.confirm_x, self.confirm_y)
                    if d == '0':
                        self.util.doubleClick(self.yu_er_x,self.yu_er_y)  
                        time.sleep(1)
                        self.util.doubleClick(self.fix_x, self.fix_y)  
                        for _ in range(4):
                            self.util.doubleClick(self.add_x, self.add_y)
                        time.sleep(1)
                        self.util.doubleClick(self.purchase_x, self.purchase_y)
                        time.sleep(1)
                        self.util.doubleClick(self.confirm_x, self.confirm_y)
                    self.util.doubleClick(self.back_x,self.back_y)
>>>>>>> 6a3869e (fix bugs)
                if (a,b,c,d).count('0') == False:
                    break

    def pull(self):
        self.addCheck()
        time.sleep(1)
<<<<<<< HEAD
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
=======
        self.util.doubleClick(self.start_btn_x,self.start_btn_y)
        time.sleep(self.duration)
        self.util.doubleClick(self.start_btn_x,self.start_btn_y)

    def drag(self):
        blue_area = self.data['FISHING']['钓鱼图片识别位置']['蓝色区域图片的路径']
        blue_area_x0,blue_area_y0,blue_area_x1,blue_area_y1 = self.data['FISHING']['钓鱼图片识别位置']['蓝色区域']
        green_area = self.data['FISHING']['钓鱼图片识别位置']['绿色区域图片的路径']
        green_area_x0,green_area_y0,green_area_x1,green_area_y1 = self.data['FISHING']['钓鱼图片识别位置']['绿色区域']
        red_area = self.data['FISHING']['钓鱼图片识别位置']['红色区域图片的路径']
        red_area_x0,red_area_y0,red_area_x1,red_area_y1 = self.data['FISHING']['钓鱼图片识别位置']['红色区域']
        
        continue_x0,continue_y0,continue_x1,continue_y1 = self.data['FISHING']['点击屏幕继续']
        escape_x0,escape_y0,escape_x1,escape_y1 = self.data['FISHING']['鱼儿跑了']
        bottle_x0, bottle_y0,bottle_x1, bottle_y1 = self.data['FISHING']['来自异世界的瓶子']

        bottle_area_x,bottle_area_y = self.data['FISHING']['漂流瓶位置']
        bottle_confirm_x,bottle_confirm_y = self.data['FISHING']['漂流瓶确定']
        
        blank_x, blank_y = self.data['FISHING']['空白区域']
        confirm_ctn_x,confirm_ctn_y = self.data['FISHING']['点击屏幕']
        
        while 1:
            if self.util.findPic(blue_area_x0,blue_area_y0,blue_area_x1,blue_area_y1,blue_area,0.98):
                self.util.mouseDown(self.start_btn_x,self.start_btn_y)
            elif self.util.findPic(green_area_x0,green_area_y0,green_area_x1,green_area_y1,green_area,0.99):
                self.util.mouseDown(self.start_btn_x,self.start_btn_y)
            elif self.util.findPic(red_area_x0,red_area_y0,red_area_x1,red_area_y1,red_area,0.97):
                self.util.mouseUp(self.start_btn_x,self.start_btn_y)   
            if self.util.OCR(continue_x0,continue_y0,continue_x1,continue_y1) == '点击屏幕继续':
                time.sleep(0.5)
                self.util.doubleClick(confirm_ctn_x,confirm_ctn_y)
                time.sleep(3)
                self.util.doubleClick(confirm_ctn_x,confirm_ctn_y)
                time.sleep(3)
                self.util.doubleClick(blank_x, blank_y)  
                if self.util.OCR(bottle_x0, bottle_y0,bottle_x1, bottle_y1) == '来自异世界的瓶子':
                    time.sleep(2)
                    self.util.doubleClick(bottle_area_x,bottle_area_y)
                    time.sleep(4)
                    self.util.doubleClick(bottle_confirm_x,bottle_confirm_y)
                break
            if self.util.OCR(escape_x0,escape_y0,escape_x1,escape_y1) == '鱼儿跑了':
>>>>>>> 6a3869e (fix bugs)
                time.sleep(2)
                break

    def fjoin(self, point):
<<<<<<< HEAD
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
=======
        time.sleep(1.5)
        self.util.doubleClick(self.fingshing_point_x,self.fingshing_point_y)
        time.sleep(2)
        points = self.data['FISHING']['钓鱼点位置']
        if point>3:
            time.sleep(2)
            self.util.swipeDown()
            time.sleep(4)
        self.util.doubleClick(points[point][0],points[point][1])
>>>>>>> 6a3869e (fix bugs)

    def fishing(self):
        _times = 0
        self.fjoin(self.point)
        time.sleep(2)
        while _times < self.times:
            self.pull()
            time.sleep(2)
            self.drag()
            _times += 1
<<<<<<< HEAD
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
=======
class tuya:
    def __init__(self,tchoice,tdif,ttimes,data):
        self.util = util(data)
        self.data = data
        self.action_x,self.action_y = self.data['DEFAULT']['行动']
        self.tuya_x,self.tuya_y = self.data['DEFAULT']['涂鸦']

        self.choice = tchoice
        self.dif = tdif
        self.times = ttimes
        self.choiceLoc = self.data['TUYA']['副本位置']
        self.difLoc = self.data['TUYA']['涂鸦难度']

        self.invt_x,self.invt_y = self.data['TUYA']['开始调查']
        self.start_x,self.start_y = self.data['TUYA']['进入挑战后的确认']
        self.bt_result_x0,self.bt_result_y0,self.bt_result_x1,self.bt_result_y1=self.data['TUYA']['战斗结果区域']
        self.again_x,self.again_y = self.data['TUYA']['再次挑战']
        self.quit_x,self.quit_y = self.data['TUYA']['退出挑战']
    def bt(self):
        _times = 0

        while _times < self.times:
            text = self.util.OCR(self.bt_result_x0,self.bt_result_y0,self.bt_result_x1,self.bt_result_y1)
            if text == '战斗胜利':
                _times += 1
                time.sleep(2)
                self.util.doubleClick(self.again_x,self.again_y)
            elif text == '战斗失败':
                self.bt_restart()

    def bt_restart(self):
        time.sleep(2)
        self.util.doubleClick(self.quit_x,self.quit_y)  #退出
        time.sleep(5)
        self.util.doubleClick(self.start_x,self.start_y)  #开始挑战
        time.sleep(2)
        self.util.doubleClick(self.start_x,self.start_y)  #确认

    def tjoin(self):
        time.sleep(2)
        self.util.doubleClick(self.action_x,self.action_y)  #点行动
        time.sleep(2)
        self.util.doubleClick(self.tuya_x,self.tuya_y)   #涂鸦
        time.sleep(2)
        cloc_x, cloc_y = self.choiceLoc[self.choice]
        dloc_x, dloc_y = self.difLoc[self.dif]
        self.util.doubleClick(cloc_x, cloc_y )
        time.sleep(2)
        self.util.doubleClick(dloc_x, dloc_y )
        time.sleep(2)
        self.util.doubleClick(self.invt_x,self.invt_y)
        time.sleep(2)
        self.util.doubleClick(self.start_x,self.start_y)
>>>>>>> 6a3869e (fix bugs)

    def stuya(self):
        self.tjoin()
        self.bt()

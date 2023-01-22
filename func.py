import time
from utility import util

class Fishing:
    def __init__(self,ftimes,fpoint,data):
        self.data = data
        self.times = ftimes
        self.point = fpoint
        self.util = util(self.data)
        # print(self.data)
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
            diao_ocr =  self.util.OCR(self.diaoshou_x0, self.diaoshou_y0, self.diaoshou_x1, self.diaoshou_y1)
            # print(diao_ocr)
            if diao_ocr == '钓':
                a = self.util.OCR(self.a_x0,self.a_y0, self.a_x1, self.a_y1)
                b = self.util.OCR(self.b_x0,self.b_y0, self.b_x1, self.b_y1)
                c = self.util.OCR(self.c_x0,self.c_y0, self.c_x1, self.c_y1)
                d = self.util.OCR(self.d_x0,self.d_y0, self.d_x1, self.d_y1)
                e = self.util.OCR(self.e_x0,self.e_y0, self.e_x1, self.e_y1)
                
                if e == '0':
                    return False
                if '0' in [a, b, c, d]:
                    print(a, b, c, d, e)
                    print(self.diaogan_x,self.diaogan_y)
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
                else:
                   
                    return True
                    

    def pull(self):
        if self.addCheck():
            time.sleep(1)
            
            self.util.doubleClick(self.start_btn_x, self.start_btn_y)
            time.sleep(self.duration)
            self.util.doubleClick(self.start_btn_x, self.start_btn_y)
            return True
        return False


    def drag(self):
        blue_area = self.data['FISHING']['钓鱼图片识别位置']['蓝色区域图片的路径']
        blue_area_x0,blue_area_y0,blue_area_x1,blue_area_y1 = self.data['FISHING']['钓鱼图片识别位置']['蓝色区域']
        green_area = self.data['FISHING']['钓鱼图片识别位置']['绿色区域图片的路径']
        green_area_x0,green_area_y0,green_area_x1,green_area_y1 = self.data['FISHING']['钓鱼图片识别位置']['绿色区域']
        red_area = self.data['FISHING']['钓鱼图片识别位置']['红色区域图片的路径']
        red_area_x0,red_area_y0,red_area_x1,red_area_y1 = self.data['FISHING']['钓鱼图片识别位置']['红色区域']
        
        continue_x0,continue_y0,continue_x1,continue_y1 = self.data['FISHING']['点击屏幕继续']
        bottle_x0, bottle_y0,bottle_x1, bottle_y1 = self.data['FISHING']['来自异世界的瓶子']

        bottle_area_x,bottle_area_y = self.data['FISHING']['漂流瓶位置']
        bottle_confirm_x,bottle_confirm_y = self.data['FISHING']['漂流瓶确定']
        
        level_up_x0, level_up_y0,  level_up_x1, level_up_y1 = self.data['FISHING']['钓鱼等级提升']
        confirm_ctn_x,confirm_ctn_y = self.data['FISHING']['点击屏幕']
        
        while 1:
            continue_ocr = self.util.OCR(continue_x0,continue_y0,continue_x1,continue_y1)
           
            fish_info = self.util.OCR(self.diaoshou_x0, self.diaoshou_y0, self.diaoshou_x1, self.diaoshou_y1)
            if self.util.findPic(blue_area_x0,blue_area_y0,blue_area_x1,blue_area_y1,blue_area,0.98):
                self.util.mouseDown(self.start_btn_x,self.start_btn_y)
            elif self.util.findPic(green_area_x0,green_area_y0,green_area_x1,green_area_y1,green_area,0.99):
                self.util.mouseDown(self.start_btn_x,self.start_btn_y)
            elif self.util.findPic(red_area_x0,red_area_y0,red_area_x1,red_area_y1,red_area,0.97):
                self.util.mouseUp(self.start_btn_x,self.start_btn_y)  
            elif fish_info == '钓':
                # time.sleep(2)
                break 
            elif continue_ocr == '点击屏幕继续':
                time.sleep(2)
                # 点击屏幕继续
                print("ping")
                self.util.doubleClick(confirm_ctn_x,confirm_ctn_y)
                time.sleep(3)
                # 确定鱼的信息
                print("yu")
                self.util.doubleClick(confirm_ctn_x,confirm_ctn_y)
                time.sleep(3)
                while 1:
                    bottle_ocr = self.util.OCR(bottle_x0, bottle_y0,bottle_x1, bottle_y1)
                    # level_up_ocr = self.util.OCR(level_up_x0, level_up_y0,  level_up_x1, level_up_y1)
                    # print(bottle_ocr)
                    if bottle_ocr == '来':
                        
                        print(self.util.OCR(bottle_x0, bottle_y0,bottle_x1, bottle_y1))
                        time.sleep(2)
                        self.util.doubleClick(bottle_area_x,bottle_area_y)
                        time.sleep(4)
                        self.util.doubleClick(bottle_confirm_x,bottle_confirm_y)
                        break
                    # print(fish_info)
                    if bottle_ocr != '来':
                        # 出现钓鱼升级或者获得食谱后再点一下，避免卡住
                        time.sleep(3)
                        print('skip')
                        self.util.doubleClick(confirm_ctn_x, confirm_ctn_y) 
                        break
                break
           

    def fjoin(self, point):
        time.sleep(2)
        self.util.doubleClick(self.fingshing_point_x,self.fingshing_point_y)
        time.sleep(2)
        points = self.data['FISHING']['钓鱼点位置']
        if point>3:
            time.sleep(2)
            self.util.swipeDown()
            time.sleep(4)
        self.util.doubleClick(points[point][0],points[point][1])

    def fishing(self):
        _times = 0
        self.fjoin(self.point)
        time.sleep(2)
        while _times < self.times:
            self.pull()
            time.sleep(2)
            self.drag()
            _times += 1
               

class Tuya:
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
        self.util.doubleClick(self.invt_x,self.invt_y)  #开始挑战
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

    def stuya(self):
        self.tjoin()
        self.bt()

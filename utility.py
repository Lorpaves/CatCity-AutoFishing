from io import BytesIO
import time
from PIL import Image
import win32api ,win32con, win32gui, win32ui
import ddddocr
import cv2 as cv
import numpy as np

class util:

    def __init__(self, data):
        self.data = data
        name = data['DEFAULT']['模拟器名称']
        self.ocr = ddddocr.DdddOcr()
        hwnd = win32gui.FindWindow(None,name)
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
        scr = self.capWindow()
        tp = self.cvRead(tmp)
        result = cv.matchTemplate(scr, tp, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val < threshold:
            print(tmp, max_val, max_loc)
            return False
        self.mouseDown(int(max_loc[0]) + int(tp.shape[1]/2), int(max_loc[1]) + int(tp.shape[0]/2))
        time.sleep(0.5)
        self.mouseUp(int(max_loc[0]) + int(tp.shape[1]/2), int(max_loc[1]) + int(tp.shape[0]/2))
        return True
        
    def findPic(self, x:int, y:int, x1:int, y1:int, tmp:str, threshold:float):
        scr = self.capWindowPos(x,y,x1,y1)
        tp = self.cvRead(tmp)
        result = cv.matchTemplate(scr, tp, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val < threshold:
            print(tmp, max_val, max_loc)
            return False
        print(tmp, max_val, max_loc)
        return True


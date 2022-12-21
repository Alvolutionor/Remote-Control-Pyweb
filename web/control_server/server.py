import win32gui,win32api,win32ui,win32con
import pywin
import ctypes
import random,time
from sys import exit
from PIL import Image
from cuda import cuda, nvrtc
import d3dshot
import numpy


def mouse_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y)

def prt_scr():
    print(time.time())
    window_capture('static\\screenshot\\screenshot.bmp')
    img = Image.open('static\\screenshot\\screenshot.bmp')
    print(time.time())
    img.save('static\\screenshot\\screenshot.png')
    print(time.time())



def screen_off():
    win32api.SendMessage(win32api.GetCurrentProcess(), win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)

def window_capture(filename):

    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    # print(time.time())
    # d_shot = d3dshot.create(capture_output="numpy")
    # d_shot.screenshot()
    # d_shot.stop()

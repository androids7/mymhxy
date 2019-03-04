#!/usr/bin/python
# coding=utf-8
import threading
import win32api,win32gui,win32con
import time
import autopy
import urllib.request 
import wx
import wx.adv
from PIL import ImageGrab
from image import OpenCVImageMatcher
import numpy as np
ver  = '1.0'
defPwd='******'
startx=0
posx=0
starty=0
posy=0
isZhuaGui = True
matcher=1

#校验密码
def CheckPwd():
    return True
    pwd1=time.strftime('%Y%m%d',time.localtime(time.time()))
    if(frame.doPwd.GetValue() == pwd1):
        return True
    else:
        win32api.MessageBox(0,u'口令错误')
        exit()

# 自动任务
def oneKeyDo(param):
    global frame
    if frame.oneKeyAutoDo.LabelText =='一键自动任务':
        frame.oneKeyAutoDo.LabelText='停止一键自动任务'
        # 检查口令
        if(CheckPwd() != True):
            return False
        win32api.MessageBox(0,u'待开发')
        return True
    else:
        frame.oneKeyAutoDo.LabelText='一键自动任务'


#宝图线程
def BaoTuTh(param):
    global frame
    if frame.autoDaTu.LabelText =='自动宝图':
        frame.autoDaTu.LabelText='停止自动宝图'
        # 检查口令
        # if(CheckPwd() != True):
        #     return False
        t = threading.Thread(target=baotu)
        t.setDaemon(True)
        t.start()
    else:
        frame.autoDaTu.LabelText='自动宝图'

def baotu():
    # 打开活动页面
    rect=matcher.match_sub_image(window_capture_all(),'./image/activity.png')
    do(rect)
    
    # 点击宝图
    rect1=matcher.match_sub_image(window_capture_all(),'./image/activity_baotu.png')
    print(rect1)
    rect1[0]=rect1[0]+327
    do(rect1)
    #接受宝图
    # rect=matcher.match_sub_image(window_capture_all(),'./image/activity_baotu_start.png')
    # do(rect)

 
#抓鬼线程
def zhuaGuiTh(param):
    global frame
    if frame.autoZhuaGui.LabelText =='自动带队抓鬼':
        frame.autoZhuaGui.LabelText='停止自动带队抓鬼'
        AddToList('自动带队抓鬼')
        # 检查口令
        # if(CheckPwd() != True):
        #     return False
        t = threading.Thread(target=zhuagui,args=(u'捉鬼',))
        t.setDaemon(True)
        t.start()

    else:
        frame.autoZhuaGui.LabelText='自动带队抓鬼'
        AddToList('停止自动带队抓鬼')

def zhuagui():
    global isZhuaGui
    


class Frame(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY,title=u"梦幻手游辅助v"+ver,pos=wx.DefaultPosition,size=(500,400),style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.SetIcon(wx.Icon('./ico/mhxy.ico', wx.BITMAP_TYPE_ICO))
        panel = wx.Panel(self, wx.ID_ANY)
        # 控件
        self.tripText1 = wx.StaticText(panel,wx.ID_ANY,label=u'口令:',pos=(0, 15))
        self.tripText1.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.doPwd= wx.TextCtrl(panel,wx.ID_ANY,pos=(40,10),size=(90,25))
        self.doPwd.SetValue(defPwd)
        self.tripText2 = wx.StaticText(panel,wx.ID_ANY,label=u'--------------------------------------操作--------------------------------------------',pos=(0, 35))
        self.tripText2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.oneKeyAutoDo = wx.Button(panel,wx.ID_ANY,label=u"一键自动任务",pos=(10,55),size=(110,35))
        self.autoZhuaGui  = wx.Button(panel,wx.ID_ANY,label=u"自动带队抓鬼",pos=(140,55),size=(110,35))
        self.autoDaTu  = wx.Button(panel,wx.ID_ANY,label=u"自动宝图",pos=(10,100),size=(110,35))
        # 控件事件
        self.Bind(wx.EVT_BUTTON, oneKeyDo, self.oneKeyAutoDo)
        self.Bind(wx.EVT_BUTTON, zhuaGuiTh, self.autoZhuaGui)
        self.Bind(wx.EVT_BUTTON, BaoTuTh, self.autoDaTu)

        self.listbox1 = wx.ListBox(panel,wx.ID_ANY,(270,55),(200,300),[],wx.LB_SINGLE)

def AddToList(strLine):
    frame.listbox1.Append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    frame.listbox1.Append(strLine)
    frame.listbox1.Append(" ")

def OnClose(event):
    global frame
    r = wx.MessageBox("是否真的要关闭窗口？", "请确认", wx.CANCEL|wx.OK|wx.ICON_QUESTION)
    if r == wx.OK:        #注意wx.OK跟wx.MessageDialog返回值wx.ID_OK不一样
        frame.Destroy()
 
def closeMhxy():
    mhName = u"梦幻手游辅助v"+ver
    # 获得窗体的句柄
    # 从顶层窗口向下搜索主窗口，无法搜索子窗口
    mhwin = win32gui.FindWindow(None,mhName)
    if(mhwin > 0):
        # 该函数将一个消息放入（寄送）到与指定窗口创建的线程相联系消息队列里，不等待线程处理消息就返回。消息队列里的消息通过调用GetMessage和PeekMessage取得。
        # 寄送的消息:win32con.WM_QUIT,加的消息特定的信息:0
        # 应该是关闭窗体
        win32api.PostMessage(mhwin, win32con.WM_QUIT, 0, 0)

def window_capture(rect):
    img_rgb = ImageGrab.grab(bbox=rect)
    img_rgb.save('./test1.jpg','JPEG') #设置保存路径和图片格式
    return './test1.jpg'

def window_capture_all():
    return window_capture((startx,starty,startx+posx,starty+posy))

def do(rect):
    if rect:
        autopy.mouse.smooth_move(rect[0],rect[1])
        time.sleep(1)
        autopy.mouse.click()
    else:
        return

if __name__ == '__main__':
    # 已经在运行的关闭窗体
    closeMhxy()
    # 测试网络
    try:
        servetStr = urllib.request.urlopen("http://www.baidu.com/").read()
    except:
        win32api.MessageBox(0,u'启动失败,请检查网络')
        exit()
 
    app = wx.App()
    # 创建操作界面
    frame = Frame(size=(500, 400))
    # 放置该帧(frame)显示在中心
    frame.Bind(wx.EVT_CLOSE, OnClose)#主窗口绑定自身的关闭事件
    frame.Centre()
    frame.Show()

   # 配置大小
    wdname='《梦幻西游》手游'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle>0:
        win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)   
        rect=win32gui.GetWindowRect(handle)
        startx=rect[0]
        starty=rect[1]
        posx=rect[2]-rect[0]
        posy=rect[3]-rect[1]
    else:
        AddToList('游戏没有启动，请关闭软件重新打开！')

    matcher=OpenCVImageMatcher()
    app.MainLoop()
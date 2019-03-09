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

shimenTh=True
# 自动任务
def oneKeyDo(param):
    global frame
    global shimenTh
    if frame.oneKeyAutoDo.LabelText =='一键师门任务':
        frame.oneKeyAutoDo.LabelText='停止一键自动任务'
        # 检查口令
        # if(CheckPwd() != True):
        #     return False
        shimenTh=True
        t = threading.Thread(target=shimen)
        t.setDaemon(True)
        t.start()
        
    else:
        shimenTh=False
        AddToList('停止师门任务')
        frame.oneKeyAutoDo.LabelText='一键自动任务'

def shimen():
    global frame
    while shimenTh:
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/gangbi.png')
        do(rect,'点击关闭')
        time.sleep(1)
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/zhicaolinfu.png')
        if rect:
            do(rect,'点击师门任务')
            time.sleep(10)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/shimenuse.png')
            do(rect,'点击使用灵符')
            time.sleep(1)
        
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/gangbi.png')
        do(rect,'点击关闭')
        time.sleep(1)
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/xunzudoxi.png')
        if rect:
            do(rect,'点击师门任务')
            time.sleep(10)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/goumai.png')
            do(rect,'点击购买')
            time.sleep(4)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/goumai2.png')
            do(rect,'点击购买')
            time.sleep(4)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/shangjiao.png')
            do(rect,'点击上交')
            time.sleep(2)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/gangbi.png')
        do(rect,'点击关闭')
        time.sleep(1)
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/congwu.png')
        if rect:
            do(rect,'点击师门任务')
            time.sleep(10)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/goumai3.png')
            do(rect,'点击购买')
            time.sleep(7)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/shangjiao.png')
            do(rect,'点击上交')
            time.sleep(2)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/gangbi.png')
        do(rect,'点击关闭')
        time.sleep(1)
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/xunluo.png')
        if rect:
            do(rect,'点击师门任务')
            time.sleep(10)
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/wancheng.png')
        if rect:
            AddToList('完成师门')
            break


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
        win32api.MessageBox(0,u'操作不允许')

def baotu():
    global frame
    # 打开活动页面
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity.png')
    do(rect,'打开活动页面')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/richanghuidong.png')
    do(rect,'选择日常活动')
    time.sleep(2)
    # 点击宝图
    rect1=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity_baotu.png')
    rect1[0]=rect1[0]+280
    do(rect1,'点击宝图')
    time.sleep(15)
    #接受宝图
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity_baotu_start.png')
    do(rect,'接受宝图')
    time.sleep(2)
    # 打开收缩的任务视图
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/open_renwu.png')
    do(rect,'打开收缩的任务视图')
    time.sleep(1)
    # 点击开始宝图
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/baotu_satrt.png')
    do(rect,'点击开始宝图1')
    do(rect,'点击开始宝图2')
    time.sleep(1)
    
    count=0
    while(True):
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhandou.png')
        if rect:
            count=0
            AddToList('正在战斗')
        else:
            count+=1
            time.sleep(10)
            # 两分钟没有则完成宝图
            if count>6:
                do(rect,'完成宝图战斗')
                count=0
                break
    
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/baogou.png')
    do(rect,'打开包裹')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/baotu.png')
    do(rect,'点击宝图')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/use.png')
    do(rect,'点击使用')
    time.sleep(1)

    while(True):
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/baotu_use.png')
        if rect:
            count=0
            rect[1]=rect[1]+60
            do(rect,'点击开始挖宝')
        else:
            count+=1
            time.sleep(10)
            # 两分钟没有则完成宝图
            if count>12:
                do(rect,'完成挖图')
                count=0
                break

    frame.autoDaTu.LabelText='自动宝图'


 
#抓鬼线程
def zhuaGuiTh(param):
    global frame
    if frame.autoZhuaGui.LabelText =='自动带队抓鬼':
        frame.autoZhuaGui.LabelText='停止自动带队抓鬼'
        AddToList('自动带队抓鬼')
        # 检查口令
        # if(CheckPwd() != True):
        #     return False
        t = threading.Thread(target=zhuagui)
        t.setDaemon(True)
        t.start()

    else:
        frame.autoZhuaGui.LabelText='自动带队抓鬼'
        AddToList('停止自动带队抓鬼')

def zhuagui():
    global isZhuaGui

    # 打开收缩的任务视图
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/open_renwu.png')
    do(rect,'打开收缩的任务视图')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/duiwu.png')
    do(rect,'打开队伍视图1')
    do(rect,'打开队伍视图2')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/duiwu1.png')
    do(rect,'打开队伍视图3')
    do(rect,'打开队伍视图4')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/chungjiangduiwu.png')
    if rect:
        do(rect,'创建队伍')
        time.sleep(2)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/duiwuxuanze.png')
        do(rect,'队伍选择')
        time.sleep(1)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguirenwu.png')
        do(rect,'选择捉鬼任务')
        time.sleep(5)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguiqueding.png')
        do(rect,'确定捉鬼任务')
        time.sleep(1)
    
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/tuichu.png')
    if rect:
        time.sleep(1)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/duiwuxuanze.png')
        do(rect,'队伍选择')
        time.sleep(1)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguirenwu.png')
        do(rect,'选择捉鬼任务')
        time.sleep(5)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguiqueding.png')
        do(rect,'确定捉鬼任务')
        time.sleep(1)
    while True:
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuzhan.png')
        if rect:
            AddToList('等待队伍人数')
            time.sleep(5)
        else:
            AddToList('队伍够人')
            break

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/guangbi.png')
    do(rect,'关闭任务界面')
    time.sleep(1)

    # 打开活动页面
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity.png')
    do(rect,'打开活动页面')
    time.sleep(1)

    rect1=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/richanghuidong.png')
    do(rect1,'选择日常活动')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuogui.png')
    if rect:
        rect[0]=rect[0]+280
        do(rect,'点击捉鬼活动')
        time.sleep(5)
    else:
        autopy.mouse.smooth_move(rect1[0]+200,rect1[1])
        time.sleep(1)
        while True:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-200)
            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuogui.png')
            if rect:
                break

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuogui.png')
        rect[0]=rect[0]+280
        do(rect,'点击捉鬼活动')
        time.sleep(5)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/lingquzhuogui.png')
    do(rect,'领取捉鬼任务')
    time.sleep(2)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguirenwu1.png')
    do(rect,'点击捉鬼任务1')
    time.sleep(1)
    do(rect,'点击捉鬼任务2')
    time.sleep(1)

    while(True):
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhandou.png')
        if rect:
            time.sleep(10)
            AddToList('正在捉鬼战斗')
        else:
            time.sleep(10)
            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguiwancheng.png')
            if rect:
                rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/jxzhuogui.png')
                do(rect,'继续捉鬼')
                time.sleep(10)

                rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/lingquzhuogui.png')
                do(rect,'领取捉鬼任务')
                time.sleep(2)

                rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/buman5ren.png')
                if rect:
                    do(rect,'队伍不满五人')
                    time.sleep(2)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/jxzhuogui.png')
                    do(rect,'确定不满5人')
                    time.sleep(3)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zidongpipei.png')
                    do(rect,'点击自动匹配')
                    time.sleep(1)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/guangbi.png')
                    do(rect,'关闭任务界面')
                    time.sleep(1)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity.png')
                    do(rect,'打开活动页面')
                    time.sleep(1)

                    rect1=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/richanghuidong.png')
                    do(rect1,'选择日常活动')
                    time.sleep(1)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuogui.png')
                    if rect:
                        rect[0]=rect[0]+280
                        do(rect,'点击捉鬼活动')
                        time.sleep(5)
                    else:
                        autopy.mouse.smooth_move(rect1[0]+200,rect1[1])
                        time.sleep(1)
                        while True:
                            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-200)
                            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuogui.png')
                            if rect:
                                break

                        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuogui.png')
                        rect[0]=rect[0]+280
                        do(rect,'点击捉鬼活动')
                        time.sleep(5)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/lingquzhuogui.png')
                    do(rect,'领取捉鬼任务')
                    time.sleep(3)

                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguirenwu1.png')
                    do(rect,'点击捉鬼任务1')
                    time.sleep(2)
                    do(rect,'点击捉鬼任务2')
                    time.sleep(1)
                else:
                    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/zhuoguirenwu1.png')
                    do(rect,'点击捉鬼任务1')
                    time.sleep(3)
                    do(rect,'点击捉鬼任务2')
                    time.sleep(1)
            else:
                rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/shimen/gangbi.png')
                do(rect,'点击关闭')
                time.sleep(1)

def yunbiaoTh(param):
    global frame
    if frame.yunbiao.LabelText =='自动运镖':
        frame.yunbiao.LabelText='停止自动运镖'
        AddToList('自动运镖')
        # 检查口令
        # if(CheckPwd() != True):
        #     return False
        t = threading.Thread(target=yunbiao)
        t.setDaemon(True)
        t.start()

    else:
        frame.yunbiao.LabelText='自动运镖'
        AddToList('停止自动运镖')

def yunbiao():
    # 打开活动页面
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity.png')
    do(rect,'打开活动页面')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/richanghuidong.png')
    do(rect,'选择日常活动')
    time.sleep(2)
    # 点击宝图
    rect1=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/yunbiao/yunbiao.png')
    rect1[0]=rect1[0]+280
    do(rect1,'点击运镖')
    time.sleep(10)

    count=0
    while True:
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/yunbiao/start.png')
        if rect:
            count+=1
            do(rect,'开始运镖')
            time.sleep(4)
            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/yunbiao/ok.png')
            do(rect,'确定')
            time.sleep(2)

        else:
            AddToList('运镖中')
            time.sleep(5)
        if count>=3:
            break


def sanjieTh(param):
    global frame
    if frame.sanjie.LabelText =='自动三界奇缘':
        frame.sanjie.LabelText='停止自动三界奇缘'
        AddToList('自动三界奇缘')
        # 检查口令
        # if(CheckPwd() != True):
        #     return False
        t = threading.Thread(target=sanjie)
        t.setDaemon(True)
        t.start()

    else:
        frame.sanjie.LabelText='自动三界奇缘'
        AddToList('停止自动三界奇缘')

def sanjie():
    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/activity.png')
    do(rect,'打开活动页面')
    time.sleep(1)

    rect1=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/zhuogui/richanghuidong.png')
    do(rect1,'选择日常活动')
    time.sleep(1)

    rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/sanjie/sanjie.png')
    if rect:
        rect[0]=rect[0]+280
        do(rect,'点击三界奇缘')
        time.sleep(5)
    else:
        autopy.mouse.smooth_move(rect1[0]+200,rect1[1])
        time.sleep(1)
        while True:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-200)
            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/sanjie/sanjie.png')
            if rect:
                rect[0]=rect[0]+280
                do(rect,'点击三界奇缘')
                time.sleep(5)
                break
    while True:
        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/sanjie/wancheng.png')
        if rect:
            do(rect,'完成三界奇缘')
            time.sleep(2)

            rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/sanjie/gbi.png')
            do(rect,'关闭三界奇缘')
            time.sleep(2)

        rect=matcher.match_sub_image(startx,starty,window_capture_all(),'./image/sanjie/bi.png')
        rect[0]=rect[0]+200
        rect[1]=rect[1]+200
        do(rect,'点击三界奇缘')
        time.sleep(2)




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

        self.oneKeyAutoDo = wx.Button(panel,wx.ID_ANY,label=u"一键师门任务",pos=(10,55),size=(110,35))
        self.autoZhuaGui  = wx.Button(panel,wx.ID_ANY,label=u"自动带队抓鬼",pos=(140,55),size=(110,35))
        self.autoDaTu  = wx.Button(panel,wx.ID_ANY,label=u"自动宝图",pos=(10,100),size=(110,35))
        self.yunbiao  = wx.Button(panel,wx.ID_ANY,label=u"自动运镖",pos=(140,100),size=(110,35))
        self.sanjie  = wx.Button(panel,wx.ID_ANY,label=u"自动三界奇缘",pos=(10,145),size=(110,35))
        # 控件事件
        self.Bind(wx.EVT_BUTTON, oneKeyDo, self.oneKeyAutoDo)
        self.Bind(wx.EVT_BUTTON, zhuaGuiTh, self.autoZhuaGui)
        self.Bind(wx.EVT_BUTTON, BaoTuTh, self.autoDaTu)
        self.Bind(wx.EVT_BUTTON, yunbiaoTh, self.yunbiao)
        self.Bind(wx.EVT_BUTTON, sanjieTh, self.sanjie)

        self.listbox1 = wx.ListBox(panel,wx.ID_ANY,(270,55),(200,300),[],wx.LB_SINGLE)

def AddToList(strLine):
    frame.listbox1.Append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    frame.listbox1.Append(strLine)
    frame.listbox1.Append(" ")
    frame.listbox1.SetSelection(frame.listbox1.GetCount()-1)

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

def do(rect,msg):
    if rect:
        autopy.mouse.smooth_move(rect[0],rect[1])
        autopy.mouse.click()
        AddToList(msg)
    else:
        AddToList(msg+'--stop')
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
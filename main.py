#!/usr/bin/python
# coding=utf-8
import threading
import win32api,win32gui,win32con
import time
import autopy
import urllib.request 
import wx
import wx.adv

ver  = '1.0'
defPwd = '******'
threads = []
isStart = True
 
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
 
def closeWin():
    #autopy.mouse.smooth_move(1255, 8)#最大化
    autopy.mouse.smooth_move(610, 10)
    time.sleep(1)
    autopy.mouse.click()
    time.sleep(1)
    #autopy.mouse.smooth_move(580, 450)#最大化
    autopy.mouse.smooth_move(260, 245)
    time.sleep(1)
    autopy.mouse.click()
    return True
 
def closePC():
    autopy.mouse.smooth_move(27, 783)
    time.sleep(1)
    autopy.mouse.click()
    time.sleep(1)
    autopy.mouse.smooth_move(303, 740)
    time.sleep(1)
    autopy.mouse.click()
    return True
 
#打图
def daTu():
    global isStart
    if(isStart == False):
        time.sleep(5)
    while isStart:
        if(frame.setRows.GetValue() == '1'):
            autopy.mouse.smooth_move(540, 125) 
        elif(frame.setRows.GetValue() == '2'):
            autopy.mouse.smooth_move(540, 168) 
        elif(frame.setRows.GetValue() == '3'):
            autopy.mouse.smooth_move(540, 214) 
        else:
            win32api.MessageBox(0,u'行号超出范围')
            return False
        time.sleep(1)
        autopy.mouse.click() # 单击   `
        time.sleep(3)
    isStart = True 
    return True
#抓鬼
def zhuaGui():
    wdname='《梦幻西游》手游'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    rect=win32gui.GetWindowRect(handle)
    #win32gui.SetWindowPos(handle,win32con.HWND_TOPMOST,0,0,640,362,win32con.SWP_SHOWWINDOW)
    autopy.mouse.smooth_move(520, 480)
    time.sleep(1)
    autopy.mouse.click() 

def startTh():
    global isStart
    isStart=True
    for t in threads:
        t.setDaemon(True)
        t.start()

#校验密码
def CheckPwd():
    return True
    pwd1=time.strftime('%Y%m%d',time.localtime(time.time()))
    if(frame.doPwd.GetValue() == pwd1):
        return True
    else:
        win32api.MessageBox(0,u'口令错误')
        exit()

#线程管理
def allThs(param,toDo):
    # 先停止全部
    endAllTh(param)
    # 检查口令
    if(CheckPwd() != True):
        return False
    t = threading.Thread(target=toDo)
    threads.append(t)
    startTh()

# 自动任务
def oneKeyDo(param):
    win32api.MessageBox(0,u'待开发')
    return True

#打图线程
def daTuTh(param):
    allThs(param,daTu)
 
#抓鬼线程
def zhuaGuiTh(param):
    allThs(param,zhuaGui)

# 停止
def endAllTh(param):
    global isStart
    isStart = False
 
class TaskBarIcon(wx.adv.TaskBarIcon):
    ID_About = wx.NewId()
    ID_Minshow=wx.NewId()
    ID_Maxshow=wx.NewId()
    ID_Closeshow=wx.NewId()
     
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='mhxy.ico', type=wx.BITMAP_TYPE_ICO), u'梦幻手游辅助工具')  #wx.ico为ico图标文件
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick) #定义左键双击
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnMinshow, id=self.ID_Minshow)
        self.Bind(wx.EVT_MENU, self.OnMaxshow, id=self.ID_Maxshow)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)
 
    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
 
    def OnAbout(self,event):
        wx.MessageBox(u'梦幻手游辅助工具v'+ver  +u'-"梦幻"群内部使用', u'关于工具')
 
    def OnMinshow(self,event):
        self.frame.Iconize(True)
         
     
    def OnMaxshow(self,event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
        #self.frame.Maximize(True) #最大化显示
 
    def OnCloseshow(self,event):
        self.frame.Close(True)
 
    # 右键菜单
    def CreatePopupMenu(self):
        menu = wx.Menu()
        #menu.Append(self.ID_Minshow, u'最小化')
        menu.Append(self.ID_Maxshow, u'显示窗口')
        menu.Append(self.ID_About, u'关于工具')
        menu.Append(self.ID_Closeshow, u'退出')
        return menu
 
class Frame(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY,title=u"梦幻手游辅助v"+ver,pos=wx.DefaultPosition,size=(400,300),style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
         
        self.SetIcon(wx.Icon('mhxy.ico', wx.BITMAP_TYPE_ICO))
        panel = wx.Panel(self, wx.ID_ANY)
 
        self.taskBarIcon = TaskBarIcon(self)
         
        # 绑定事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy) # 窗口最小化时，调用OnIconfiy,注意Wx窗体上的最小化按钮，触发的事件是 wx.EVT_ICONIZE,而根本就没有定义什么wx.EVT_MINIMIZE,但是最大化，有个wx.EVT_MAXIMIZE。
 
        self.tripText1 = wx.StaticText(panel,wx.ID_ANY,label=u'请在此输入框内输入操作口令:',pos=(0, 10))
        self.tripText1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.doPwd= wx.TextCtrl(panel,wx.ID_ANY,pos=(250,0),size=(90,25))
        self.doPwd.SetValue(defPwd);
 
        self.oneKeyAutoDo = wx.Button(panel,wx.ID_ANY,label=u"一键自动任务",pos=(10,60),size=(80,25))
        self.autoZhuaGui  = wx.Button(panel,wx.ID_ANY,label=u"自动带队抓鬼",pos=(95,60),size=(80,25))
        self.autoDaTu  = wx.Button(panel,wx.ID_ANY,label=u"自动打图",pos=(180,60),size=(80,25))
        self.endDo  = wx.Button(panel,wx.ID_ANY,label=u"停止操作",pos=(265,60),size=(80,25))
         
        self.Bind(wx.EVT_BUTTON, oneKeyDo, self.oneKeyAutoDo)
        self.Bind(wx.EVT_BUTTON, zhuaGuiTh, self.autoZhuaGui)
        self.Bind(wx.EVT_BUTTON, daTuTh, self.autoDaTu)
        self.Bind(wx.EVT_BUTTON, endAllTh, self.endDo)
         
    def OnHide(self, event):
        self.Hide()
    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()
    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()
    def OnCloseMe(self, event):
        self.SetBackgroundColour('Red')
        self.Refresh()
 
 
if __name__ == '__main__':
    # 关闭窗体
    closeMhxy()
    # 测试网络
    try:
        servetStr = urllib.request.urlopen("http://www.baidu.com/").read()
    except:
        win32api.MessageBox(0,u'启动失败,请检查网络')
        exit()
    
    # 获取海马模拟器的窗体
    winName = u'海马玩模拟器(Droid4X) 0.7.3 Beta'
    hmw = win32gui.FindWindow(None,winName)
 
    app = wx.App()
    # 创建操作界面
    frame = Frame(size=(400, 300))
    # 放置该帧(frame)显示在中心
    frame.Centre()
    frame.Show()
    app.MainLoop()
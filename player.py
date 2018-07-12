# python3
# _*_ coding: utf-8 _*_

'''
Created on 20180402
@Auther: Mild Yang

0.0.04.20180615.beta
'''

import pygame
import time
import wx
import wx.adv
import threading
# from wx.lib.pubsub import pub
# import multiprocessing
import os
import sys
import logging


version = "0.0.04.20180710.beta"
# 应用程序数据默认保存目录
apppath = r"D:/语音测试工具应用/"
mp3path = apppath + "/测试语音/"
tmppath = apppath + "/tmp/"


'''
日志模块：
    获取日志实例，配置日志的格式和输出方式
    APP           主日志
    APP.UI        页面相关日志
    APP.Server    处理过程日志
    APP.operater  操作记录日志
    APP.Test      测试相关日志
'''


class MyLog():

    def LogCfg(self, filename):
        # logging.basicConfig(level=logging.DEBUG)

        # 获取logger实例，如果参数为空则返回root logger
        logger = logging.getLogger("APP")

        # 指定logger输出格式
        formatter = logging.Formatter(
            '%(asctime)s %(name)-8s %(funcName)-8s %(levelname)-8s: %(message)s')

        # 文件日志
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值

        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.DEBUG)

        '''
        # 输出不同级别的log
        logger.debug('this is debug info')
        logger.info('this is information')
        logger.warn('this is warning message')
        logger.error('this is error message')
        logger.fatal('this is fatal message, it is same as logger.critical')
        logger.critical('this is critical message')
        '''

        # return logger

    # 根据日期创建日志目录，并返回日志文件名
    def CreateLogFile(self, tmppath):
        print("创建LOG文件---------》")
        mytime = MyTime()
        path = tmppath + mytime.TimeFormatDay() + "\\"
        nowTime = mytime.TimeFormatSecondF()
        fileName = path + nowTime + '.log'

        # 如果路径不存在，则创建路径
        if os.path.exists(path) is False:
            os.makedirs(path)
            print("路径不存在，创建路径")
        else:
            pass

        # open(fileName, 'w').close()

        return fileName


'''
时间格式处理模块：
    整数时间戳
    年月日_时分秒
    时：分：秒
    年-月-日
'''


class MyTime():
    # 返回str，时间戳
    def TimeStamp(self):
        nowTime = time.time()
        nowTime = int(nowTime)
        nowTime = str(nowTime)
        return nowTime

    # 返回完整时间
    def TimeFormatAll(self):
        nowTime = wx.DateTime.Now().Format("%Y%m%d_%H%M%S")
        return nowTime

    # 返回时分秒
    def TimeFormatSecond(self):
        # nowTime = wx.DateTime.Now().Format("%H:%M:%S")
        nowTime = wx.DateTime.Now().FormatISOTime()
        return nowTime

    # 返回时分秒
    def TimeFormatSecondF(self):
        nowTime = wx.DateTime.Now().Format("%H%M%S")
        # nowTime = wx.DateTime.Now().FormatISOTime()
        return nowTime

    # 返回年月日
    def TimeFormatDay(self):
        # nowTime = wx.DateTime.Now().Format("%H:%M:%S")
        nowTime = wx.DateTime.Now().FormatISODate()
        return nowTime

    # 返回默认格式的完整时间
    def TimeFormat(self):
        nowTime = wx.DateTime.Now().FormatISOCombined()
        nowTime = nowTime.replace('T', ' ')
        return nowTime


# 获取测试集及测试音频


class MyFile():

    # 获取目录下指定测试集每一行的具体内容，并以列表形式返回
    def testlist(self, num, path):

        # 指定测试集
        testtxtfile = self.testtxt(path)
        testList = path + testtxtfile[num] + ".txt"
        try:
            f = open(testList, "r")
            line = f.readlines()
            testfile = []

            for i in line:
                i = i.replace("\n", "")  # 去掉换行符
                # print(i)
                testfile.append(i)

            f.close()
        except Exception as e:
            print("读取失败")
            print(e)
            return False

        return testfile

    # 获取目录下的所有mp3文件，并以列表形式返回
    def testmp3(self, path):

        testmp3file = []
        file = os.listdir(path)

        for f in file:
            if os.path.splitext(f)[1] == ".mp3":
                testmp3file.append(f)
        '''
        使用正则表达式提取mp3文件，会有一个txt没有屏蔽掉
        p1 = ".*?[.]mp3"
        pa = re.compile(p1)
        new = []

        #file = pa.findall(testmp3file)

        for f in file:
            new = re.match(p1,f)
            print (new)
            if new is None:
                file.remove(f)

        testmp3file = file
        print(testmp3file)
        '''

        return testmp3file

    # 获取目录下的所有txt文件，并以列表形式返回，去掉扩展名
    def testtxt(self, path):

        testtxtfile = []
        file = os.listdir(path)

        for f in file:
            if os.path.splitext(f)[1] == ".txt":
                name = os.path.splitext(f)[0]
                testtxtfile.append(name)

        return testtxtfile

    # 在指定路径新建txt
    def newtxt(self, name, path):
        print("生成TXT文件---------》")

        fileName = path + name + '.txt'
        print(fileName)

        # 如果路径不存在，则创建路径
        if os.path.exists(path) is False:
            os.makedirs(path)
            print("路径不存在，创建路径")
        else:
            pass

        try:
            open(fileName, 'x').close()
        except FileExistsError as e:
            print(e)
            return False

    # 在行末写入输入
    def writetxt(self, name, path, data):
        print("写入TXT文件---------》")

        fileName = path + name + '.txt'
        print(fileName)

        try:
            f = open(fileName, 'a+')
            f.write(data)
            f.write("\n")
        except Exception as e:
            print(e)
            return False

    # 删除指定内容
    def modifytxt(self, name, path, data):
        print("写入TXT文件---------》")

        fileName = path + name + '.txt'

        with open(fileName, 'r') as f:
            lines = f.readlines()

        with open(fileName, 'w') as f_w:
            for line in lines:
                if data in line:
                    continue
                f_w.write(line)

    # 删除指定CSV文件
    def deltxt(self, name, path):
        print("写入TXT文件---------》")

        fileName = path + name + '.txt'

        try:
            os.remove(fileName)
        except Exception as e:
            print(e)
            return False


# 音频播放器
class MyPlayer():
    myfile = MyFile()

    # mp3path = os.getcwd() + "//测试语音//"
    # mp3name = []
    # mp3file = mp3path + mp3name[0]
    # playerfg = True

    # 播放器初始化
    try:
        pygame.mixer.init()
    except Exception as e:
        print(e)

    # 实现指定路径、指定音频的播放功能
    def playmp3(self, mp3path, mp3name):
        filepath = mp3path
        filename = mp3name
        file = filepath + filename
        # print(file)

        # 播放器初始化
        try:
            pygame.mixer.init()
        except Exception as e:
            print(e)

        track = pygame.mixer.music.load(file)
        # print("开始播放：" + mp3name)
        pygame.mixer.music.play()
        # print(pygame.mixer.music.get_busy())
        # while(pygame.mixer.music.get_busy()):continue

    # 暂停
    def pausemp3(self):
        pygame.mixer.music.pause()

    # 继续
    def unpausemp3(self):
        pygame.mixer.music.unpause()

    # 停止
    def stopmp3(self):
        pygame.mixer.music.stop()

    # 判断是否有音频正在播放，该函数暂未使用
    def isPlayEnd(self):
        if pygame.mixer.music.get_busy():
            return False
        else:
            return True


class WorkerThread(threading.Thread):

    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageCount = "0"

    def stop(self):
        self.timeToQuit.set()

    def ThreadFinished(self, thread):
        pass


# UI及逻辑功能实现


class MyFrame(wx.Frame):
    myplayer = MyPlayer()
    myfile = MyFile()
    mylog = MyLog()
    mytime = MyTime()
    isPlayList = False
    time = 10
    repetition = 1

    def __init__(self):
        # 添加画板和工具标题
        wx.Frame.__init__(
            self, None, -1, "天猫精灵语音测试工具 " + version, size=(800, 800))
        # frame = wx.Frame(self)
        # frame.SetMinSize((300,600))   #设定UI可变化的最小尺寸，还存在问题
        # 添加画布，获取桌面尺寸，并最大化、居中、保持在其它窗口顶部显示
        self.panel = wx.Panel(self)
        c_x, c_y, c_w, c_h = wx.ClientDisplayRect()
        # self.fromx = c_w
        print(c_x, c_y, c_w, c_h)
        # logging.basicConfig(level=logging.DEBUG)
        # self.logger_UI.debug('屏幕尺寸：%d %d %d %d' % (c_x, c_y, c_w, c_h))
        # self.SetSize(wx.Size(c_w, c_h))
        # self.Center()
        self.SetBackgroundColour("LIGHT GREY")
        # self.ToggleWindowStyle(wx.STAY_ON_TOP)

        # 加快调试效率，屏蔽初始化检查
        self.Cfginit()

        self.AddMenu()
        self.AddPanel()
        self.AddSizer()

    # 配置初始化
    def Cfginit(self):
        global apppath
        global mp3path
        global tmppath

        # 播放器初始化
        try:
            pygame.mixer.init()
        except Exception as e:
            print(e)
            wx.MessageBox(str(e))

        # 检查当前程序运行的路径，并在该盘创建路径
        apppath = os.getcwd()
        # apppath = path[0] + ':/雷士生产智能化应用/'
        mp3path = apppath + "/测试语音/"
        tmppath = apppath + "/tmp/"
        # print(apppath, csvpath, tmppath)

        # 检查项目目录是否已经创建，没有则创建
        if os.path.exists(mp3path) is False:
            os.makedirs(mp3path)
            # print("测试语音路径不存在")
            wx.MessageBox("测试语音路径不存在，在当前路径创建")
        if os.path.exists(tmppath) is False:
            os.makedirs(tmppath)
            print("临时文件目录不存在，创建目录")
            # wx.MessageBox("测试语音路径不存在")

        # 启动日志模块
        logName = self.mylog.CreateLogFile(tmppath)
        self.mylog.LogCfg(logName)
        self.logger = logging.getLogger("APP")
        self.logger_UI = logging.getLogger("APP.UI")
        self.logger_Server = logging.getLogger("APP.Server")
        self.logger_Operter = logging.getLogger("APP.Operter")
        self.logger_Test = logging.getLogger("APP.Test")
        self.logger.info('App Start.........')

    # 添加菜单和状态栏，并绑定动作
    def AddMenu(self):
        # 创建一个菜单栏
        menubar = wx.MenuBar()
        # 创建一个系统菜单
        sysmenu = wx.Menu()

        choicedir = sysmenu.Append(-1, "选择目录",
                                  "选择测试音频所在的目录", kind=wx.ITEM_NORMAL)
        sysmenu.AppendSeparator()

        exit = sysmenu.Append(wx.ID_EXIT, "退出")

        # 添加菜单选项，并放到菜单指定位置
        # openfile = sysmenu.Insert(1, -1, "导入配置", "打开配置CSV文件", kind=wx.ITEM_NORMAL)
        # sysmenu.InsertSeparator(1)

        # choicedir = sysmenu.Insert(0, -1, "打开目录", "打开项目文件夹", kind=wx.ITEM_NORMAL)
        # sysmenu.InsertSeparator(1)

        # 绑定菜单事件
        self.Bind(wx.EVT_MENU, self.OnChoiceDir, choicedir)
        # self.Bind(wx.EVT_MENU, self.OnConfigbar, configbar)
        self.Bind(wx.EVT_MENU, self.OnExit, exit)
        # self.Bind(wx.EVT_MENU, self.OnOpenfile, openfile)
        # self.Bind(wx.EVT_MENU, self.OnBackup, savefile)
        # self.Bind(wx.EVT_MENU, self.OnUpload, upload)
        # self.Bind(wx.EVT_MENU, self.OnNetCheck, netcheck)
        # self.Bind(wx.EVT_MENU, self.OnPrinterCheck, printercheck)

        # 绑定窗口关闭事件，导致程序无法关闭，问题已修复
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # 创建帮助菜单
        helpmenu = wx.Menu()
        helptext = helpmenu.Append(-1, "帮助", "打开帮助文档")
        about = helpmenu.Append(-1, "关于", "查看软件信息")

        self.Bind(wx.EVT_MENU, self.OnHelptext, helptext)
        self.Bind(wx.EVT_MENU, self.OnAbout, about)

        # 添加菜单到菜单栏
        menubar.Append(sysmenu, "系统")
        menubar.Append(helpmenu, "帮助")

        self.SetMenuBar(menubar)
        '''
        # 创建工具栏，不使用工具栏
        toolbar = self.CreateToolBar()
        qtool = toolbar.AddTool(wx.ID_ANY, "退出", wx.Bitmap('love.png'))
        toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnExit, qtool)
        '''
        # 创建状态栏
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths([-3, -1, -1, -2])
        # nowTime = datetime.now().strftime("%Y%m%d %H%M%S")
        # self.statusbar.SetStatusText(nowTime, 1)
        self.statusbar.SetStatusText('天猫精灵语音测试工具 by Mild Yang', 3)

    # 添加页面元素并绑定动作
    def AddPanel(self):
        panel = self.panel
        # 空白行
        # self.label = wx.StaticText(panel, -1, "")

        # 添加语音集标题及选择框，并绑定事件
        self.labelList = wx.StaticText(panel, -1, "选择用例")
        currentList = self.myfile.testtxt(mp3path)
        self.choiceList = wx.Choice(
            panel, -1, choices=currentList)
        self.Bind(wx.EVT_CHOICE, self.OnChoiceList, self.choiceList)

        # 添加测试集控制按钮
        self.buttonStartTest = wx.Button(panel, -1, "开始测试", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.StartTest, self.buttonStartTest)
        self.buttonStopTest = wx.Button(panel, -1, "停止测试", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.btnStopTest, self.buttonStopTest)

        # 调整语音间隔时间
        self.setTime = wx.StaticText(panel, -1, "语音间隔")
        self.textTime = wx.TextCtrl(panel, -1, value=str(self.time),
                                    size=(75, 25),
                                    style=wx.TE_PROCESS_ENTER | wx.TE_CENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OntextTime, self.textTime)

        # 设置重复次数
        self.setRep = wx.StaticText(panel, -1, "重复次数")
        self.textRep = wx.TextCtrl(panel, -1, value=str(self.repetition),
                                   size=(75, 25),
                                   style=wx.TE_PROCESS_ENTER | wx.TE_CENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OntextRep, self.textRep)

        # 用例管理
        self.buttonAddCase = wx.Button(panel, -1, "新增用例", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.OnaddCase, self.buttonAddCase)
        self.buttonDelCase = wx.Button(panel, -1, "删除用例", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.OndelCase, self.buttonDelCase)
        # currentList = self.myfile.testtxt(mp3path)
        self.addList = wx.ComboBox(panel, -1, value="请输入新用例名称或选择已有用例",
                                   choices=currentList,
                                   style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnaddList, self.addList)
        # self.Bind(wx.EVT_TEXT, self.OnaddCase, self.addList)

        currentFile = self.myfile.testmp3(mp3path)
        self.allList = wx.ListBox(panel, -1, choices=currentFile,
                                  style=wx.LB_SINGLE | wx.LB_SORT)
        # self.Bind(wx.EVT_LISTBOX, self.OnChoiceFile, self.choiceFile)

        self.buttonAddAudio = wx.Button(panel, -1, ">>", size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnbtnAddAudio, self.buttonAddAudio)
        self.buttonDelAudio = wx.Button(panel, -1, "<<", size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnbtnDelAudio, self.buttonDelAudio)

        self.newList = wx.ListBox(panel, -1,
                                  style=wx.LB_SINGLE)
        # self.Bind(wx.EVT_LISTBOX, self.OnChoiceFile, self.choiceFile)

        # 添加音频文件选择框，并绑定事件
        currentFile = self.myfile.testmp3(mp3path)
        self.choiceFile = wx.ListBox(panel, -1, choices=currentFile,
                                     style=wx.LB_SINGLE | wx.LB_SORT)
        self.Bind(wx.EVT_LISTBOX, self.OnChoiceFile, self.choiceFile)

        # 添加音频文件控制按钮
        self.buttonStart = wx.Button(panel, -1, "开始播放", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.btnStart, self.buttonStart)

        self.buttonPause = wx.Button(panel, -1, "暂停播放", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.btnPause, self.buttonPause)

        self.buttonUnpause = wx.Button(panel, -1, "继续播放", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.btnUnpause, self.buttonUnpause)

        self.buttonStop = wx.Button(panel, -1, "停止播放", size=(75, 25))
        self.Bind(wx.EVT_BUTTON, self.btnStop, self.buttonStop)

        # 添加信息展示标题及窗口
        self.labelInfo = wx.StaticText(panel, -1, "用例详情:")
        self.textInfo = wx.TextCtrl(
            panel, -1, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # 添加测试LOG展示标题及窗口
        self.labelLog = wx.StaticText(panel, -1, "测试记录:")
        self.textLog = wx.TextCtrl(
            panel, -1, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # 绑定定时器事件
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1, self.timer1)
        # self.timer1.Start(1000)

        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.timer2)

    # 添加页面布局
    def AddSizer(self):

        # 测试用例容器
        boxCase = wx.StaticBox(self.panel, -1, "测试用例")
        CaseSizer = wx.StaticBoxSizer(boxCase, wx.HORIZONTAL)
        CaseSizer.Add(self.labelList, 0, wx.ALL, border=5)
        CaseSizer.Add(self.choiceList, 1, wx.EXPAND | wx.ALL, border=5)

        # 测试控制容器
        boxbtnTest = wx.StaticBox(self.panel, -1, "测试控制")
        btnTestSizer = wx.StaticBoxSizer(boxbtnTest, wx.HORIZONTAL)
        btnTestSizer.Add(self.buttonStartTest, 0, wx.ALL, border=5)
        btnTestSizer.Add(self.buttonStopTest, 0, wx.ALL, border=5)

        # 测试设置容器
        boxSetTest = wx.StaticBox(self.panel, -1, "其它设置")
        SetTestSizer = wx.StaticBoxSizer(boxSetTest, wx.HORIZONTAL)
        SetTestSizer.Add(self.setTime, 0, wx.ALL, border=5)
        SetTestSizer.Add(self.textTime, 1, wx.EXPAND | wx.ALL, border=5)
        SetTestSizer.Add(self.setRep, 0, wx.ALL, border=5)
        SetTestSizer.Add(self.textRep, 1, wx.EXPAND | wx.ALL, border=5)

        # 用例管理容器
        AddSizer = wx.BoxSizer(wx.HORIZONTAL)
        # AddSizer.Add(self.addList, 1, wx.EXPAND | wx.ALL, border=5)
        AddSizer.Add(self.buttonAddCase, 0, wx.ALL, border=5)
        AddSizer.Add(self.buttonDelCase, 0, wx.ALL, border=5)

        btnAudioSizer = wx.BoxSizer(wx.VERTICAL)
        btnAudioSizer.Add(self.buttonAddAudio, 0, wx.ALIGN_CENTER)
        btnAudioSizer.Add(self.buttonDelAudio, 0, wx.ALIGN_CENTER)

        ControlSizer = wx.BoxSizer(wx.HORIZONTAL)
        ControlSizer.Add(self.allList, 1, wx.EXPAND | wx.ALL, border=5)
        ControlSizer.Add(btnAudioSizer, 0)
        ControlSizer.Add(self.newList, 1, wx.EXPAND | wx.ALL, border=5)

        boxManage = wx.StaticBox(self.panel, -1, "用例管理")
        ManageSizer = wx.StaticBoxSizer(boxManage, wx.VERTICAL)
        ManageSizer.Add(self.addList, 0, wx.EXPAND | wx.ALL, border=5)
        ManageSizer.Add(AddSizer, 0, wx.EXPAND)
        ManageSizer.Add(ControlSizer, 0, wx.EXPAND)

        # 测试容器
        TestSizer = wx.BoxSizer(wx.VERTICAL)
        TestSizer.Add(CaseSizer, 0, wx.EXPAND)
        TestSizer.Add(btnTestSizer, 0, wx.EXPAND)
        TestSizer.Add(SetTestSizer, 0, wx.EXPAND)
        TestSizer.Add(ManageSizer, 0, wx.EXPAND)

        # 音频控制容器
        playSizer = wx.BoxSizer(wx.HORIZONTAL)
        playSizer.Add(self.buttonStart, 0, wx.ALL, border=5)
        playSizer.Add(self.buttonPause, 0, wx.ALL, border=5)
        playSizer.Add(self.buttonUnpause, 0, wx.ALL, border=5)
        playSizer.Add(self.buttonStop, 0, wx.ALL, border=5)

        # 播放器容器
        boxPlayList = wx.StaticBox(self.panel, -1, "音频列表")
        PlayListSizer = wx.StaticBoxSizer(boxPlayList, wx.VERTICAL)
        PlayListSizer.Add(self.choiceFile, 1, wx.EXPAND | wx.ALL, border=5)
        PlayListSizer.Add(playSizer, 0, wx.EXPAND)

        # 主界面容器
        AppSizer = wx.BoxSizer(wx.HORIZONTAL)
        AppSizer.Add(TestSizer, 1, wx.ALL | wx.EXPAND, border=5)
        AppSizer.Add(PlayListSizer, 1, wx.ALL | wx.EXPAND, border=5)

        # 用例详情容器
        detailSizer = wx.BoxSizer(wx.VERTICAL)
        detailSizer.Add(self.labelInfo, 0, wx.ALL | wx.EXPAND, border=5)
        detailSizer.Add(self.textInfo, 1, wx.ALL | wx.EXPAND, border=5)

        # 测试记录容器
        recordSizer = wx.BoxSizer(wx.VERTICAL)
        recordSizer.Add(self.labelLog, 0, wx.ALL | wx.EXPAND, border=5)
        recordSizer.Add(self.textLog, 1, wx.ALL | wx.EXPAND, border=5)

        # 信息展示容器
        infoSizer = wx.BoxSizer(wx.HORIZONTAL)
        infoSizer.Add(detailSizer, 1, wx.ALL | wx.EXPAND, border=5)
        infoSizer.Add(recordSizer, 1, wx.ALL | wx.EXPAND, border=5)

        # 添加主容器，并按添加顺序布局
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(AppSizer, 3, wx.ALL | wx.EXPAND, border=5)
        mainSizer.Add(infoSizer, 2, wx.ALL | wx.EXPAND, border=5)

        self.panel.SetSizer(mainSizer)
        self.panel.SetAutoLayout(True)
        # 不添加此行布局会混乱
        mainSizer.Fit(self.panel)
        mainSizer.Layout()

    # 选择测试音频目录
    def OnChoiceDir(self, event):
        print("选择测试音频目录---------》")
        global mp3path

        dlg = wx.DirDialog(self, '选择测试音频所在目录：',
                           defaultPath=mp3path,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            mp3path = dlg.GetPath()
            self.Oninfo(status='选择目录：' + dlg.GetPath(),
                        level="prompt",
                        Box=False,
                        Allsame=True)
            # os.startfile(dlg.GetPath())
            currentList = self.myfile.testtxt(mp3path)
            currentFile = self.myfile.testmp3(mp3path)
            self.newList.Clear()
            self.textInfo.Clear()
            self.addList.Set(currentList)
            self.choiceList.Set(currentList)
            self.allList.Set(currentFile)
            self.choiceFile.Set(currentFile)
        elif result == wx.ID_CANCEL:
            pass
        dlg.Destroy()

    # 菜单退出程序动作
    def OnExit(self, event):
        self.Close(True)

    # 打开帮助文档，待补充
    def OnHelptext(self, event):
        wx.MessageBox("没得帮助信息，哈哈！")

    # 关于
    def OnAbout(self, event):
        wx.MessageBox("也没得其它相关信息，略！")

    # 关闭窗口动作，检查生产状态，检查临时图片
    def OnCloseWindow(self, event):
        dlg = wx.MessageDialog(None, '关闭应用程序，是否继续？',
                               '警告', wx.YES_NO | wx.YES_DEFAULT |
                               wx.ICON_EXCLAMATION)
        result = dlg.ShowModal()
        # print(result)
        # print(wx.ID_YES, wx.ID_NO)
        dlg.Destroy()

        if result == wx.ID_YES:
            self.Destroy()
        elif result == wx.ID_NO:
            pass

    def OnTimer1(self, event):
        if pygame.mixer.music.get_busy():
            pass
        elif self.isPlayList is True:
            self.timer1.Stop()
            self.timer2.Start(self.time * 1000)

            if(len(self.mp3List) > 0):
                self.Oninfo(status="指令结束，等待 " + str(self.time) + "秒 开始下一条指令...",
                            level="prompt", Box=False, Allsame=True)
            elif self.repetition > 1:
                self.repetition -= 1
                print(self.repetition)
                self.GetCase()
                self.Oninfo(status="第 " + str(int(self.textRep.GetValue()) - self.repetition) + "次 测试结束",
                            level="prompt", Box=False, Allsame=True)
            else:
                self.isPlayList = False
                self.timer2.Stop()
                self.Oninfo(status="测试结束！！！",
                            level="prompt", Box=False, Allsame=True)

    def OnTimer2(self, event):
        myplayer = MyPlayer()
        global mp3path

        mp3 = self.mp3List[0]
        self.Oninfo(status="开始播放：" + mp3,
                    level="prompt", Box=False, Allsame=True)
        myplayer.playmp3(mp3path, mp3)
        # self.mp3List.pop[0]
        del self.mp3List[0]
        self.timer2.Stop()
        self.timer1.Start(1000)

    # 语音集选择框事件，在语音信息展示窗口显示语音集内容
    def OnChoiceList(self, event):
        # print("选我")
        num = self.choiceList.GetSelection()  # 所选语音集的序号
        # print(num)
        content = self.choiceList.GetStringSelection()  # 所选语音集的名称
        self.textInfo.Clear()
        self.Oninfo(status="选择测试用例：" + content,
                    level="prompt", Box=False, Allsame=True)
        self.textInfo.AppendText(content + "包含如下语音指令：\n")
        i = 0
        while(i < len(self.myfile.testtxt(mp3path))):
            if(num == i):
                for l in self.myfile.testlist(i, mp3path):
                    self.textInfo.AppendText(l)
                    self.textInfo.AppendText("\n")
            i += 1

    def OnaddList(self, event):
        num = self.addList.GetSelection()  # 所选语音集的序号
        print(num)
        content = self.addList.GetStringSelection()  # 所选语音集的名称
        self.newList.Clear()
        self.Oninfo(status="修改测试用例：" + content,
                    level="prompt", Box=False, Allsame=True)
        i = 0
        while(i < len(self.myfile.testtxt(mp3path))):
            if(num == i):
                self.newList.Set(self.myfile.testlist(i, mp3path))
            i += 1

    def OnaddCase(self, event):
        global mp3path
        newCaseName = self.addList.GetValue()
        print(newCaseName)
        
        if self.myfile.newtxt(newCaseName, mp3path) is False:
            wx.MessageBox("用例已存在！")
        else:
            currentList = self.myfile.testtxt(mp3path)
            # self.addList.Clear()
            # self.addList.Clear()
            self.addList.Set(currentList)
            self.choiceList.Set(currentList)

    def OndelCase(self, event):
        content = self.addList.GetStringSelection()  # 所选语音集的名称

        if len(content) < 1:
            print("未选择用例")
        else:
            dlg = wx.MessageDialog(None, '删除测试用例，是否继续？',
                                   '警告', wx.YES_NO | wx.NO_DEFAULT |
                                   wx.ICON_EXCLAMATION)
            result = dlg.ShowModal()
            # print(result)
            # print(wx.ID_YES, wx.ID_NO)
            dlg.Destroy()

            if result == wx.ID_YES:
                self.myfile.deltxt(content, mp3path)
                currentList = self.myfile.testtxt(mp3path)
                self.newList.Clear()
                # self.addList.Clear()
                # self.addList.Clear()
                self.addList.Set(currentList)
                self.choiceList.Set(currentList)
                self.Oninfo(status="删除测试用例：" + content,
                            level="prompt", Box=False, Allsame=True)
            elif result == wx.ID_NO:
                pass
        

    def OnbtnAddAudio(self, event):
        mp3 = self.allList.GetStringSelection()
        # print(mp3)
        if len(mp3) < 1:
            print("未选择音频")
        else:
            self.newList.Append(mp3)

            content = self.addList.GetStringSelection()  # 所选语音集的名称
            self.myfile.writetxt(content, mp3path, mp3)

    def OnbtnDelAudio(self, event):
        mp3 = self.newList.GetStringSelection()
        if len(mp3) < 1:
            print("未选择音频")
        else:
            num = self.newList.GetSelection()
            self.newList.Delete(num)

            content = self.addList.GetStringSelection()  # 所选语音集的名称
            self.myfile.modifytxt(content, mp3path, mp3)

    # 音频文件选择框事件，在Log展示窗口显示选择的音频文件名称
    def OnChoiceFile(self, event):
        content = self.choiceFile.GetStringSelection()
        self.Oninfo(status="选择音频：" + content,
                    level="prompt", Box=False, Allsame=True)

    # 语音集控制按钮事件，实现测试集播放功能
    def btnStartTest(self, event):
        print("来了")
        th = WorkerThread()
        wx.CallAfter(self.StartTest)
        msg = "正在播放测试集哟"
        if th.timeToQuit.isSet():
            print("哟哟")
            wx.CallAfter(self.StartTest, msg)
        else:
            pass

        '''
        print("a")
        p = multiprocessing.Process(target=MyFrame.StartTest)
        p.start()
        print("b")
        '''
        '''
        # threads = []
        t1 = threading.Thread(target=self.StartTest)
        # self.threads.append(t1)
        t1.start()
        t1.join()
        print("b")
        '''

    # 开始测试用例
    def StartTest(self, enent):
        self.isPlayList = True
        self.time = int(self.textTime.GetValue())
        self.repetition = int(self.textRep.GetValue())

        self.GetCase()

        self.timer2.Start(1000)

    # 停止测试用例
    def btnStopTest(self, event):
        self.isPlayList = False
        self.timer1.Stop()
        self.timer2.Stop()
        self.myplayer.stopmp3()
        self.Oninfo(status="停止测试！！！",
                    level="prompt", Box=False, Allsame=True)

    # 获取测试用例详情
    def GetCase(self):
        num = self.choiceList.GetSelection()
        self.mp3List = self.myfile.testlist(num, mp3path)

    # 语音间隔时间设置，拖动条方式
    def OnsliderTime(self, event):
        self.time = int(self.sliderTime.GetValue())
        # print(self.time)
        self.Oninfo(status="设定语言间隔时间为：" + str(self.time) + "秒",
                    level="prompt", Box=False, Allsame=True)
        # self.textTime.Clear()

    # 语音间隔时间设置
    def OntextTime(self, event):
        self.time = int(self.textTime.GetValue())
        # print(self.time)
        self.Oninfo(status="设定语言间隔时间为：" + str(self.time) + "秒",
                    level="prompt", Box=False, Allsame=True)
        # self.textTime.Clear()

    # 语音间隔时间设置
    def OntextRep(self, event):
        self.repetition = int(self.textRep.GetValue())
        # print(self.time)
        self.Oninfo(status="设定测试用例重复次数为：" + str(self.repetition) + "次",
                    level="prompt", Box=False, Allsame=True)
        # self.textTime.Clear()

    # 音频控制按钮事件，实现音频文件控制功能
    def btnStart(self, event):
        global mp3path
        mp3 = self.choiceFile.GetStringSelection()
        self.Oninfo(status="开始播放...", level="prompt",
                    Box=False, Allsame=True)
        self.myplayer.playmp3(mp3path, mp3)

    def btnStop(self, event):
        self.myplayer.stopmp3()
        # print("停止播放！")
        self.Oninfo(status="停止播放！", level="prompt",
                    Box=False, Allsame=True)

    def btnPause(self, event):
        self.Oninfo(status="暂停播放...", level="prompt",
                    Box=False, Allsame=True)
        self.myplayer.pausemp3()

    def btnUnpause(self, event):
        self.Oninfo(status="继续播放...", level="prompt",
                    Box=False, Allsame=True)
        self.myplayer.unpausemp3()

    def delay(self):
        # self.time = t
        time.sleep(self.time)

    # 信息提示函数，状态栏、操作提示、操作记录、信息提示框
    # 操作信息分级显示，prompt提示绿色，warning警告橙色，error错误红色
    def Oninfo(self, status, level,
               operater=None, log=None, message=None, Box=False, Allsame=True):
        mytime = self.mytime
        if level is "prompt":
            status = "提示：" + status
            self.textLog.SetForegroundColour('SLATE BLUE')
            self.logger_Operter.info(status)
        elif level is "warning":
            status = "警告：" + status
            self.textLog.SetForegroundColour('CORAL')
            self.logger_Operter.warning(status)
        elif level is "error":
            status = "错误：" + status
            self.textLog.SetForegroundColour('RED')
            self.logger_Operter.error(status)

        if Allsame is True:
            operater = status
            log = status
            message = status
        else:
            pass
        self.statusbar.SetStatusText(status)
        # self.labelOperation.SetValue(operater)
        self.textLog.AppendText(mytime.TimeFormatSecond() +
                                "  " + log + "\n")
        if Box is True:
            wx.MessageBox(message)


class App(wx.App):

    def OnInit(self):
        '''
        bmp = wx.Image("cat.png").ConvertToBitmap()
        wx.adv.SplashScreen(bmp,
                            wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                            3000, None, -1)
        wx.Yield()
        '''
        self.frame = MyFrame()
        self.frame.Show()
        # self.SetTopWindow(self.frame)
        return True


def main():
    logger = logging.getLogger("APP")
    app = App()
    app.MainLoop()
    logger.info('App Close.........')


if __name__ == '__main__':

    main()

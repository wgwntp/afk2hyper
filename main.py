import win32gui   
import win32api  
import time 
import pyautogui 

import os
import threading
import cv2
import numpy as np
from PIL import Image 
import tkinter as tk
import queue
from tkinter import scrolledtext

from tkinter import messagebox
import event
import cus_enum
import turbo
import config
import utils
import log
import page_test

# 卡片模板路径  
CARDS_PATH = './images/cards'
# 当前选择句柄，默认:0
hwnd = 0
# 当前运行模式，默认:蒸馏史诗
draw_mode = cus_enum.DrawMode.TURBO_DRAW_EPIC
# 是否暂停
paused = False
# 创建一个全局的队列对象,用于在线程之间传递消息  
message_queue = queue.Queue()
# 当前剩余白票数量
white_tickets = 0
# 当前剩余红票数量
red_tickets = 0
# 当前剩余神魔球数量
ball_tickets = 0
# 窗口期分钟开始时间,默认:58
limit_begin_m = 58
# 窗口期分钟结束时间,默认:3
limit_end_m = 3
# 窗口期小时开始时间,默认:1
limit_begin_h = 1
# 窗口期小时结束时间,默认:5
limit_end_h = 5

# 检查消息队列
# 参数:无
# 返回值:无
# 用于在主线程中检查队列并更新GUI
def check_queue():  
    try:  
        # 从队列中获取一条消息（如果队列为空，则此调用将阻塞直到有消息可用）  
        message = message_queue.get_nowait()
        # 更新GUI（例如，在Text组件中添加一条日志）  
        log_text.insert(tk.END, message + "\n")  
        log_text.see(tk.END)  # 确保滚动条显示到最后
        root.after(100, check_queue)
    except queue.Empty:  
        # 如果队列为空，则重新安排此函数稍后再次调用
        root.after(100, check_queue)  # 100毫秒后再次检查队列
      
def get_all_windows():  
    # 获取桌面窗口句柄  
    # hwnd_desktop = win32gui.GetDesktopWindow()  
    # 初始化一个空列表来存储窗口句柄  
    windows = []  
 
    # 枚举所有顶级窗口  
    def foreach_window(hwnd, lParam):  
        if win32gui.IsWindowVisible(hwnd): 
            title = win32gui.GetWindowText(hwnd)
            if title != "":
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))  
 
    # 使用 EnumWindows 函数枚举所有顶级窗口  
    win32gui.EnumWindows(foreach_window, 0)  
    return windows  

def changeFullCardWishList(hwnd,ocr_result):
    targetWishList = ["1","2","7","8","15","16","22","23","29","30","35","36","42","43","48","49"]
    utils.clickIntoByButtonName(hwnd,'心愿单',ocr_result)
    time.sleep(0.2)
    #截图
    imagePath,w,h = utils.window_screenshot(hwnd)
    print(w,",",h)
    image = cv2.imread(imagePath)
    #按当前窗口尺寸调整模板比例
    calW,calH =  utils.reCalTemplateSize(w,h,0.08,0.05)
    #读取所有英雄图片
    cardsMap = []
    for filename in os.listdir(CARDS_PATH):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = cv2.imread(CARDS_PATH + '/' + filename)
            resized_img = cv2.resize(img, (calW, calH), interpolation=cv2.INTER_AREA)
            cardsMap.append([filename.split('.')[0] ,resized_img])
    currentWishList = []
    for cm in cardsMap:
        cardNumber = cm[0]
        card = cm[1]
        # 获取模板的宽度和高度  
        _, w, h = card.shape[::-1]
        # 使用matchTemplate函数在大图中搜索模板  
        res = cv2.matchTemplate(image, card, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.8
        loc = np.where(res >= threshold)  
        
        # 在原图上绘制矩形框，标记出匹配的位置
        pts = list(zip(*loc[::-1]))
        if len(pts)>0 :
            pt = pts[0]
            currentWishList.append([cardNumber,pt])
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    for cwl in currentWishList:
        if cwl[0] not in targetWishList:
            pyautogui.click(cwl[1][0],cwl[1][1])
            time.sleep(0.3)
            #截图
            selectImagePath,sw,sh = utils.window_screenshot(hwnd)
            ocr_select_result = config.READER.readtext(selectImagePath)
            #按比例重新计算模板尺寸
            CARDS_SWAP_WIDTH_RATIO = 0.104
            CARDS_SWAP_HEIGHT_RATIO = 0.062 
            calW = int(sw * CARDS_SWAP_WIDTH_RATIO)
            calH = int(sh * CARDS_SWAP_HEIGHT_RATIO)
            wishLIstCardsMap = []
            for filename in os.listdir(CARDS_PATH):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    if filename.split('.')[0] in targetWishList:
                        t_img = cv2.imread(CARDS_PATH + '/' + filename)
                        resized_img = cv2.resize(t_img, (calW, calH), interpolation=cv2.INTER_AREA)
                        wishLIstCardsMap.append([filename.split('.')[0] ,resized_img])
            selectImage = cv2.imread(selectImagePath)
            swapCard=[]
            for cm in wishLIstCardsMap:
                cardNumber = cm[0]
                card = cm[1]
                # 获取模板的宽度和高度  
                _, w, h = card.shape[::-1]
                # 使用matchTemplate函数在大图中搜索模板  
                res = cv2.matchTemplate(selectImage, card, cv2.TM_CCOEFF_NORMED)  
                # 设置一个阈值，用于确定匹配的程度  
                threshold = 0.8
                loc = np.where(res >= threshold)
                 # 在原图上绘制矩形框，标记出匹配的位置
                pts = list(zip(*loc[::-1]))
                if len(pts)>0 :
                    pt = pts[0]
                    swapCard = pt
                    break
            pyautogui.click(swapCard[0],swapCard[1])
            utils.clickIntoByButtonName(hwnd,"保存编辑",ocr_select_result)
            os.remove(selectImagePath)
            time.sleep(0.3)
    # # 显示结果图像  
    # cv2.imshow('Detected Rectangles', image)  
    # cv2.waitKey(0)  
    # cv2.destroyAllWindows()
    #删除截图
    os.remove(imagePath)
    
def changeEpicCardWishList(hwnd):
    targetWishList = ["29","30","15","42","43"]
    #截图
    imagePath,w,h = utils.window_screenshot(hwnd)
    print(w,",",h)
    #按比例重新计算模板尺寸
    CARDS_WIDTH_RATIO = 0.104
    CARDS_HEIGHT_RATIO = 0.062 
    calW = int(w * CARDS_WIDTH_RATIO)
    calH = int(h * CARDS_HEIGHT_RATIO)
    image = cv2.imread(imagePath)
    #读取所有英雄图片
    cardsMap = []
    for filename in os.listdir(CARDS_PATH):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = cv2.imread(CARDS_PATH + '/' + filename)
            resized_img = cv2.resize(img, (calW, calH), interpolation=cv2.INTER_AREA)
            cardsMap.append([filename.split('.')[0] ,resized_img])
    currentWishList = []
    currentWishListCardNumber = []
    for cm in cardsMap:
        cardNumber = cm[0]
        card = cm[1]
        # 获取模板的宽度和高度  
        _, w, h = card.shape[::-1]
        # 使用matchTemplate函数在大图中搜索模板  
        res = cv2.matchTemplate(image, card, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.8
        loc = np.where(res >= threshold)
        
    for cm in cardsMap:
        cardNumber = cm[0]
        card = cm[1]
        # 获取模板的宽度和高度  
        _, w, h = card.shape[::-1]
        # 使用matchTemplate函数在大图中搜索模板  
        res = cv2.matchTemplate(image, card, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.8
        loc = np.where(res >= threshold)  
        
        # 在原图上绘制矩形框，标记出匹配的位置
        pts = list(zip(*loc[::-1]))
        if len(pts)>0 :
            pt = pts[0]
            currentWishList.append([cardNumber,pt])
            currentWishListCardNumber.append(cardNumber)
    #找到缺少的目标心愿单卡
    needAddList = []
    for target in targetWishList:
        if target not in currentWishListCardNumber:
            needAddList.append(target)
    i = 0
    for cwl in currentWishList:
        if cwl[0] not in targetWishList:
            pyautogui.click(cwl[1][0],cwl[1][1])
            time.sleep(0.3)
            #截图
            selectImagePath,sw,sh = utils.window_screenshot(hwnd)
            ocr_select_result = config.READER.readtext(selectImagePath)
            selectImage = cv2.imread(selectImagePath)
            #按比例重新计算模板尺寸
            CARDS_SWAP_WIDTH_RATIO = 0.104
            CARDS_SWAP_HEIGHT_RATIO = 0.062 
            calW = int(sw * CARDS_SWAP_WIDTH_RATIO)
            calH = int(sh * CARDS_SWAP_HEIGHT_RATIO)
            wishLIstCardsMap = []
            
            for filename in os.listdir(CARDS_PATH):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    if filename.split('.')[0] == needAddList[i]:
                        i += 1
                        t_img = cv2.imread(CARDS_PATH + '/' + filename)
                        resized_img = cv2.resize(t_img, (calW, calH), interpolation=cv2.INTER_AREA)
                        wishLIstCardsMap.append([filename.split('.')[0] ,resized_img])
                        break
            
            swapCard=[]
            isFindSwapCard = False
            while True:
                for cm in wishLIstCardsMap:
                    cardNumber = cm[0]
                    card = cm[1]
                    # 获取模板的宽度和高度  
                    _, w, h = card.shape[::-1]
                    # 使用matchTemplate函数在大图中搜索模板  
                    res = cv2.matchTemplate(selectImage, card, cv2.TM_CCOEFF_NORMED)  
                    # 设置一个阈值，用于确定匹配的程度  
                    threshold = 0.8
                    loc = np.where(res >= threshold)
                    pts = list(zip(*loc[::-1]))
                    if len(pts)>0 :
                        pt = pts[0]
                        swapCard = pt
                        # cv2.rectangle(selectImage, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2) 
                        isFindSwapCard = True
                        break
                # cv2.imshow('Detected', selectImage)  
                # cv2.waitKey(0) 
                if isFindSwapCard:
                    break
 
                moveToX = int(sw / 2) 
                moveToY = int(sh / 2) + 200
                pyautogui.moveTo(moveToX, moveToY, duration=0.1)
                pyautogui.dragTo(moveToX,moveToY - 300, button='left',duration=0.3)
                time.sleep(0.3)
                scrollImagePath,sw,sh = utils.window_screenshot(hwnd)
                selectImage = cv2.imread(scrollImagePath)
                os.remove(scrollImagePath)
            os.remove(selectImagePath)  
            pyautogui.click(swapCard[0],swapCard[1])
            utils.clickIntoByButtonName(hwnd,"保存编辑",ocr_select_result)
            time.sleep(0.3)
    os.remove(imagePath)
    
def changeStarOriginWishList(hwnd):
    targetWishList = "55"
    #截图
    imagePath,w,h = utils.window_screenshot(hwnd)
    print(w,",",h)
    #按比例重新计算模板尺寸
    CARDS_WIDTH_RATIO = 0.109
    CARDS_HEIGHT_RATIO = 0.06 
    calW = int(w * CARDS_WIDTH_RATIO)
    calH = int(h * CARDS_HEIGHT_RATIO)
    image = cv2.imread(imagePath)
    #读取所有神魔图片
    cardsMap = []
    for filename in os.listdir(CARDS_PATH):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            if int(filename.split(".")[0]) >= 52:
                img = cv2.imread(CARDS_PATH + '/' + filename)
                resized_img = cv2.resize(img, (calW, calH), interpolation=cv2.INTER_AREA)
                cardsMap.append([filename.split('.')[0] ,resized_img])
    currentCard = []
    for cm in cardsMap:
        cardNumber = cm[0]
        card = cm[1]
        # 获取模板的宽度和高度  
        _, w, h = card.shape[::-1]
        # 使用matchTemplate函数在大图中搜索模板  
        res = cv2.matchTemplate(image, card, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.8
        loc = np.where(res >= threshold)
        # 在原图上绘制矩形框，标记出匹配的位置
        pts = list(zip(*loc[::-1]))
        if len(pts)>0 :
            pt = pts[0]
            currentCard=[cardNumber,pt]
    if currentCard[0] != targetWishList:
        pyautogui.click(currentCard[1][0],currentCard[1][1])
        time.sleep(0.3)
        selectImagePath,sw,sh = utils.window_screenshot(hwnd)
        ocr_select_result = config.READER.readtext(selectImagePath)
        selectImage = cv2.imread(selectImagePath)
        #按比例重新计算模板尺寸
        CARDS_SWAP_WIDTH_RATIO = 0.099
        CARDS_SWAP_HEIGHT_RATIO = 0.055 
        calW = int(sw * CARDS_SWAP_WIDTH_RATIO)
        calH = int(sh * CARDS_SWAP_HEIGHT_RATIO)
        wishLIstCard = [] 
        for filename in os.listdir(CARDS_PATH):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                if filename.split('.')[0] == targetWishList :
                    t_img = cv2.imread(CARDS_PATH + '/' + filename)
                    resized_img = cv2.resize(t_img, (calW, calH), interpolation=cv2.INTER_AREA)
                    wishLIstCard=[filename.split('.')[0] ,resized_img]
                    break
        cardNumber = wishLIstCard[0]
        card = wishLIstCard[1]
        # 获取模板的宽度和高度  
        _, w, h = card.shape[::-1]
        # 使用matchTemplate函数在大图中搜索模板  
        res = cv2.matchTemplate(selectImage, card, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.8
        loc = np.where(res >= threshold)
        pts = list(zip(*loc[::-1]))
        if len(pts)>0 :
            pt = pts[0]
            swapCard = pt
            # cv2.rectangle(selectImage, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2) 
        pyautogui.click(swapCard[0],swapCard[1])
        utils.clickIntoByButtonName(hwnd,"保存编辑",ocr_select_result)
        time.sleep(0.3)
#抽卡模式
def draw_cards_mode(): 
    message_queue.put(f"进入抽卡模式")  
    full_list_line = [
        [cus_enum.PageType.START_PAGE,'点击开始游戏'],
        [cus_enum.PageType.PAUSE_PAGE,'点击屏幕恢复'],
        [cus_enum.PageType.MAIN_PAGE,'神秘屋'],
        [cus_enum.PageType.SHEN_MI_WU,'月桂酒馆'],
        [cus_enum.PageType.UP_DRAW,'全英雄招募'],
        [cus_enum.PageType.OTHER_PAGE,'点击空白处关闭']
    ]
    
    epic_list_line = [
        [cus_enum.PageType.START_PAGE,'点击开始游戏'],
        [cus_enum.PageType.PAUSE_PAGE,'点击屏幕恢复'],
        [cus_enum.PageType.MAIN_PAGE,'神秘屋'],
        [cus_enum.PageType.SHEN_MI_WU,'月桂酒馆'],
        [cus_enum.PageType.UP_DRAW,'史诗招募'],
        [cus_enum.PageType.FULL_CARD_DRAW,'史诗招募'],
        [cus_enum.PageType.OTHER_PAGE,'点击空白处关闭']
    ]
    
    star_origin_line = [
        [cus_enum.PageType.START_PAGE,'点击开始游戏'],
        [cus_enum.PageType.PAUSE_PAGE,'点击屏幕恢复'],
        [cus_enum.PageType.MAIN_PAGE,'神秘屋'],
        [cus_enum.PageType.SHEN_MI_WU,'月桂酒馆'],
        [cus_enum.PageType.UP_DRAW,'星源占卜'],
        [cus_enum.PageType.FULL_CARD_DRAW,'星源占卜'],
        [cus_enum.PageType.EPIC_CARD_DRAW,'星源占卜'],
        [cus_enum.PageType.OTHER_PAGE,'点击空白处关闭']
    ]
    # hwnd = 328656
    # hwnd = 3082684
    currentPagetype = ''
    isCheckFullWishList = False
    isCheckEpicWishLis = False
    isCheckStarOriginWishList = False
    try:
        while True:
            time.sleep(0.7)
            if paused:
                continue
            #截图
            imagePath,w,h = utils.window_screenshot(hwnd)
            print(w,",",h)
            #识别图片内容
            ocr_result = config.READER.readtext(imagePath)
            allText = []
            for item in ocr_result:
                trimText = item[1].replace(" ","")
                # print(trimText)
                allText.append(trimText)
            
            isFind = False
            global draw_mode
            for uii in config.UI_TYPE_LIST:
                if utils.is_subset(uii[1],allText):
                    currentPagetype = uii[0]
                    print('界面类型：',currentPagetype.value)
                    
                    if draw_mode == cus_enum.DrawMode.FULL_LIST_DRAW:
                        for li in full_list_line:
                            if uii[0] == li[0]:
                                    utils.clickIntoByButtonName(hwnd,li[1],ocr_result)
                    elif draw_mode == cus_enum.DrawMode.EPIC_CARD_DRAW:
                        for li in epic_list_line:
                            if uii[0] == li[0]:
                                    utils.clickIntoByButtonName(hwnd,li[1],ocr_result)
                    elif draw_mode == cus_enum.DrawMode.STAR_ORIGIN_DRAW:
                        if currentPagetype == cus_enum.PageType.UP_DRAW or currentPagetype == cus_enum.PageType.FULL_CARD_DRAW or currentPagetype == cus_enum.PageType.EPIC_CARD_DRAW:
                            mX = int(w / 2)
                            mY = h - 10
                            pyautogui.moveTo(mX, mY, duration=0.1)
                            pyautogui.dragTo(mX - 200,mY, button='left',duration=0.3)
                            time.sleep(0.3)
                            #再次识别图片内容
                            imagePath2,w,h = utils.window_screenshot(hwnd)
                            ocr_result = config.READER.readtext(imagePath2)
                            os.remove(imagePath2)
                        for li in star_origin_line:
                            if uii[0] == li[0]:
                                    utils.clickIntoByButtonName(hwnd,li[1],ocr_result)
                                    time.sleep(0.3)
                        print(draw_mode)
                    
                    isFind = True
                    break
            if not isFind:
                print('未知界面')
            #删除截图
            os.remove(imagePath)


            #如果是在全英雄招募界面，进入心愿单进行调整
            if currentPagetype == cus_enum.PageType.FULL_CARD_DRAW and not isCheckFullWishList:
                message_queue.put(f"开始调整心愿单...") 
                isCheckFullWishList = True
                changeFullCardWishList(hwnd,ocr_result)
                message_queue.put(f"调整心愿单成功")
            elif currentPagetype == cus_enum.PageType.EPIC_CARD_DRAW and not isCheckEpicWishLis:
                message_queue.put(f"开始调整心愿单...") 
                isCheckEpicWishLis = True
                changeEpicCardWishList(hwnd)
                message_queue.put(f"调整心愿单成功")
            elif currentPagetype == cus_enum.PageType.STAR_ORIGIN_DRAW and not isCheckStarOriginWishList:
                message_queue.put(f"开始调整心愿单...")
                isCheckStarOriginWishList = True
                changeStarOriginWishList(hwnd)
                message_queue.put(f"调整心愿单成功")
    except KeyboardInterrupt:  
        print("Script interrupted by user.")
        
class DrawCardsThread(threading.Thread):  
    def __init__(self, name):  
        super().__init__()  
        self.name = name  
  
    def run(self):
        global draw_mode
        tickets = [white_tickets,red_tickets,ball_tickets]
        limit_times = [limit_begin_h,limit_end_h,limit_begin_m,limit_end_m]
        if draw_mode == cus_enum.DrawMode.TURBO_DRAW_EPIC:
            log.logger.info("开始史诗抽卡模式")
            turbo.turbo_draw_mode(hwnd,False,limit_times,tickets)
        elif draw_mode == cus_enum.DrawMode.TURBO_DRAW_GD:
            log.logger.info("开始神魔抽卡模式")
            turbo.turbo_draw_mode(hwnd,True,limit_times,tickets)
        elif draw_mode == cus_enum.DrawMode.DIRECT_DRAW_FULL:
            log.logger.info("开始全英雄定向金抽卡模式")
            turbo.direct_draw_full_mode(hwnd,limit_times,39)
        elif draw_mode == cus_enum.DrawMode.DIRECT_DRAW_EPIC:
            log.logger.info("开史诗定向金抽卡模式")
        elif draw_mode == cus_enum.DrawMode.IDLE_MODE:
            log.logger.info("开始自动挂机模式")
            turbo.idle_mode(hwnd)
        else :
            log.logger.info("调整心愿单")
            draw_cards_mode()

drawCardsThread = DrawCardsThread('Draw Card Thread')           
#界面响应函数 
def on_select(name, index, mode):  
    # 当用户选择一个选项时，这个函数会被调用
    v = window_menu_var.get()
    global hwnd
    hwnd = int(v.split(':')[1]) 
    
def on_mode_select(name, index, mode):
    # 当用户选择一个选项时，这个函数会被调用
    v = mode_menu_var.get()
    global draw_mode
    for e in cus_enum.DrawMode:
        if e.value == v:
            draw_mode = e
   
def on_closing():
        # 这里我们不需要显式中断线程，因为我们将线程设置为守护线程  
        # 当主线程（即tkinter事件循环）结束时，守护线程会自动结束  
        print("Window is closing, exiting program.")
        try:
            for filename in os.listdir('./'):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    os.remove('./'+filename)
        except:
            print('无法删除图片')
        root.destroy()  # 销毁窗口  

def on_start_click(event):        
    if hwnd != 0:
        global white_tickets
        user_input = entry1.get()
        if not user_input.isdigit():
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry1.config(state=tk.DISABLED)
        white_tickets = int(user_input)
        
        global red_tickets
        user_input = entry2.get()
        if not user_input.isdigit():
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry2.config(state=tk.DISABLED)
        red_tickets = int(user_input)
        
        # 使用get()方法读取Entry中的值
        global ball_tickets
        user_input = entry3.get()
        if not user_input.isdigit():
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry3.config(state=tk.DISABLED)
        ball_tickets = int(user_input)
        
        if white_tickets == 0 or red_tickets == 0 or ball_tickets == 0:
            messagebox.showinfo("提示", "数量不足，无法开始！") 
        
        global limit_begin_h
        global limit_end_h
        global limit_begin_m
        global limit_end_m

        begin_h_input = entry1_s.get()
        if (not begin_h_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry1_s.config(state=tk.DISABLED)
        limit_begin_h = int(begin_h_input)
        
        end_h_input = entry2_s.get()
        if (not end_h_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry2_s.config(state=tk.DISABLED)
        limit_end_h = int(end_h_input)
        
        begin_m_input = entry3_s.get()
        if (not begin_m_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry3_s.config(state=tk.DISABLED)
        limit_begin_m = int(begin_m_input)
        
        end_m_input = entry4_s.get()
        if (not end_m_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry4_s.config(state=tk.DISABLED)
        limit_end_m = int(end_m_input)
        

       
        drawCardsThread = DrawCardsThread('Draw Card Thread')
        drawCardsThread.daemon = True
        drawCardsThread.start()

        # 禁用start_button  
        start_button.button.config(state=tk.DISABLED)
        paused_button.button.config(state=tk.ACTIVE)
        stop_button.button.config(state=tk.ACTIVE)
        turbo.turbo_stop = False
    else :
        messagebox.showinfo("错误", "请选择游戏窗口！") 
        
def on_paused_click(event):
    if hwnd != 0:
        turbo.turbo_paused = not turbo.turbo_paused
        print(turbo.turbo_paused)
        if  turbo.turbo_paused:
            paused_button.button.config(text='继续')
        else :
            paused_button.button.config(text='暂停')
            
def on_stop_click(event):
    if hwnd != 0:
        turbo.turbo_stop = True
        stop_button.button.config(state=tk.DISABLED)
        paused_button.button.config(state=tk.DISABLED)
        start_button.button.config(state=tk.ACTIVE)
        entry1_s.config(state=tk.NORMAL)
        entry2_s.config(state=tk.NORMAL)
        entry3_s.config(state=tk.NORMAL)
        entry4_s.config(state=tk.NORMAL)
        entry1.config(state=tk.NORMAL)
        entry2.config(state=tk.NORMAL)
        entry3.config(state=tk.NORMAL)
        
def on_test_ocr_click(event):
    if hwnd != 0:
        page_test.show_screen_ocr(hwnd)
        
        
 #自定义button    
class EventButton:
    def __init__(self, root,text,row,column):  
        self.root = root  
        self.button = tk.Button(root, text=text, command=self.on_click)  
        self.button.grid(row=row,column=column,pady=10,padx=10,sticky="nsew")
        self.event_handlers = {}  # 用于存储事件和对应处理函数的字典

    def on_click(self):
        # 当按钮被点击时，触发所有注册到这个按钮的事件处理函数  
        for _, handler in self.event_handlers.items():  
            handler(event) 
    def register_event_handler(self, event_name, handler):  
        # 注册一个事件处理函数到特定的事件上  
        self.event_handlers[event_name] = handler
    
    # 重写on_event方法以处理来自事件系统的通知  
    def on_event(self, event_name, *args, **kwargs):  
        # 检查是否有为这个事件注册的处理函数，并调用它  
        if event_name in self.event_handlers:  
            self.event_handlers[event_name](*args, **kwargs)    

# 获取所有窗口句柄列表
# 参数:无
# 返回值:句柄列表 格式 ["title:hwnd_id",...]
def get_window_hwnd_list():
    hwnd_list = []
    windows = get_all_windows()
    for w_hwnd, title in windows: 
        item =  title + ":" + str(w_hwnd)
        hwnd_list.append(item)
    return hwnd_list

# 创建一个事件系统  
event_system = {  
    "start_clicked": event.Event("start_clicked")  
}
        
if __name__ == "__main__":
    # 获取所有窗口句柄列表
    hwnd_list = get_window_hwnd_list()
    # 构建界面
    # 参数: hwndList 桌面窗口句柄列表
    root = tk.Tk()  
    root.title("AFK2Hyper")
    # 使用StringVar来存储选中的值  
    window_menu_var = tk.StringVar(value="请选择游戏窗口")
    window_menu = tk.OptionMenu(root, window_menu_var, *hwnd_list)  
    window_menu.pack(fill=tk.X,padx=5, pady=5)
    window_menu_var.trace("w", on_select)
    draw_mode_list = []
    for dm in cus_enum.DrawMode:
        draw_mode_list.append(dm.value)

    mode_menu_var = tk.StringVar(value=cus_enum.DrawMode.TURBO_DRAW_EPIC.value)
    mode_menu = tk.OptionMenu(root, mode_menu_var, *draw_mode_list)  
    mode_menu.pack(fill=tk.X,padx=5, pady=5)
    mode_menu_var.trace("w", on_mode_select)
    text = tk.Label(width=30,text="请输入背包库存")
    text.pack(padx=5, pady=20)
    # 创建父框架，使用pack布局
    parent_frame = tk.Frame(root)
    parent_frame.pack(padx=10, pady=10)
    

    # 在父框架内使用grid布局
    text1 = tk.Label(parent_frame,width=15,text="白票数量")
    text1.grid(row=0, column=0, padx=5, pady=5)

    text2 = tk.Label(parent_frame,text="红票数量")
    text2.grid(row=0, column=1, padx=5, pady=5)
    
    text3 = tk.Label(parent_frame,text="水晶球数量")
    text3.grid(row=0, column=2, padx=5, pady=5)
    
    # 创建第一个输入框
    entry1 = tk.Entry(parent_frame, width=15)
    entry1.grid(row=1, column=0, padx=5, pady=5)
    entry1.insert(tk.END,"60")
    # 创建第二个输入框
    entry2 = tk.Entry(parent_frame, width=15)
    entry2.grid(row=1, column=1, padx=5, pady=5)
    entry2.insert(tk.END,"30")
    # 创建第三个输入框
    entry3 = tk.Entry(parent_frame, width=15)
    entry3.grid(row=1, column=2, padx=5, pady=5)
    entry3.insert(tk.END,"40")
    
    text_s = tk.Label(width=30,text="设置抽卡窗口期")
    text_s.pack(padx=5, pady=20)
    
    # 创建父框架，使用pack布局
    parent_frame_2 = tk.Frame(root)
    parent_frame_2.pack(fill=tk.X, expand=True, padx=10, pady=10)
    # 在父框架内使用grid布局
    text1_s = tk.Label(parent_frame_2,width=15,text="小时开始时间(0-24)")
    text1_s.grid(row=0, column=0, padx=5, pady=5)

    text2_s = tk.Label(parent_frame_2,text="小时结束时间(0-24)")
    text2_s.grid(row=0, column=1, padx=5, pady=5)
    
    text3_s = tk.Label(parent_frame_2,text="分钟开始时间(0-60)")
    text3_s.grid(row=0, column=2, padx=5, pady=5)
    
    text4_s = tk.Label(parent_frame_2,text="分钟结束时间(0-60)")
    text4_s.grid(row=0, column=3, padx=5, pady=5)
    
    # 创建第一个输入框
    entry1_s = tk.Entry(parent_frame_2, width=15)
    entry1_s.grid(row=1, column=0, padx=5, pady=5)
    entry1_s.insert(tk.END,"1")
    # 创建第二个输入框
    entry2_s = tk.Entry(parent_frame_2, width=15)
    entry2_s.grid(row=1, column=1, padx=5, pady=5)
    entry2_s.insert(tk.END,"5")
    # 创建第三个输入框
    entry3_s = tk.Entry(parent_frame_2, width=15)
    entry3_s.grid(row=1, column=2, padx=5, pady=5)
    entry3_s.insert(tk.END,"58")
    # 创建第四个输入框
    entry4_s = tk.Entry(parent_frame_2, width=15)
    entry4_s.grid(row=1, column=3, padx=5, pady=5)
    entry4_s.insert(tk.END,"3")
    
    # 创建父框架，使用pack布局
    button_frame = tk.Frame(root)
    button_frame.pack( padx=10, pady=10)
    start_button = EventButton(button_frame,'开始',0,0)
    start_button.register_event_handler("start_clicked", on_start_click)
    paused_button = EventButton(button_frame,'暂停',0,1)
    paused_button.button.config(state=tk.DISABLED)
    paused_button.register_event_handler("start_clicked",on_paused_click)
    stop_button = EventButton(button_frame,'停止',0,2)
    stop_button.register_event_handler("start_clicked", on_stop_click)
    stop_button.button.config(state=tk.DISABLED)
    
    test_ocr_button = EventButton(button_frame,'识别文字',0,3)
    test_ocr_button.register_event_handler("start_clicked", on_test_ocr_click)
    
    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)  
    log_text.pack(padx=10, pady=10)
    log_text.config(state=tk.NORMAL)
    
    close_button = tk.Button(root, text="关闭", command=on_closing)
    close_button.pack(pady=5)

    
    # 安排check_queue函数在主线程的事件循环中定期运行  
    root.after(100, check_queue)
    # 绑定窗口关闭事件到on_closing函数  
    root.protocol("WM_DELETE_WINDOW", on_closing)  
   
    
    # 运行tkinter事件循环  
    root.mainloop()

    
    
   

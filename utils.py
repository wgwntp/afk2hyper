from datetime import datetime
import win32gui
import cv2
import pyautogui
import cus_enum 
import config
import numpy as np
import os
import time
from collections import Counter
import shutil
import random
import win32api
import win32con

def window_screenshot(hwnd):  
    # 获取窗口的矩形区域  
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  
    width = right - left  
    height = bottom - top  
  
    screenshot =  pyautogui.screenshot(region=(left, top, width, height))

    # 保存截图到文件
    current_time_str = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    screenshot_path = "window_screenshot"+current_time_str+".png"  
    screenshot.save(screenshot_path)  
    return screenshot_path,width,height,left,top

def save_window_screenshot(hwnd):
    # 获取窗口的矩形区域  
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  
    width = right - left  
    height = bottom - top  
  
    screenshot =  pyautogui.screenshot(region=(left, top, width, height))

    # 保存截图到文件
    current_time_str = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    screenshot_path ="./res/" + "window_screenshot"+current_time_str+".png"  
    screenshot.save(screenshot_path)  
    return screenshot_path,width,height

def get_card_color(hwnd):
    for i in range(3):
        path,_,_ = save_window_screenshot(hwnd)
        image = cv2.imread(path)
        img_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        width,height,_ = img_rgb.shape
        # 左上角
        pt1 = (int(width * 0.05),int(height * 0.05))
        # 右上角
        pt2 = (int(width * 0.97),int(height * 0.04))
        # 左下角
        pt3 = (int(width * 0.05),int(height * 0.98))
        # 右下角
        pt4 = (int(width * 0.97),int(height * 0.98))
        pts = [pt1,pt2,pt3,pt4]
        colors = []
        for p in pts:
            colors.append(getPointColor(img_rgb,p[0],p[1]))
        
        for c in colors:
            if c != cus_enum.CardColor.UNKNOWN:
                return c
        current_time_str = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        shutil.move(path, "./unknown/" + current_time_str +".png")
        time.sleep(2)
    return cus_enum.CardColor.UNKNOWN

def getPointColor(img,x,y):
    pixel_color = img[x, y]
    r = pixel_color[0]
    g = pixel_color[1]
    b = pixel_color[2]
    # print("中心像素的 RGB 值:", pixel_color)
    if 35<r<55 and 145<g<165 and 155<b<175:
        return cus_enum.CardColor.BLUE
    elif 60<r<80 and 145<g<165 and 110<b<140:
        return cus_enum.CardColor.GREEN
    elif 70<r<190 and 50<g<110 and 140<b<255:
        return cus_enum.CardColor.PURPLE
    elif 200<r<255 and 110<g<170 and 0<b<80:
        return cus_enum.CardColor.GOLD
    else :
        return cus_enum.CardColor.UNKNOWN
    
def is_subset(subset, superset):  
    """  
    判断一个列表是否是另一个列表的子集。  
  
    参数:  
    subset (list): 子集列表。  
    superset (list): 超集列表。  
  
    返回:  
    bool: 如果subset是superset的子集，则返回True；否则返回False。  
    """  
    # 将列表转换为集合  
    set_subset = set(subset)  
    set_superset = set(superset)  
      
    # 使用集合的issubset方法检查子集关系  
    return set_subset.issubset(set_superset)

def cal_center(hwnd,vertices):
    rect = win32gui.GetWindowRect(hwnd)  
    left, top, right, bottom = rect
    client_left = left 
    client_top = top 
    x = (vertices[0][0] + vertices[1][0]) / 2 
    y = (vertices[0][1] + vertices[2][1]) / 2
    
    screen_x = client_left + x  
    screen_y = client_top + y
    return screen_x, screen_y

def clickIntoByButtonName(hwnd,buttontNames, ocr_result):
    isSuccess = False
    if len(buttontNames) == 0:
        return False
    
    if buttontNames[0].lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # 截取屏幕图片
        screen_path,w,h,left,top = window_screenshot(hwnd)
        screenImage = cv2.imread(screen_path)
        os.remove(screen_path)
        temp_img = cv2.imread(config.IMAGES_PATH + buttontNames[0])
        calW,calH = reCalTemplateSize(w,h,0.086,0.035)
        resized_img = cv2.resize(temp_img, (calW, calH), interpolation=cv2.INTER_AREA)
        h_cal_w = int(calW / 2)
        h_cal_h = int(calH / 2)
        res = cv2.matchTemplate(screenImage, resized_img, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.8
        loc = np.where(res >= threshold)
        pts = list(zip(*loc[::-1]))
        if len(pts)>0 :
            pt = pts[0]
            pyautogui.click(pt[0]+left+h_cal_w, pt[1]+top+h_cal_h)
            isSuccess = True
        else:
            print('not find:',buttontNames[0])
    else: 
        for i in ocr_result:
            if i[1] in buttontNames:
                x,y = cal_center(hwnd,i[0])
                pyautogui.click(x, y)
                isSuccess = True
                break
    return isSuccess 

def clickIntoByImage(hwnd,image_name,w_radio,h_radio):
    isSuccess = False
    # 截取屏幕图片
    screen_path,w,h,left,top = window_screenshot(hwnd)
    screenImage = cv2.imread(screen_path)
    os.remove(screen_path)
    temp_img = cv2.imread(config.IMAGES_PATH + image_name)
    calW,calH = reCalTemplateSize(w,h,w_radio,h_radio)
    resized_img = cv2.resize(temp_img, (calW, calH), interpolation=cv2.INTER_AREA)
    res = cv2.matchTemplate(screenImage, resized_img, cv2.TM_CCOEFF_NORMED)  
    # 设置一个阈值，用于确定匹配的程度  
    threshold = 0.8
    loc = np.where(res >= threshold)
    pts = list(zip(*loc[::-1]))
    if len(pts)>0 :
        pt = pts[0]
        pyautogui.click(pt[0]+left, pt[1]+top)
        isSuccess = True
    else:
        print('not find:',image_name)
    return isSuccess
        
def reCalTemplateSize(screen_w,screen_h,w_ratio,h_ratio):
    cal_w = int(screen_w * w_ratio)
    cal_h = int(screen_h * h_ratio)
    return cal_w,cal_h

def matchOneTemplate(hwnd,temp_path,ratio_w,ratio_h):
    imagePath,w,h,left,top = window_screenshot(hwnd)
    map_image = cv2.imread(imagePath)
    os.remove(imagePath)
    trans_image = cv2.imread(config.IMAGES_PATH + temp_path)
    tempW,tempH = reCalTemplateSize(w,h,ratio_w,ratio_h)
    resized_img = cv2.resize(trans_image, (tempW, tempH), interpolation=cv2.INTER_AREA)
    # 使用matchTemplate函数在大图中搜索模板  
    res = cv2.matchTemplate(map_image, resized_img, cv2.TM_CCOEFF_NORMED)  
    # 设置一个阈值，用于确定匹配的程度  
    threshold = 0.85
    loc = np.where(res >= threshold)
    # 在原图上绘制矩形框，标记出匹配的位置
    pts = list(zip(*loc[::-1]))
    if len(pts) > 0:
        rand_index = random.randint(0,len(pts) - 1)
        pt = pts[rand_index]
        x = pt[0] + int(tempW / 2)
        y = pt[1] + int(tempH * 0.7)
        # _, sw, sh = resized_img.shape[::-1]    
        # cv2.rectangle(map_image, pts[0], (pts[0][0] + sw, pts[0][1] + sh), (0, 255, 0), 2)
        # cv2.imshow('Detected Rectangles', map_image)  
        # cv2.waitKey(0)  
        return x+left,y+top
    else :
        return 0,0

def get_current_page_type(hwnd):
    current_page_type = cus_enum.PageType.UNKNOWN_PAGE
    #截图
    imagePath,w,h,_,_ = window_screenshot(hwnd)
    #识别图片内容
    ocr_result = config.READER.readtext(imagePath)
    os.remove(imagePath)
    all_text = []
    for item in ocr_result:
        trimText = item[1].replace(" ","")
        all_text.append(trimText)
    for uii in config.UI_TYPE_LIST:
        if uii[1][0].lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # 60,60 60/1155=0.05, 60/2093=0.028
            x,y = matchOneTemplate(hwnd,uii[1][0],0.05,0.028)
            if x != 0 or y != 0:
                current_page_type = uii[0]
                break
        else :
            if is_subset(uii[1],all_text):
                current_page_type = uii[0]
                break
        
    return current_page_type,ocr_result   
# def click_message(hwnd,x,y):
#     lparam = win32api.MAKELONG(x,y)
#     win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,lparam)
#     time.sleep(0.05)
#     win32gui.SendMessage(hwnd,win32con.WM_LBUTTONUP,0,lparam)
import utils
import os
import pyautogui
import time
import config
import random
UI_TYPE_LIST = [
    (1,['互助']),
    (2,['战斗','秋夜之争']),
    (3,['秋叶之争']),
    (4,['点击空白处关闭']),
]
TO_CONFIM_STEP = [
    [1,'帮助夺回资源'],
]

TO_FIGHT_STEP = [
    [2,'战斗']
]

TO_HELP_SETP = [
    [4,'点击空白处关闭'],
]
def toTargetPage(hwnd,step,target_page):
    count = 0 
    while True:
        time.sleep(0.3)
        count +=1
        current_page_type = ''
        #截图
        imagePath,w,h,left,top = utils.window_screenshot(hwnd)
        print(w,",",h)
        #识别图片内容
        ocr_result = config.READER.readtext(imagePath)
        os.remove(imagePath)
        all_text = []
        for item in ocr_result:
            trimText = item[1].replace(" ","")
            all_text.append(trimText)
        # print(all_text)
        for uii in UI_TYPE_LIST:
            r = random.randint(8,20)
            if utils.is_subset(uii[1],all_text):
                current_page_type = uii[0]
                print('界面类型：',current_page_type)
                mX = int(w / 2)
                mY = h - 300
                if current_page_type == target_page:
                     return True
                if target_page == 2 and current_page_type == 1:
                        for i in range(r):
                            slide_up(hwnd)
                        time.sleep(0.7)
                        pyautogui.click(mX+left, mY+top)
                        imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
                        #识别图片内容
                        ocr_result = config.READER.readtext(imagePath)
                        os.remove(imagePath)
                for li in step:
                    if current_page_type == li[0]:
                        while True:
                            success = utils.clickIntoByButtonName(hwnd,li[1],ocr_result)
                            if not success :
                                for i in range(r):
                                    slide_up(hwnd)
                                time.sleep(0.7)
                                pyautogui.click(mX+left, mY+top)
                                imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
                                #识别图片内容
                                ocr_result = config.READER.readtext(imagePath)
                                os.remove(imagePath)
                                count += 1
                                if count > 10:
                                    break
                            else:
                                time.sleep(0.3)
                                count = 0
                                break
                break
        return
def gandy_heart(hwnd):
    while True:
        time.sleep(0.3)
        toTargetPage(hwnd,TO_CONFIM_STEP,2)
            
        time.sleep(0.3)
        toTargetPage(hwnd,TO_FIGHT_STEP,3)
            
        time.sleep(0.3)
        toTargetPage(hwnd,TO_HELP_SETP,1)
           
    
    
def slide_up(hwnd):
    #截图
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    os.remove(imagePath)
    mX = int(w / 2)
    mY = h - 300
    pyautogui.moveTo(mX+left, mY+top, duration=0.1)
    time.sleep(0.1)
    pyautogui.dragTo(mX+left,mY+top-1500, button='left',duration=0.2)

    
if __name__ == "__main__":
    # 4196852
    gandy_heart(3801690)
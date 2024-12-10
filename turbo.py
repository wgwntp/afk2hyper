
from datetime import datetime
import cus_enum
import config
import time
import utils
import os
import pyautogui
import log
import wish_list
import random
import shutil
import cv2

turbo_paused = False
turbo_stop = False
is_change_wish_list = False


is_need_change_full_wish_list = True
is_need_change_epic_wish_list = True

FULL_LIST_DRAW_SETP = [
    [cus_enum.PageType.MAIN_PAGE,['神秘屋']],
    [cus_enum.PageType.CATEGORY,['神秘屋']],
    [cus_enum.PageType.HERO_HALL,['神秘屋']],
    [cus_enum.PageType.CLUB,['神秘屋']],
    [cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']],
    [cus_enum.PageType.UP_DRAW,['全英雄招募']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['全英雄招募']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

EPIC_DRAW_SETP = [
    [cus_enum.PageType.MAIN_PAGE,['神秘屋']],
    [cus_enum.PageType.CATEGORY,['神秘屋']],
    [cus_enum.PageType.HERO_HALL,['神秘屋']],
    [cus_enum.PageType.CLUB,['神秘屋']],
    [cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']],
    [cus_enum.PageType.UP_DRAW,['史诗招募']],
    [cus_enum.PageType.FULL_CARD_DRAW,['史诗招募']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

STAR_ORIGIN_SETP = [
    [cus_enum.PageType.MAIN_PAGE,['神秘屋']],
    [cus_enum.PageType.CATEGORY,['神秘屋']],
    [cus_enum.PageType.HERO_HALL,['神秘屋']],
    [cus_enum.PageType.CLUB,['神秘屋']],
    [cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']],
    [cus_enum.PageType.UP_DRAW,['星源占卜']],
    [cus_enum.PageType.FULL_CARD_DRAW,['星源占卜']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['星源占卜']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

MAIN_PAGE_SETP = [
    [cus_enum.PageType.CATEGORY,['./back2.png']],
    [cus_enum.PageType.HERO_HALL,['./back2.png']],
    [cus_enum.PageType.CLUB,['./back2.png']],
    [cus_enum.PageType.SHEN_MI_WU,['./back2.png']],
    [cus_enum.PageType.UP_DRAW,['./back2.png']],
    [cus_enum.PageType.FULL_CARD_DRAW,['./back2.png']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['./back2.png']],
    [cus_enum.PageType.STAR_ORIGIN_DRAW,['./back2.png']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
    [cus_enum.PageType.IDLE_PAGE,['back.png']],
    [cus_enum.PageType.READY_FIGHT_PAGE,['back.png']],
    [cus_enum.PageType.PLAGIARIZE_PAGE,['点击空白处关闭']],
    [cus_enum.PageType.FIGHT_FAIL_PAGE,['继续挑战']],
    [cus_enum.PageType.FIGHT_SUCCESS_1_PAGE,['继续挑战']],
    [cus_enum.PageType.FIGHT_SUCCESS_2_PAGE,['back.png']], 
]

PACK_PAGE_SETP = [
    [cus_enum.PageType.MAIN_PAGE,['./menu_icon.png']],
    [cus_enum.PageType.SECOND_PAGE,['背包']],
    [cus_enum.PageType.CATEGORY,['./menu_icon.png']],
    [cus_enum.PageType.HERO_HALL,['./menu_icon.png']],
    [cus_enum.PageType.CLUB,['./menu_icon.png']],
    [cus_enum.PageType.SHEN_MI_WU,['./menu_icon.png']],
    [cus_enum.PageType.UP_DRAW,['./back2.png']],
    [cus_enum.PageType.FULL_CARD_DRAW,['./back2.png']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['./back2.png']],
    [cus_enum.PageType.STAR_ORIGIN_DRAW,['./back2.png']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

FULL_LIST_DRAW_ONECE_STEP = [
    [cus_enum.PageType.MAIN_PAGE,['神秘屋']],
    [cus_enum.PageType.CATEGORY,['神秘屋']],
    [cus_enum.PageType.HERO_HALL,['神秘屋']],
    [cus_enum.PageType.CLUB,['神秘屋']],
    [cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']],
    [cus_enum.PageType.UP_DRAW,['全英雄招募']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['全英雄招募']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
    [cus_enum.PageType.FULL_CARD_DRAW,['招募一次','招募-次']]
]

EPIC_DRAW_ONCE_STEP = [
    [cus_enum.PageType.MAIN_PAGE,['神秘屋']],
    [cus_enum.PageType.CATEGORY,['神秘屋']],
    [cus_enum.PageType.HERO_HALL,['神秘屋']],
    [cus_enum.PageType.CLUB,['神秘屋']],
    [cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']],
    [cus_enum.PageType.UP_DRAW,['史诗招募']],
    [cus_enum.PageType.FULL_CARD_DRAW,['史诗招募']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['招募一次','招募-次']]
]

ORIGIN_STAR_TEHTH_STEP = [ 
    [cus_enum.PageType.MAIN_PAGE,['神秘屋']],
    [cus_enum.PageType.CATEGORY,['神秘屋']],
    [cus_enum.PageType.HERO_HALL,['神秘屋']],
    [cus_enum.PageType.CLUB,['神秘屋']],
    [cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']],
    [cus_enum.PageType.UP_DRAW,['星源占卜']],
    [cus_enum.PageType.FULL_CARD_DRAW,['星源占卜']],
    [cus_enum.PageType.EPIC_CARD_DRAW,['星源占卜']],
    [cus_enum.PageType.STAR_ORIGIN_DRAW,['占卜十次']],
    [cus_enum.PageType.READY_TO_DRAW_ORIGIN_PAGE,['长按或点击进行占卜']],
    [cus_enum.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [cus_enum.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

def get_current_page_type(hwnd):
    current_page_type = cus_enum.PageType.UNKNOWN_PAGE
    #截图
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
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
            x,y = utils.matchOneTemplate(hwnd,uii[1][0],0.05,0.028)
            if x != 0 or y != 0:
                current_page_type = uii[0]
                break
        else :
            if utils.is_subset(uii[1],all_text):
                current_page_type = uii[0]
                break
        
    return current_page_type,ocr_result
# 跳转界面函数，从任一界面跳转到目标界面
def toTargetPage(hwnd,step,target_page,cards_map=[],full_back_up_wish_list=[],epic_back_up_wish_list=[]):
    count = 0
    step.extend(config.COMMON_ROUTE)
    current_page_type,ocr_result = get_current_page_type(hwnd)
    while True:
        if turbo_paused:
            return

        if turbo_stop:
            return
        time.sleep(1.2)
        count +=1
        
        print(current_page_type,count)
        # 如果出现编辑心愿单提示。需要替换心愿单
        if current_page_type == cus_enum.PageType.EDIT_PAGE:
            if not wish_list.change_wish_list_for_max_cards(hwnd,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                continue
        if target_page in [cus_enum.PageType.STAR_ORIGIN_DRAW,cus_enum.PageType.DRAW_TENTH_AGAIN] and current_page_type in [cus_enum.PageType.UP_DRAW,cus_enum.PageType.FULL_CARD_DRAW,cus_enum.PageType.EPIC_CARD_DRAW]:
            slide_for_star(hwnd)
            imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
            #识别图片内容
            ocr_result = config.READER.readtext(imagePath)
            os.remove(imagePath)
            
        for li in step:
            if current_page_type == li[0]:
                is_success = utils.clickIntoByButtonName(hwnd,li[1],ocr_result)
                time.sleep(1.2)
                if current_page_type in [cus_enum.PageType.FULL_CARD_DRAW,cus_enum.PageType.EPIC_CARD_DRAW] and target_page == cus_enum.PageType.DRAW_AGAIN_ONCE:
                    time.sleep(6)
                if current_page_type == cus_enum.PageType.READY_TO_DRAW_ORIGIN_PAGE:
                    time.sleep(8)
                if is_success:
                    count = 0
                break
            
        current_page_type,ocr_result = get_current_page_type(hwnd)
        
        if current_page_type == cus_enum.PageType.DRAW_TENTH_AGAIN:
            log.logger.info("截图保存")
            utils.save_window_screenshot(hwnd)
        
        if current_page_type == target_page:
            return True  
        else:
            if count >= 6 and count < 10:
                if utils.clickIntoByButtonName(hwnd,['confirm.png'],ocr_result):
                    print("click confirm")
                    count = 0
                    continue
                if utils.clickIntoByButtonName(hwnd,['确认'],ocr_result):
                    print("click confirm")
                    count = 0
                    continue
                # 尝试返回上级界面
                if utils.clickIntoByButtonName(hwnd,['back.png'],ocr_result):
                    count = 0
                    continue
                
                if utils.clickIntoByButtonName(hwnd,['back2.png'],ocr_result):
                    count = 0
                    continue
                if utils.clickIntoByImage(hwnd,'mumu_exit.png',0.025,0.014):
                    count = 0
                    continue
            elif count >= 10:
                return False
      
# def draw_again(hwnd,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
#     #截图
#     imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
#     #识别图片内容
#     ocr_result = config.READER.readtext(imagePath)
#     os.remove(imagePath)
#     is_success = utils.clickIntoByButtonName(hwnd,'再招募一次',ocr_result)
#     time.sleep(0.5)
#     # 检查是否有钻石抽取确认界面
#     imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
#     #识别图片内容
#     ocr_result = config.READER.readtext(imagePath)
#     os.remove(imagePath)
#     utils.clickIntoByButtonName(hwnd,'确认',ocr_result)
#     time.sleep(1)
#     # 再次识别
#     imagePath,_,_,_,_ = utils.window_screenshot(hwnd)
#     #识别图片内容
#     ocr_result = config.READER.readtext(imagePath)
#     os.remove(imagePath)
#     is_need_edit = False
#     for ocr in ocr_result:
#         if ocr[1] == '编辑英雄':
#             is_need_edit = True
#     # 如果出现编辑心愿单提示。需要替换心愿单
#     if is_need_edit:
#         if not wish_list.change_wish_list_for_max_cards(hwnd,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
#             return False
               
#     return is_success
   
# def draw_ten(hwnd):
    #截图
    # imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    # #识别图片内容
    # ocr_result = config.READER.readtext(imagePath)
    # os.remove(imagePath)
    # utils.clickIntoByButtonName(hwnd,'占卜十次',ocr_result)
    # time.sleep(1)
    # pyautogui.click(int(w / 2)+left,int(h / 2)+top)
    # time.sleep(1)
    # pyautogui.click(int(w / 2)+left,int(h / 2)+top)
    # time.sleep(5)
    # log.logger.info("截图保存")
    # utils.save_window_screenshot(hwnd)
 
def slide_for_star(hwnd):
    #截图
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    os.remove(imagePath)
    mX = int(w / 2)
    mY = h - 10
    pyautogui.moveTo(mX+left, mY+top, duration=0.1)
    pyautogui.dragTo(mX+left - 200,mY+top, button='left',duration=0.3)
    time.sleep(0.5)

def main_page_refresh(hwnd):
    # 977,237
    # 977/1155 = 0.84
    # 237/2093 = 0.11
    if turbo_paused:
        return False
    
    if turbo_stop:
        return False
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    mapX,mapY = utils.reCalTemplateSize(w,h,0.84,0.11)
    pyautogui.click(mapX+left,mapY+top)
    time.sleep(0.5)
    os.remove(imagePath)
    # 再次截图
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    ocr_result = config.READER.readtext(imagePath)
    map_list = []
    for ocr in ocr_result:
        if "薄暮丛林" in ocr[1] or "格罗登平原" in ocr[1] or "圣石镇" in ocr[1] or "瓦度索山脉" in ocr[1] or "遗迹群山" in ocr[1]:
            vertices = ocr[0]
            y = vertices[0][1] + vertices[2][1]
            # 过滤屏幕上半部分的地图名字
            if y + top < (h/2):
                continue
            map_list.append(ocr)
    os.remove(imagePath)
    if len(map_list) == 0:
        return False
    rand_index = random.randint(0,len(map_list)-1)
    rand_map_ocr = map_list[rand_index]
    x,y = utils.cal_center(hwnd,rand_map_ocr[0])
    pyautogui.click(x, y)
    time.sleep(0.5)
    # 28,51 28/1155=0.024 51/2093=0.024
    x,y = utils.matchOneTemplate(hwnd,"transmit.png",0.024,0.024)
    if x == 0 and y == 0:
        return False
    else:
        if turbo_paused:
            return False
    
        if turbo_stop:
            return False
        pyautogui.click(x, y)
        time.sleep(0.2)
    
    #90/1155=0.077 80/2093=0.038
    x,y = utils.matchOneTemplate(hwnd,"jump.png",0.077,0.038)
    if x == 0 and y== 0:
        return False
    else :
        if turbo_paused:
            return False
    
        if turbo_stop:
            return False
        pyautogui.click(x,y)
        time.sleep(1)
   
    # 60,60 60/1155=0.05, 60/2093=0.028   
    x,y = utils.matchOneTemplate(hwnd,"time_icon.png",0.05,0.028)
    if x == 0 and y== 0:
        return False
    else :
        if turbo_paused:
            return False
    
        if turbo_stop:
            return False
        pyautogui.click(x,y)
        time.sleep(0.5)
        
    morning_x = int(w * 0.2)
    morning_y = int(h * 0.4)
    
    noon_x = int(w * 0.5)
    noon_y = int(h * 0.3)
    
    afternoon_x = int(w*0.75)
    afternoon_y = int(h * 0.4)
    
    night_x = int(w * 0.5)
    night_y = int(h * 0.6)
    
    timeClickList = [[morning_x,morning_y],[afternoon_x,afternoon_y],[noon_x,noon_y],[night_x,night_y]]
    nextTimeIndex = 0
    for filename in os.listdir(config.IMAGES_PATH):
        if filename.lower().startswith(('t_')):
            x_ratio = 0
            y_ratio = 0
            if filename == "t_morning.png" or filename == "t_afternoon.png":
                x_ratio = 0.389
                y_ratio = 0.119
            else :
                x_ratio = 0.216
                y_ratio = 0.215
        
            x,y = utils.matchOneTemplate(hwnd,filename,x_ratio,y_ratio)
            if x != 0 or y != 0 :
                if filename == 't_morning.png':
                    nextTimeIndex = 1
                elif filename == 't_afternoon.png':
                    nextTimeIndex = 2
                elif filename == 't_noon.png':
                    nextTimeIndex = 3
                else:
                    nextTimeIndex = 0
                break
    nextTime = timeClickList[nextTimeIndex]
    
    if turbo_paused:
        return False
    
    if turbo_stop:
        return False
    
    pyautogui.click(nextTime[0]+left,nextTime[1]+top)
    time.sleep(0.5)
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
    #识别图片内容
    ocr_result = config.READER.readtext(imagePath)
    os.remove(imagePath)
    for i in ocr_result:
        if "切换至" in i[1]:
            x,y = utils.cal_center(hwnd,i[0])
            
            if turbo_paused:
                return False
    
            if turbo_stop:
                return False
            
            pyautogui.click(x, y)
            time.sleep(0.5)
            break
    return True
# target_full_list=["1-y","2-y","42-w","43-w","16-m","15-m","30-l","29-l"],target_epic_list=["42-w","16-m","15-m","30-l","29-l"]
def turbo_draw_mode(hwnd,is_draw_balls,limit_times,tickets,target_full_list=["2-y","4-y","17-m","32-l","45-w","44-w","16-m","6-l"],target_epic_list=["2-y","17-m","44-w","16-m","6-l"],full_back_up_wish_list=['4-y','18-m'],epic_back_up_wish_list=['17-m','3-y','45-w']):
    try:
        white_tickets = tickets[0]
        red_tickets = tickets[1]
        ball_tickets = tickets[2]
        limit_begin_h = limit_times[0]
        limit_end_h = limit_times[1]
        limit_begin_m = limit_times[2]
        limit_end_m = limit_times[3]
        count_white_streak = 0
        global is_need_change_full_wish_list
        cards_map = wish_list.get_card_map(config.GOLD_CARD_PATH)
        log.logger.info("时间窗口期  小时：%d-%d 分钟: %d-%d",limit_begin_h,limit_end_h,limit_begin_m,limit_end_m)
  
        all_color_count_map = {cus_enum.CardColor.GREEN:0,cus_enum.CardColor.BLUE:0,cus_enum.CardColor.PURPLE:0,cus_enum.CardColor.GOLD:0}
        full_color_count_map = {cus_enum.CardColor.GREEN:0,cus_enum.CardColor.BLUE:0,cus_enum.CardColor.PURPLE:0,cus_enum.CardColor.GOLD:0}
        epic_color_count_map = {cus_enum.CardColor.GREEN:0,cus_enum.CardColor.BLUE:0,cus_enum.CardColor.PURPLE:0,cus_enum.CardColor.GOLD:0}
        
        draw_count = 0
        full_draw_count = 0
        epic_draw_count = 0
        
        while True:
            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
            
            if count_white_streak >= 10:
                log.logger.info("十次没有进入史诗，暂停")
                count_white_streak = 0
                time.sleep(300)
            # 获取当前日期和时间
            current_time = datetime.now()
            current_hour = current_time.hour
            current_min = current_time.minute
            is_in_limit_m = False
            if limit_begin_m > limit_end_m:
                is_in_limit_m = (current_min >= limit_begin_m or current_min <= limit_end_m)
            else :
                is_in_limit_m = (current_min >= limit_begin_m and current_min <= limit_end_m)
            if (current_hour >= limit_begin_h and current_hour <= limit_end_h) and is_in_limit_m:
                log.logger.info("================================时间符合:%s:%s",str(current_hour),str(current_min))
                # 连续十次普抽没进入史诗，则暂停五分钟
                log.logger.info("当前库存数 白票:%s, 红票:%s, 水晶球:%s",str(white_tickets),str(red_tickets),str(ball_tickets))
                
                if white_tickets <= 0 or red_tickets <= 0:
                    log.logger.info("库存不满足抽卡条件，退出")
                    return
                
                if is_draw_balls and  ball_tickets <= 0:
                    log.logger.info("神魔库存不满足抽卡条件，退出")
                    return
                
                # 第一步进入主界面
                if not toTargetPage(hwnd,MAIN_PAGE_SETP,cus_enum.PageType.MAIN_PAGE):
                    log.logger.info("进入主页面失败,重新开始")
                    #进入目标页面失败,重新开始
                    continue
                
                if turbo_paused:
                    time.sleep(1)
                    continue
                
                if turbo_stop:
                    break
            
                log.logger.info("进入主页面")
                #第二步 主界面跳转+调整时间
                is_success = False
                for i in range(5):
                    is_success = main_page_refresh(hwnd)
                    if is_success:
                        break
                if not is_success:
                    utils.clickIntoByImage(hwnd,'mumu_exit.png',0.025,0.014)
                    log.logger.info("主页面跳转+调整时间失败")
                    continue
                
                if turbo_paused:
                    time.sleep(1)
                    continue
                
                if turbo_stop:
                    break
                
                log.logger.info("主页面跳转+调整时间完成")
                if not toTargetPage(hwnd,FULL_LIST_DRAW_SETP,cus_enum.PageType.FULL_CARD_DRAW):
                    #进入目标页面失败
                    log.logger.info("进入全英雄页面失败")
                    continue
                
                if is_change_wish_list and is_need_change_full_wish_list:
                    print("调整普池心愿单金卡顺序")
                    is_success =wish_list.full_list_run(hwnd,target_epic_list,target_full_list,cards_map)
                    if not is_success:
                        log.logger.info("普池模式，调整心愿单失败，重新开始")
                        continue
                    is_need_change_full_wish_list = False
                    # 返回普池页面
                # 第三步普池抽卡
                if turbo_paused:
                    time.sleep(1)
                    continue
                
                if turbo_stop:
                    break
                
                log.logger.info("开始普池第一抽")
                if not toTargetPage(hwnd,FULL_LIST_DRAW_ONECE_STEP,cus_enum.PageType.DRAW_AGAIN_ONCE,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                    log.logger.info("普池第一抽失败，重新开始")
                    continue
                time.sleep(2)
                card_color_1 = utils.get_card_color(hwnd)
                log.logger.info("普池第一抽颜色:%s",card_color_1.name)
                
                white_tickets -= 1
                draw_count += 1
                full_draw_count += 1
                
                if card_color_1 == cus_enum.CardColor.GREEN:
                    log.logger.info("普池第一抽绿色,重新开始")
                    #普池绿卡，重新开始
                    count_white_streak += 1
                    continue
                # 普池连抽
                elif card_color_1 in [cus_enum.CardColor.BLUE,cus_enum.CardColor.PURPLE,cus_enum.CardColor.GOLD]:
                    all_color_count_map[card_color_1] += 1
                    full_color_count_map[card_color_1] += 1
                    log.logger.info("普池进入第二抽")
                    if turbo_paused:
                        time.sleep(1)
                        continue
                    
                    if turbo_stop:
                        break
                    
                    log.logger.info("开始普池第二抽")
                    if not toTargetPage(hwnd,FULL_LIST_DRAW_ONECE_STEP,cus_enum.PageType.DRAW_AGAIN_ONCE,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                        log.logger.info("普池第二抽失败，重新开始")
                        continue
                    time.sleep(3)
                    card_color_2 = utils.get_card_color(hwnd)
                    log.logger.info("普池第二抽颜色:%s",card_color_2.name)
                    
                    white_tickets -= 1
                    draw_count += 1
                    full_draw_count += 1
                    
                    if card_color_2 == cus_enum.CardColor.GREEN:
                        log.logger.info("普池第二抽绿色,重新开始")
                        #普池绿卡，重新开始
                        count_white_streak += 1
                        continue
                    elif card_color_2 in [cus_enum.CardColor.BLUE,cus_enum.CardColor.PURPLE,cus_enum.CardColor.GOLD]:
                        log.logger.info("进入史诗页面")
                        all_color_count_map[card_color_2] += 1
                        full_color_count_map[card_color_2] += 1
                        if turbo_paused:
                            time.sleep(1)
                            continue
                    
                        if turbo_stop:
                            break

                        # 白票连续绿卡记录清空
                        count_white_streak = 0
                        
                        if not toTargetPage(hwnd,EPIC_DRAW_SETP,cus_enum.PageType.EPIC_CARD_DRAW):
                            log.logger.info("进入史诗页面失败，重新开始")
                            continue
                        
                        if is_change_wish_list:
                            print("调整史诗心愿单金卡顺序")
                            is_success =wish_list.epic_list_run(hwnd,target_epic_list,target_full_list,cards_map)
                            if not is_success:
                                log.logger.info("史诗模式，调整心愿单失败，重新开始")
                                continue
                            is_need_change_full_wish_list = True
                        # 史诗抽卡
                        log.logger.info("开始史诗第一抽")
                        if turbo_paused:
                            time.sleep(1)
                            continue
                    
                        if turbo_stop:
                            break
                        
                        if not toTargetPage(hwnd,EPIC_DRAW_ONCE_STEP,cus_enum.PageType.DRAW_AGAIN_ONCE,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                            log.logger.info("史诗第一抽失败，重新开始")
                            continue
                        time.sleep(2)
                        card_color_3 = utils.get_card_color(hwnd)
                        log.logger.info("史诗第一抽颜色:%s",card_color_3.name)
                        
                        red_tickets -= 1
                        draw_count += 1
                        epic_draw_count += 1
                        all_color_count_map[card_color_3] += 1
                        epic_color_count_map[card_color_3] += 1
                        if card_color_3 == cus_enum.CardColor.GREEN:
                            #史诗绿卡，重新开始
                            log.logger.info("史诗第一抽绿色,重新开始")
                            continue
                        if card_color_3 in [cus_enum.CardColor.BLUE,cus_enum.CardColor.PURPLE]:
                            # 如果神魔模式
                            if is_draw_balls:
                                if turbo_paused:
                                    time.sleep(1)
                                    continue
                            
                                if turbo_stop:
                                    break
                        
                                log.logger.info("进入神魔模式，开始史诗第二抽")
                                # 史诗抽卡
                                if not toTargetPage(hwnd,EPIC_DRAW_ONCE_STEP,cus_enum.PageType.DRAW_AGAIN_ONCE,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                                    log.logger.info("史诗第二抽失败，重新开始")
                                    continue
                                time.sleep(2)
                                card_color_4 = utils.get_card_color(hwnd)
                                log.logger.info("史诗第二抽颜色:%s",card_color_4.name)
                                
                                red_tickets -= 1
                                draw_count += 1
                                epic_draw_count += 1
                                all_color_count_map[card_color_4] += 1
                                epic_color_count_map[card_color_4] += 1
                                
                                if card_color_4 == cus_enum.CardColor.GREEN:
                                    #史诗绿卡，重新开始
                                    log.logger.info("史诗第二抽绿色,重新开始")
                                    continue
                                if card_color_4 in [cus_enum.CardColor.BLUE,cus_enum.CardColor.PURPLE,cus_enum.CardColor.GOLD]:
                                    log.logger.info("史诗第二抽蓝紫金，跳转神魔十连")
                                    if turbo_paused:
                                        time.sleep(1)
                                        continue
                                
                                    if turbo_stop:
                                        break
                        
                                    #去神魔界面
                                    if not toTargetPage(hwnd,STAR_ORIGIN_SETP,cus_enum.PageType.STAR_ORIGIN_DRAW):
                                        log.logger.info("去神魔页面失败，重新开始")
                                        continue
                                    # 占卜十次
                                    if turbo_paused:
                                        time.sleep(1)
                                        continue
                                
                                    if turbo_stop:
                                        break
                                    log.logger.info("开始神魔十连")
                                    if not toTargetPage(hwnd,ORIGIN_STAR_TEHTH_STEP,cus_enum.PageType.DRAW_TENTH_AGAIN):
                                        log.logger.info("抽象神魔十连失败，重新开始")
                                        continue
                                    ball_tickets -= 10
                                    continue
                            else:
                                log.logger.info("进入史诗模式，开始史诗第二抽")
                                # 史诗模式，循环单抽
                                if turbo_paused:
                                    time.sleep(1)
                                    continue
                            
                                if turbo_stop:
                                    break
                                
                                while True:
                                    log.logger.info("跳转史诗界面")
                                    if turbo_paused:
                                        break
                            
                                    if turbo_stop:
                                        break
                                    
                                    log.logger.info("开始史诗抽卡")
                                    if turbo_paused:
                                        break
                            
                                    if turbo_stop:
                                        break
                                    if not toTargetPage(hwnd,EPIC_DRAW_ONCE_STEP,cus_enum.PageType.DRAW_AGAIN_ONCE,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                                        break
                                    time.sleep(2)
                                    card_color_5 = utils.get_card_color(hwnd)
                                    log.logger.info("史诗抽卡颜色:%s",card_color_5.name)
                                    
                                    red_tickets -= 1
                                    draw_count += 1
                                    epic_draw_count += 1
                                    all_color_count_map[card_color_3] += 1
                                    epic_color_count_map[card_color_3] += 1
                                    
                                    # 如果出绿，出金结束，否则继续
                                    if card_color_5 in [cus_enum.CardColor.GREEN, cus_enum.CardColor.GOLD]:
                                        log.logger.info("史诗抽卡绿色,重新开始")
                                        break
                        elif card_color_3 == cus_enum.CardColor.GOLD:
                            if is_draw_balls:
                                if turbo_paused:
                                    time.sleep(1)
                                    continue
                            
                                if turbo_stop:
                                    break
                                
                                log.logger.info(",神魔模式：史诗第一抽金色,去神魔界面")
                                #去神魔界面
                                if not toTargetPage(hwnd,STAR_ORIGIN_SETP,cus_enum.PageType.STAR_ORIGIN_DRAW):
                                    log.logger.info("跳转神魔界面失败,重新开始")
                                    continue
                                # 占卜十次
                                if turbo_paused:
                                    time.sleep(1)
                                    continue
                            
                                if turbo_stop:
                                    break
                                
                                log.logger.info("开始神魔十连")
                                if not toTargetPage(hwnd,ORIGIN_STAR_TEHTH_STEP,cus_enum.PageType.DRAW_TENTH_AGAIN):
                                    log.logger.info("抽象神魔十连失败，重新开始")
                                    continue
                                ball_tickets -= 10
                                continue
                            else:
                                log.logger.info("史诗模式，史诗第一抽金色结束,重新开始")
                                continue
            else:
                time.sleep(1)
        if draw_count > 0 and full_draw_count > 0 and epic_draw_count > 0:
            log.logger.info(f"抽卡统计:")
            log.logger.info(f"总金卡概率:{all_color_count_map[cus_enum.CardColor.GOLD]}/{draw_count}={(all_color_count_map[cus_enum.CardColor.GOLD]/draw_count):.2f}")
            log.logger.info(f"总紫卡概率:{all_color_count_map[cus_enum.CardColor.PURPLE]}/{draw_count}={(all_color_count_map[cus_enum.CardColor.PURPLE]/draw_count):.2f}")
            
            log.logger.info(f"全英雄卡池金卡概率:{full_color_count_map[cus_enum.CardColor.GOLD]}/{full_draw_count}={(full_color_count_map[cus_enum.CardColor.GOLD]/full_draw_count):.2f}")
            log.logger.info(f"全英雄卡池紫卡概率:{full_color_count_map[cus_enum.CardColor.PURPLE]}/{full_draw_count}={(full_color_count_map[cus_enum.CardColor.PURPLE]/full_draw_count):.2f}")
            
            log.logger.info(f"史诗卡池金卡概率:{epic_color_count_map[cus_enum.CardColor.GOLD]}/{epic_draw_count}={(epic_color_count_map[cus_enum.CardColor.GOLD]/epic_draw_count):.2f}")
            log.logger.info(f"史诗卡池紫卡概率:{epic_color_count_map[cus_enum.CardColor.PURPLE]}/{epic_draw_count}={(epic_color_count_map[cus_enum.CardColor.PURPLE]/epic_draw_count):.2f}")
    except KeyboardInterrupt:  
        print("Script interrupted by user.")
        
def direct_draw_full_mode(hwnd,limit_times,limit_count,target_full_list=["3-y","4-y","32-l","33-l","44-w","17-m","16-m","45-w"],target_epic_list=["18-m","44-w","17-m","16-m","45-w"],full_back_up_wish_list=['18-m'],epic_back_up_wish_list=['3-y']):
    limit_begin_h = limit_times[0]
    limit_end_h = limit_times[1]
    limit_begin_m = limit_times[2]
    limit_end_m = limit_times[3]
    log.logger.info("时间窗口期  小时：%d-%d 分钟: %d-%d",limit_begin_h,limit_end_h,limit_begin_m,limit_end_m)
    
    full_color_count_map = {cus_enum.CardColor.GREEN:0,cus_enum.CardColor.BLUE:0,cus_enum.CardColor.PURPLE:0,cus_enum.CardColor.GOLD:0}
    
    is_change_wish_list = True
   

    cards_map = wish_list.get_card_map(config.GOLD_CARD_PATH)
    if is_change_wish_list:
        is_success =wish_list.full_list_run(hwnd,target_epic_list,target_full_list,cards_map)
        if not is_success:
            log.logger.info("普池模式，调整心愿单失败，重新开始")

    draw_count = 0
    while True:
        if turbo_paused:
            time.sleep(1)
            continue
        
        if turbo_stop:
            break
        
        current_time = datetime.now()
        current_hour = current_time.hour
        current_min = current_time.minute
        is_in_limit_m = True
        if limit_begin_m > limit_end_m:
            is_in_limit_m = (current_min >= limit_begin_m or current_min <= limit_end_m)
        else :
            is_in_limit_m = (current_min >= limit_begin_m and current_min <= limit_end_m)
        if (current_hour >= limit_begin_h and current_hour <= limit_end_h) and is_in_limit_m:
            log.logger.info("================================时间符合:%s:%s",str(current_hour),str(current_min))
            log.logger.info("当前次数限制:%s,当前已抽次数:%s",str(limit_count),str(draw_count))
            if draw_count >= limit_count:
                break
            # 第一步进入主界面
            if not toTargetPage(hwnd,MAIN_PAGE_SETP,cus_enum.PageType.MAIN_PAGE):
                log.logger.info("进入主页面失败,重新开始")
                #进入目标页面失败,重新开始
                continue
            
            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
        
            log.logger.info("进入主页面")
            #第二步 主界面跳转+调整时间
            is_success = False
            for i in range(5):
                is_success = main_page_refresh(hwnd)
                if is_success:
                    break
            if not is_success:
                log.logger.info("主页面跳转+调整时间失败")
                continue
            
            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
            
            log.logger.info("主页面跳转+调整时间完成")
            if not toTargetPage(hwnd,FULL_LIST_DRAW_SETP,cus_enum.PageType.FULL_CARD_DRAW):
                #进入目标页面失败
                log.logger.info("进入全英雄页面失败")
                continue
            
            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
            
             # 第三步普池抽卡
            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
            
            while True:
                log.logger.info("开始普池抽卡")
                if not toTargetPage(hwnd,FULL_LIST_DRAW_ONECE_STEP,cus_enum.PageType.DRAW_AGAIN_ONCE,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
                    log.logger.info("普池第抽卡失败，重新开始")
                    continue
                time.sleep(2)
                card_color_1 = utils.get_card_color(hwnd)
                log.logger.info("普池抽卡颜色:%s",card_color_1.name)
                draw_count += 1
                full_color_count_map[card_color_1] += 1
                if card_color_1 == cus_enum.CardColor.GREEN or card_color_1 == cus_enum.CardColor.UNKNOWN:
                    log.logger.info("普池抽卡颜色:%s,重新开始",card_color_1.name)
                    #普池绿卡，重新开始
                    break
                if full_color_count_map[cus_enum.CardColor.GOLD] >= 2:
                    break
                time.sleep(0.5)
                
            if full_color_count_map[cus_enum.CardColor.GOLD] >= 2:
                break
    if draw_count > 0 :
        log.logger.info(f"抽卡统计:")
        log.logger.info(f"全英雄卡池金卡概率:{full_color_count_map[cus_enum.CardColor.GOLD]}/{draw_count}={(full_color_count_map[cus_enum.CardColor.GOLD]/draw_count):.2f}")
        log.logger.info(f"全英雄卡池紫卡概率:{full_color_count_map[cus_enum.CardColor.PURPLE]}/{draw_count}={(full_color_count_map[cus_enum.CardColor.PURPLE]/draw_count):.2f}")
        

def idle_mode(hwnd):
    failed_count = 0
    current_plagiarize_number = 2
    talent_fight = True
    success_count = 0
    # 当前挑战第几局
    game_number = 1
    while True:
        if turbo_paused:
            time.sleep(1)
            continue
        
        if turbo_stop:
            break
        current_page_type,_ = get_current_page_type(hwnd)
        log.logger.info(f"当前使用第{current_plagiarize_number+1}个通关作业,当前尝试次数:{failed_count}")
        if current_page_type not in [cus_enum.PageType.IDLE_PAGE,cus_enum.PageType.READY_FIGHT_PAGE]:
            # 第一步进入主界面
            if not toTargetPage(hwnd,MAIN_PAGE_SETP,cus_enum.PageType.MAIN_PAGE):
                log.logger.info("进入主页面失败,重新开始")
                #进入目标页面失败,重新开始
                continue
            

            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
            if not toTargetPage(hwnd,[[cus_enum.PageType.MAIN_PAGE,['当前进度','当前迸度']]],cus_enum.PageType.IDLE_PAGE):
                log.logger.info("进入挂机页面失败,重新开始")
                continue
            
            if turbo_paused:
                time.sleep(1)
                continue
            
            if turbo_stop:
                break
        if current_plagiarize_number >= 6 and failed_count > 3:
            log.logger.info("失败次数太多，尝试切换挑战类型")
            talent_fight = not talent_fight
            
        if talent_fight :
            to_fight_step = [[cus_enum.PageType.IDLE_PAGE,['天赋挑战']]]
        else:
            to_fight_step = [[cus_enum.PageType.IDLE_PAGE,['挑战']]]
        
        log.logger.info("进入准备战斗页面") 
        if not toTargetPage(hwnd,to_fight_step,cus_enum.PageType.READY_FIGHT_PAGE):
            log.logger.info("进入准备战斗页面失败,重新开始")
            continue
            
          
        if not toTargetPage(hwnd,[[cus_enum.PageType.READY_FIGHT_PAGE,['通关记录']]],cus_enum.PageType.PLAGIARIZE_PAGE):
            log.logger.info("进入抄作业页面失败,重新开始")
            continue
        

        if failed_count >= 7:
            failed_count = 0
            current_plagiarize_number += 1
            
        for i in range(current_plagiarize_number):
            utils.clickIntoByButtonName(hwnd,['next.png'],[])
            time.sleep(0.3)
        
        count = 1
        while True:
            count += 1
            if count > 6:
                break
            current_page_type ,ocr_res = get_current_page_type(hwnd)
            if current_page_type != cus_enum.PageType.PLAGIARIZE_PAGE:
                break
            is_find_no_card = False
            for o in ocr_res:
                if o[1] == '未拥有' or o[1] == '末拥有':
                    current_plagiarize_number +=1
                    utils.clickIntoByButtonName(hwnd,['next.png'],[])
                    is_find_no_card = True
                    time.sleep(1)
                    break
            if not is_find_no_card:
                break
            time.sleep(1)
        if not toTargetPage(hwnd,[[cus_enum.PageType.PLAGIARIZE_PAGE,['一键采用']],[cus_enum.PageType.NO_HERO_PAGE,['确定']],[cus_enum.PageType.CONFIMR_PAGE,['confirm.png']]],cus_enum.PageType.READY_FIGHT_PAGE):
            log.logger.info("进入抄作业页面失败,重新开始")
            continue
        
        # # 检查是否有不存在的英雄或回响
        # time.sleep(0.5)
        # current_page_type,ocr_result= get_current_page_type(hwnd)
        # print("check no hero page",current_page_type)
        # if current_page_type == cus_enum.PageType.NO_HERO_PAGE:
        #     current_plagiarize_number += 1
        #     utils.clickIntoByButtonName(hwnd,['取消'],ocr_result)
        #     continue
        
        time.sleep(1)
        if game_number == 2:
            count = 0
            while True:
                count += 1
                if count > 4:
                    break
                if utils.clickIntoByButtonName(hwnd,['game2.png'],[]):
                    break
                time.sleep(0.3)
                
        print('准备开始战斗')
        if not toTargetPage(hwnd,[[cus_enum.PageType.READY_FIGHT_PAGE,['战斗']]],cus_enum.PageType.FIGHTING_PAGE):
            log.logger.info("进入战斗页面失败,重新开始")
            continue
        while True:
            current_page_type,_ = get_current_page_type(hwnd)
            if current_page_type == cus_enum.PageType.FIGHTING_PAGE:
                time.sleep(2)
                continue
            if current_page_type in [cus_enum.PageType.FIGHT_FAIL_PAGE,cus_enum.PageType.FIGHT_SUCCESS_1_PAGE,cus_enum.PageType.FIGHT_SUCCESS_2_PAGE]:
                print("战斗结束",current_page_type)
                break
            time.sleep(0.5)
        if current_page_type == cus_enum.PageType.FIGHT_SUCCESS_1_PAGE:
            if not toTargetPage(hwnd,[[cus_enum.PageType.FIGHT_SUCCESS_1_PAGE,['继续挑战']]],cus_enum.PageType.READY_FIGHT_PAGE):
                log.logger.info("进入抄作业页面失败,重新开始")
                continue
            if not toTargetPage(hwnd,[[cus_enum.PageType.READY_FIGHT_PAGE,['战斗']]],cus_enum.PageType.FIGHTING_PAGE):
                log.logger.info("进入战斗页面失败,重新开始")
                continue
            game_number = 2
            # 第二局战斗开始
            count = 0
            while True:
                count += 1
                if count > 30:
                    break
                time.sleep(0.5)
                current_page_type,_ = get_current_page_type(hwnd)
                if current_page_type == cus_enum.PageType.FIGHTING_PAGE:
                    time.sleep(2)
                    continue
                if current_page_type in [cus_enum.PageType.FIGHT_FAIL_PAGE,cus_enum.PageType.FIGHT_SUCCESS_2_PAGE]:
                    print("战斗2结束",current_page_type)
                    break
            
            if current_page_type == cus_enum.PageType.FIGHT_SUCCESS_2_PAGE:
                failed_count = 0
                current_plagiarize_number = 2
                success_count += 1
                game_number = 1
                if not toTargetPage(hwnd,[[cus_enum.PageType.FIGHT_SUCCESS_2_PAGE,['天赋挑战','挑战']]],cus_enum.PageType.READY_FIGHT_PAGE):
                    log.logger.info("进入战斗页面失败,重新开始")
                    continue
            elif current_page_type == cus_enum.PageType.FIGHT_FAIL_PAGE:
                print("第二局失败，失败次数加一")
                failed_count += 1
                if not toTargetPage(hwnd,[[cus_enum.PageType.FIGHT_FAIL_PAGE,['继续挑战']]],cus_enum.PageType.READY_FIGHT_PAGE):
                    log.logger.info("进入战斗页面失败,重新开始")
                    continue
        elif current_page_type == cus_enum.PageType.FIGHT_FAIL_PAGE:
            print("第一局失败，失败次数加一")
            failed_count += 1
            if not toTargetPage(hwnd,[[cus_enum.PageType.FIGHT_FAIL_PAGE,['继续挑战']]],cus_enum.PageType.READY_FIGHT_PAGE):
                log.logger.info("进入战斗页面失败,重新开始")
                continue
        elif current_page_type == cus_enum.PageType.FIGHT_SUCCESS_2_PAGE:
            print("战斗2结束",current_page_type)
            failed_count = 0
            current_plagiarize_number = 2
            success_count += 1
            game_number = 1
            if not toTargetPage(hwnd,[[cus_enum.PageType.FIGHT_SUCCESS_2_PAGE,['天赋挑战','挑战']]],cus_enum.PageType.READY_FIGHT_PAGE):
                log.logger.info("进入战斗页面失败,重新开始")
        
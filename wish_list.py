import os
import utils
import config
import cv2
import numpy as np
import pyautogui
import time
import log

CARDS_SWAP_WIDTH_RATIO = 0.104
CARDS_SWAP_HEIGHT_RATIO = 0.062
def full_list_run(hwnd,target_epic_wish_list,target_full_wish_list,cards_map):
    if not reset_full_wish_list(hwnd,target_epic_wish_list,target_full_wish_list,cards_map,False):
        print("心愿单校验失败，重新开始")
        return False
    count = 0
    print('开始关闭心愿单')
    while True:
        time.sleep(0.3)
        if count > 6:
            break
        imagePath,_,_,_,_ = utils.window_screenshot(hwnd)
        ocr_select_result = config.READER.readtext(imagePath)
        os.remove(imagePath)
        if not utils.clickIntoByButtonName(hwnd,["点击空白处关闭","点击空自处关闭"],ocr_select_result):
            time.sleep(0.4)
            count += 1
            continue
        break
    if count > 6:
        print("关闭心愿页面失败")
        return False
    time.sleep(0.4)
    imagePath,_,_,_,_ = utils.window_screenshot(hwnd)
    ocr_select_result = config.READER.readtext(imagePath)
    os.remove(imagePath)
    if not utils.clickIntoByButtonName(hwnd,["史诗招募"],ocr_select_result):
        print("进入史诗招募页面失败")
        return False
    time.sleep(0.4)
    reset_epic_wish_list(hwnd,target_epic_wish_list,target_full_wish_list,cards_map,True)
    time.sleep(0.4)
    if not utils.clickIntoByButtonName(hwnd,["全英雄招募"],ocr_select_result):
        print("返回全英雄招募页面失败")
        return False
    time.sleep(0.4)
    return True

def epic_list_run(hwnd,target_epic_list,target_full_list,cards_map):
    reset_epic_wish_list(hwnd,target_epic_list,target_full_list,cards_map,False)
    time.sleep(0.2)
    imagePath,_,_,_,_ = utils.window_screenshot(hwnd)
    ocr_select_result = config.READER.readtext(imagePath)
    os.remove(imagePath)
    if not utils.clickIntoByButtonName(hwnd,["全英雄招募"],ocr_select_result):
        print("进入全英雄招募页面失败")
        return
    time.sleep(0.2)
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    ocr_result = config.READER.readtext(image)
    utils.clickIntoByButtonName(hwnd,['心愿单'],ocr_result)
    time.sleep(0.2)
    reset_full_wish_list(hwnd,target_epic_list,target_full_list,cards_map,True)
        
    count = 0
    while True:
        if count > 6:
            break
        imagePath,_,_,_,_ = utils.window_screenshot(hwnd)
        ocr_select_result = config.READER.readtext(imagePath)
        os.remove(imagePath)
        if not utils.clickIntoByButtonName(hwnd,["点击空白处关闭","点击空自处关闭"],ocr_select_result):
            time.sleep(0.3)
            count += 1
            continue
        break
    if count > 6:
        print("关闭心愿页面失败")
        return
    time.sleep(0.2)
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    ocr_result = config.READER.readtext(image)
    if not utils.clickIntoByButtonName(hwnd,["史诗招募"],ocr_result):
        print("进入史诗招募页面失败")
        return
    return True
def reset_full_wish_list(hwnd,target_epic_list,target_full_list,cards_map,is_for_epic_list):
    # 第一步清空心愿单
    clear_full_wish_list(hwnd,target_epic_list,target_full_list,cards_map)
    # 重新设置心愿单
    # 把当前心愿的种族顺调整为target wish list的种族顺序
    # 识别当前心愿单,结构[cardNumber,cardPoint]
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    current_wish_list = get_current_screen_cards_m(image,cards_map,w,h,0.08,0.05)
    sorted_current_wish_list = []
    for t in target_full_list:
        for c in current_wish_list:
            if t.split("-")[1] == c[0].split("-")[1]:
                current_wish_list.remove(c)
                sorted_current_wish_list.append(c)
                break
    
    target_cards_map = []
    for t in target_full_list:
        for cm in cards_map:
            if cm[0] == t:
                target_cards_map.append(cm)
                break
    
    if is_for_epic_list:
         sorted_current_wish_list = sorted_current_wish_list[-3:]
         target_full_list = target_full_list[-3:]
         target_cards_map = target_cards_map[-3:]
    
    i = 0   
    for cwl in sorted_current_wish_list:
        if cwl[0] not in target_full_list:
            pyautogui.click(cwl[1][0]+left,cwl[1][1]+top)
            time.sleep(0.3)
            #截图
            selectImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
            ocr_select_result = config.READER.readtext(selectImagePath)
            sImage = cv2.imread(selectImagePath)
            os.remove(selectImagePath)
            current_target_cards = get_current_screen_cards_m(sImage,[target_cards_map[i]],sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
            if len(current_target_cards) > 0:
                card = current_target_cards[0]
                pyautogui.click(card[1][0]+left,card[1][1]+top)
                time.sleep(0.3)
            utils.clickIntoByButtonName(hwnd,["保存编辑"],ocr_select_result)
            try_to_confirm(hwnd)
            time.sleep(0.5)
        i += 1
    if is_for_epic_list:
        return True
    
    # 校验心愿单
    print('开始校验全英雄心愿单')
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    current_wish_list = get_current_screen_cards_m(image,cards_map,w,h,0.08,0.05)
    for c in current_wish_list:
        if c[0] not in target_full_list:
            return False
    time.sleep(0.3)
    return True
            
def reset_epic_wish_list(hwnd,target_epic_wish_list,target_full_wish_list,cards_map,is_for_full_list):
    print("开始重置史诗心愿单")
    clear_epic_wish_list(hwnd,target_epic_wish_list,target_full_wish_list,cards_map)
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    # 识别当前心愿单,结构[cardNumber,cardPoint]
    CARDS_WIDTH_RATIO = 0.104
    CARDS_HEIGHT_RATIO = 0.062
    
    if is_for_full_list:
        # 获取心愿单里最后三个卡
        target_epic_wish_list = target_epic_wish_list[-3:]
   
    target_cards_map = []
    for t in target_epic_wish_list:
        for cm in cards_map:
            if cm[0] == t:
                target_cards_map.append(cm)
                break
    current_wish_list = get_current_screen_cards_m(image,cards_map,w,h,CARDS_WIDTH_RATIO,CARDS_HEIGHT_RATIO)
    i = 0
    for c in current_wish_list:
        if i > len(target_epic_wish_list) - 1:
            break
        if c[0] not in target_epic_wish_list:
            pyautogui.click(c[1][0]+left,c[1][1]+top)
            time.sleep(0.5)
            #截图
            sImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
            ocr_select_result = config.READER.readtext(sImagePath)
            sImage = cv2.imread(sImagePath)
            os.remove(sImagePath)
            
            s_cards = get_current_screen_cards_m(sImage,[target_cards_map[i]],sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
            limitH = int(sh * 0.4)
            if len(s_cards) == 0:
                moveToX = int(sw / 2) 
                moveToY = int(sh / 2) + 200
                pyautogui.moveTo(moveToX+left, moveToY+top, duration=0.1)
                pyautogui.dragTo(moveToX+left,moveToY+top - 300, button='left',duration=0.3)
                time.sleep(0.4)
                scrollImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
                sImage = cv2.imread(scrollImagePath)
                os.remove(scrollImagePath)
                s_cards = get_current_screen_cards_m(sImage,[target_cards_map[i]],sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
            for sc in s_cards:
                if sc[1][1] > limitH:
                    pyautogui.click(sc[1][0]+left,sc[1][1]+top)
                    time.sleep(0.4)
                    break
            utils.clickIntoByButtonName(hwnd,["保存编辑"],ocr_select_result)
            try_to_confirm(hwnd)
            time.sleep(0.5)
        i+=1
    if is_for_full_list:
        return True
    
    # 再次获取当前心愿，校验是否正确
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    current_wish_list = get_current_screen_cards_m(image,cards_map,w,h,CARDS_WIDTH_RATIO,CARDS_HEIGHT_RATIO)
    for c in current_wish_list:
        if c[0] not in target_epic_wish_list:
            return False
    return True
def clear_full_wish_list(hwnd,target_epic_list,target_wish_list,cards_map):
    is_success = False
    if len(target_wish_list) != 8:
        return is_success
    
    #截图
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    ocr_result = config.READER.readtext(image)
    utils.clickIntoByButtonName(hwnd,['心愿单'],ocr_result)
    time.sleep(0.4)
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    
    # 识别当前心愿单,结构[cardNumber,cardPoint]
    current_wish_list = get_current_screen_cards_m(image,cards_map,w,h,0.08,0.05)
    not_in_target_list = []
    for c in cards_map:
        if c[0] not in target_wish_list and c[0] not in target_epic_list:
            not_in_target_list.append(c)
            
    for t in target_wish_list:
        for current in current_wish_list:
            if t == current[0]:
                pyautogui.click(current[1][0]+left,current[1][1]+top)
                time.sleep(0.3)
                #截图
                sImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
                ocr_select_result = config.READER.readtext(sImagePath)
                sImage = cv2.imread(sImagePath)
                os.remove(sImagePath)
               
                s_cards = get_current_screen_cards_m(sImage,not_in_target_list,sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
                limitH = int(sh * 0.6)
                for sc in s_cards:
                    if sc[1][1] > limitH:
                        pyautogui.click(sc[1][0]+left,sc[1][1]+top)
                        time.sleep(0.4)
                        break
                utils.clickIntoByButtonName(hwnd,["保存编辑"],ocr_select_result)
                try_to_confirm(hwnd)
                time.sleep(0.4)
                
def clear_epic_wish_list(hwnd,target_epic_list,target_full_list,cards_map):
    print("开始清空史诗心愿单！")
    is_success = False
    if len(target_epic_list) != 5:
        return is_success
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    os.remove(imagePath)
    # 识别当前心愿单,结构[cardNumber,cardPoint]
    CARDS_WIDTH_RATIO = 0.104
    CARDS_HEIGHT_RATIO = 0.062 
    current_wish_list = get_current_screen_cards_m(image,cards_map,w,h,CARDS_WIDTH_RATIO,CARDS_HEIGHT_RATIO)
    not_in_target_list = []
    for c in cards_map:
        if c[0] not in target_epic_list and c[0] not in target_full_list:
            not_in_target_list.append(c)
            
    for t in target_epic_list:
        for current in current_wish_list:
            if t == current[0]:
                print("find:",t)
                pyautogui.click(current[1][0]+left,current[1][1]+top)
                time.sleep(0.5)
                #截图
                sImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
                ocr_select_result = config.READER.readtext(sImagePath)
                sImage = cv2.imread(sImagePath)
                os.remove(sImagePath)
                CARDS_SWAP_WIDTH_RATIO = 0.104
                CARDS_SWAP_HEIGHT_RATIO = 0.062 
                s_cards = get_current_screen_cards_m(sImage,not_in_target_list,sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
                limitH = int(sh * 0.4)
                for sc in s_cards:
                    if sc[1][1] > limitH:
                        pyautogui.click(sc[1][0]+left,sc[1][1]+top)
                        time.sleep(0.4)
                        break
                utils.clickIntoByButtonName(hwnd,["保存编辑"],ocr_select_result)
                try_to_confirm(hwnd)
                time.sleep(0.4)
    is_success = True
    return is_success
def get_card_map(cart_path):
    # cardsMap [cardNumber=1-y,2-y,cardImage=[...]]
    cardsMap = []
    for filename in os.listdir(cart_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = cv2.imread(config.GOLD_CARD_PATH + filename)
            # resized_img = cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_AREA)
            sp = filename.split('.')
            cardsMap.append([sp[0] ,img])
    return cardsMap

def getCurrentScreenCards(image,cards_map,w,h,w_radio,h_radio):
    calW = int(w * w_radio)
    calH = int(h * h_radio)
    current_card_list = []
    for cm in cards_map:
        cardNumber = cm[0]
        card = cm[1]
        resized_img = cv2.resize(card, (calW, calH), interpolation=cv2.INTER_AREA)
        # 使用matchTemplate函数在大图中搜索模板  
        res = cv2.matchTemplate(image, resized_img, cv2.TM_CCOEFF_NORMED)  
        # 设置一个阈值，用于确定匹配的程度  
        threshold = 0.75
        
        loc = np.where(res >= threshold)  
        # 在原图上绘制矩形框，标记出匹配的位置
        pts = list(zip(*loc[::-1]))
        if len(pts)>0 :
            pt = pts[0]
            current_card_list.append([cardNumber,pt])
            # cv2.rectangle(image, pt, (pt[0] + calW, pt[1] + calH), (0, 255, 0), 2)
            # cv2.imshow('Detected', image)  
            # cv2.waitKey(0) 
            
    return current_card_list

def getCurrentScreenPointMatchCards(image,cards_map,w,h,w_radio,h_radio):
    calW = int(w * w_radio)
    calH = int(h * h_radio)
    current_cards = []
    for cm in cards_map:
        cardNumber = cm[0]
        card = cm[1]
        resized_img = cv2.resize(card, (calW, calH), interpolation=cv2.INTER_AREA)
        # 使用matchTemplate函数在大图中搜索模板  
        sift = cv2.SIFT_create()  # 或者 cv2.ORB_create() for ORB
        keypoints_image, descriptors_image = sift.detectAndCompute(image, None)
        keypoints_template, descriptors_template = sift.detectAndCompute(resized_img, None)
        # # 创建 BFMatcher 并进行匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors_template, descriptors_image, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        if len(good_matches) > 40:
            pt = keypoints_image[good_matches[0].trainIdx].pt
            current_cards.append([cardNumber,pt])
            break
    return current_cards

def get_current_screen_cards_m(image,cards_map,w,h,w_radio,h_radio):
    cards= getCurrentScreenCards(image,cards_map,w,h,w_radio,h_radio)
    print(cards)
    if len(cards) > 0:
        return cards
    else:
        cards = getCurrentScreenPointMatchCards(image,cards_map,w,h,w_radio,h_radio)
        return cards
    
def change_wish_list_for_max_cards(hwnd,cards_map,full_back_up_wish_list,epic_back_up_wish_list):
    # 识别当前英雄
     #截图
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
    image = cv2.imread(imagePath)
    #识别图片内容
    ocr_result = config.READER.readtext(imagePath)
    os.remove(imagePath)
    # 110/1155, 120/2093
    cards = getCurrentScreenPointMatchCards(image,cards_map,w,h,0.095,0.057)
    if len(cards) == 0:
        log.logger.info("无法找到模板英雄，退出心愿单调整")
        return False
    cardNumber = cards[0][0]
    log.logger.info("需要编辑的英雄:%s",cardNumber)
    if not utils.clickIntoByButtonName(hwnd,['编辑英雄'],ocr_result):
        return False
    time.sleep(0.2)
    # 进入心愿单编辑
    wish_list_path,w,h,left,top = utils.window_screenshot(hwnd)
    image = cv2.imread(wish_list_path)
    #识别图片内容
    ocr_result = config.READER.readtext(wish_list_path)
    os.remove(wish_list_path)
    wish_list_type = 0
    for ocr in ocr_result:
        if ocr[1] == '耀光帝国' or ocr[1] == '蛮血部落' or ocr[1] == '绿裔联盟' or ocr[1] == '亡灵眷族':
            # 全英雄心愿单调整
            print("1")
            wish_list_type = 1
            break
        elif ocr[1] == '自选英雄':
            # 史诗英雄心愿单调整
            print("2")
            wish_list_type = 2
            break
    
    if wish_list_type == 0:
        log.logger.info("无法识别心愿单界面类型")
        return False
    elif wish_list_type == 1:
        # 全英雄心愿单调整
        cards = get_current_screen_cards_m(image,cards_map,w,h,0.08,0.05)
        for c in cards:
            if c[0] == cardNumber:
                pyautogui.click(c[1][0]+left,c[1][1]+top)
                break
        time.sleep(0.2)
        selectImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
        ocr_select_result = config.READER.readtext(selectImagePath)
        sImage = cv2.imread(selectImagePath)
        os.remove(selectImagePath)
        for cm in cards_map:
            if cm[0] in full_back_up_wish_list:
                current_target_cards = get_current_screen_cards_m(sImage,[cm],sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
                isFind = False
                if len(current_target_cards) > 0:
                    card = current_target_cards[0]
                    pyautogui.click(card[1][0]+left,card[1][1]+top)
                    time.sleep(0.2)
                    isFind = True
                if isFind:
                    utils.clickIntoByButtonName(hwnd,["保存编辑"],ocr_select_result)
                    try_to_confirm(hwnd)
                    time.sleep(0.2)
        count = 0
        while True:
            if count > 6:
                break
            imagePath,_,_,_,_ = utils.window_screenshot(hwnd)
            ocr_select_result = config.READER.readtext(imagePath)
            os.remove(imagePath)
            if not utils.clickIntoByButtonName(hwnd,["点击空白处关闭","点击空自处关闭"],ocr_select_result):
                time.sleep(0.2)
                count += 1
                continue
            break
        if count > 6:
            print("关闭心愿页面失败")
            return False
    elif wish_list_type == 2:
        # 史诗英雄心愿单调整
        for cm in cards_map:
            if cm[0] in epic_back_up_wish_list:
                s_cards = get_current_screen_cards_m(image,[cm],w,h,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
                limitH = int(h * 0.4)
                if len(s_cards) == 0:
                    moveToX = int(w / 2) 
                    moveToY = int(h / 2) + 200
                    pyautogui.moveTo(moveToX+left, moveToY+top, duration=0.1)
                    pyautogui.dragTo(moveToX+left,moveToY+top - 300, button='left',duration=0.3)
                    time.sleep(0.4)
                    scrollImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
                    sImage = cv2.imread(scrollImagePath)
                    os.remove(scrollImagePath)
                    s_cards = get_current_screen_cards_m(sImage,[cm],sw,sh,CARDS_SWAP_WIDTH_RATIO,CARDS_SWAP_HEIGHT_RATIO)
                isFind = False
                for sc in s_cards:
                    if sc[1][1] > limitH:
                        pyautogui.click(sc[1][0]+left,sc[1][1]+top)
                        time.sleep(0.2)
                        isFind = True
                        break
                if isFind:
                    utils.clickIntoByButtonName(hwnd,["保存编辑"],ocr_result)
                    try_to_confirm(hwnd)
                    time.sleep(0.2)
    return True


def try_to_confirm(hwnd):
    sImagePath,sw,sh,left,top = utils.window_screenshot(hwnd)
    ocr_select_result = config.READER.readtext(sImagePath)
    os.remove(sImagePath)
    utils.clickIntoByButtonName(hwnd,['confirm.png'],ocr_select_result)
    time.sleep(0.5)
import utils
import cus_enum as ce
import route
import log
import time
import config
import pyautogui
import os
import random
import wish_list
from datetime import datetime

global_vars = {
    # 白票剩余数量
    'white_tickets':0,
    # 红票剩余数量
    'red_tickets':0,
    # 水晶球剩余数量
    'ball_tickets':0,
    # 窗口期开始小时：0-24
    'limit_begin_h':0,
    # 窗口期结束小时：0-24
    'limit_end_h':0,
    # 窗口期开始分钟数：0-60
    'limit_begin_m':0,
    # 窗口期结束分钟数：0-60
    'limit_end_m':0,
    # 白票连续出现绿色计数
    'count_white_streak':0,
    # 是否神魔模式
    'is_star_origin':False,
    # 抽卡总次数统计
    'draw_count':0,
    # 全英雄卡池抽卡次数统计
    'full_draw_count':0, 
    # 史诗卡池抽卡次数统计
    'epic_draw_count':0,
    # 总抽卡各个颜色数量记录
    'all_color_count_map':{ce.CardColor.GREEN:0,ce.CardColor.BLUE:0,ce.CardColor.PURPLE:0,ce.CardColor.GOLD:0},
    # 全英雄抽卡各个颜色数量记录
    'full_color_count_map':{ce.CardColor.GREEN:0,ce.CardColor.BLUE:0,ce.CardColor.PURPLE:0,ce.CardColor.GOLD:0},
    # 史诗抽卡各个颜色数量记录
    'epic_color_count_map':{ce.CardColor.GREEN:0,ce.CardColor.BLUE:0,ce.CardColor.PURPLE:0,ce.CardColor.GOLD:0},
    'gold_cards_map':[],
    'full_back_up_wish_list':[],
    'epic_back_up_wish_list':[],
}

# 把参数读取到global_vars中
# 抽卡窗口期
# 白票数量，红票数量，水晶球数量
# 是否为神魔模式
# 全英雄心愿单备选项
# 史诗英雄心愿单备选项
# 返回步骤：step_check_time
def step_begin(iso,limit_times,tickets,full_back_up_wish_list,epic_back_up_wish_list):
    global_vars['white_tickets'] = tickets[0]
    global_vars['red_tickets'] = tickets[1]
    global_vars['ball_tickets'] = tickets[2]
    global_vars['limit_begin_h'] = limit_times[0]
    global_vars['limit_end_h'] = limit_times[1]
    global_vars['limit_begin_m'] = limit_times[2]
    global_vars['limit_end_m'] = limit_times[3]
    global_vars['is_star_origin'] = iso
    global_vars['full_back_up_wish_list'] = full_back_up_wish_list
    global_vars['epic_back_up_wish_list'] = epic_back_up_wish_list
    # 读取所有金卡图片
    global_vars['gold_cards_map'] = wish_list.get_card_map(config.GOLD_CARD_PATH)
    return step_check_time
 
# 检查当前时间是否在窗口期内
# 如果在窗口期内返回True,step_check_stock
# 否则返回False
def step_check_time(**kwargs):
    limit_begin_h = global_vars['limit_begin_h']
    limit_end_h = global_vars['limit_end_h']
    limit_begin_m = global_vars['limit_begin_m']
    limit_end_m = global_vars['limit_end_m']
    next_step = step_check_stock
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
        log.logger.info("时间窗口期  小时：%d-%d 分钟: %d-%d",limit_begin_h,limit_end_h,limit_begin_m,limit_end_m)
        log.logger.info("进入窗口期，当前时间:%s:%s",str(current_hour),str(current_min))
        return True,next_step
    else:
        return False,None

# 检查当前库存数
# 如果红票，白票数量小于等于0，则返回False,None
# 如果神魔模式，水晶球数量小于10，返回False,None
# 否则返回True，step_check_white_streak
def step_check_stock(**kwargs):
    white_tickets = global_vars['white_tickets']
    red_tickets = global_vars['red_tickets']
    ball_tickets = global_vars['ball_tickets']
    is_star_origin = global_vars['is_star_origin']
    next_step = step_check_white_streak
    log.logger.info("当前库存数 白票:%s, 红票:%s, 水晶球:%s",str(white_tickets),str(red_tickets),str(ball_tickets))
    if white_tickets <= 0 or red_tickets <= 0:
        log.logger.info("库存不满足抽卡条件，退出")
        return False,None
    if is_star_origin and  ball_tickets <= 10:
        log.logger.info("神魔库存不满足抽卡条件，退出")
        return False,None
    return True,next_step

# 检查白票连续出绿次数
# 如果超过10次，休眠300S,返回False
# 并重置count_white_streak为0
# 否则返回True，step_to_main
def step_check_white_streak(**kwargs):
    next_step = step_to_main
    count_white_streak = global_vars["count_white_streak"]
    if count_white_streak > 10:
        time.sleep(300)
        log.logger.info(f"连续十次出绿色休眠300S")
        global_vars["count_white_streak"] = 0
        return False,None
    return True,next_step

# 进入主页面
# 期望当前页面：任何页面
# 目标页面：主页面
# 下一步：step_to_map
def step_to_main(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_to_map
    target_page_types = [ce.PageType.MAIN_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_MAIN_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入主页面失败,未找到按钮")
        return False,None
    return False,None

# 进入地图界面
# 期望当前界面：主界面
# 目标页面:地图页面
# 下一步：step_choose_big_map
def step_to_map(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_choose_big_map
    target_page_types = [ce.PageType.MAP_PAGE]
    current_page_type,_ = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    image_path,w,h,left,top = utils.window_screenshot(hwnd)
    # 计算截图右上角坐标
    mapX,mapY = utils.reCalTemplateSize(w,h,0.84,0.11)
    pyautogui.click(mapX+left,mapY+top)
    os.remove(image_path)
    return False,None

# 选择大地图类别
# 期望当前页面：地图界面
# 如果不在地图界面，返回False,None
# 点击大地图按钮成功后
# 不再对当前页面类型进行判断
# 直接返回True,step_choose_small_map
def step_choose_big_map(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_choose_small_map
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type != ce.PageType.MAP_PAGE:
        return False,None
    if not utils.clickIntoByButtonName(hwnd,["启程篇章"],ocr):
        log.logger.info("点击启程篇章失败,未找到按钮")
        return False,None
    return True,next_step

# 选择小地图类别
# 期望当前页面：地图界面
# 如果不在地图界面，返回False,None
# 随机选择点击小地图按钮成功后
# 不再对当前页面类型进行判断
# 直接返回True,step_choose_transmit
def step_choose_small_map(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_choose_transmit
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type != ce.PageType.MAP_PAGE:
        return False,None
    imagePath,_,h,_,top = utils.window_screenshot(hwnd)
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
        return False,None
    rand_index = random.randint(0,len(map_list)-1)
    rand_map_ocr = map_list[rand_index]
    x,y = utils.cal_center(hwnd,rand_map_ocr[0])
    pyautogui.click(x, y)
    return True,next_step

# 选择地图上的传送点
# 当前界面如果处于待确认界面，先点击确认，返回False，None
# 如果不在待确认界面，寻找传送点，并点击。返回True,step_transmit_to_main
# 如果没有找到返回False，None
def step_choose_transmit(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_transmit_to_main
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    # 如果需要确认，点击确认，然后返回False，再次尝试寻找传送点
    if current_page_type == ce.PageType.CONFIMR_PAGE:
        button_names = route.get_route_button_names([],current_page_type)
        utils.clickIntoByButtonName(hwnd,button_names,ocr)
        time.sleep(2)
        return False,None
    image_info = utils.window_screenshot(hwnd)
    image_path = image_info[0]
    # 28,51 28/1155=0.024 51/2093=0.024
    # 随机寻找地图上的传送点
    x,y = utils.matchTemplate(image_info,"transmit.png",0.024,0.024)
    if x == 0 and y == 0:
        return False,None
    pyautogui.click(x, y)
    os.remove(image_path)
    return True,next_step

# 选择传送点回到主界面
# 目标界面:主界面
# 寻找确认传递按钮，并点击
# 如果没有找到返回False，None
# 下一步:step_choose_time
def step_transmit_to_main(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_choose_time
    target_page_types = [ce.PageType.MAIN_PAGE]
    current_page_type,_ = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    image_info = utils.window_screenshot(hwnd)
    image_path = image_info[0]
    x,y = utils.matchTemplate(image_info,"jump.png",0.077,0.038)
    if x == 0 and y== 0:
        return False,None
    pyautogui.click(x,y)
    os.remove(image_path)
    return True,next_step

# 跳转时间界面
# 目标界面:跳转时间界面
# 期望当前界面:主界面
# 下一步：step_change_time
def step_choose_time(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_change_time
    image_info = utils.window_screenshot(hwnd)
    image_path = image_info[0]
    x,y = utils.matchTemplate(image_info,"time_icon.png",0.05,0.028)
    if x == 0 and y== 0:
        # 有可能时mumu广告遮挡，尝试关闭mumu广告
        utils.clickIntoByImage(hwnd,'mumu_exit.png',0.025,0.014)
        return False,None
    pyautogui.click(x,y)
    os.remove(image_path)
    return True,next_step

# 随机选择其他时间进行跳转
# 下一步：step_confirm_change_time
def step_change_time(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_confirm_change_time
    image_info = utils.window_screenshot(hwnd)
    imagePath,w,h,left,top = image_info
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
            x,y = utils.matchTemplate(image_info,filename,x_ratio,y_ratio)
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
    pyautogui.click(nextTime[0]+left,nextTime[1]+top)
    os.remove(imagePath)
    return True,next_step

# 确认跳转时间
# 下一步：step_to_full_card_draw
def step_confirm_change_time(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_to_full_card_draw
    imagePath,w,h,_,_ = utils.window_screenshot(hwnd)
    #识别图片内容
    ocr_result = config.READER.readtext(imagePath)
    os.remove(imagePath)
    for i in ocr_result:
        if "切换至" in i[1]:
            x,y = utils.cal_center(hwnd,i[0])            
            pyautogui.click(x, y)
            break
    log.logger.info("时间切换完成！")
    return True,next_step

# 跳转全英雄界面
# 期望当前界面：任何界面
# 目标页面:全英雄界面
# 下一步：step_full_card_draw
def step_to_full_card_draw(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_full_card_draw
    target_page_types = [ce.PageType.FULL_CARD_DRAW]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_FULL_CARD_DRAW_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入全英雄抽卡面失败,未找到按钮")
        return False,None
    return False,None

# 全英雄第一抽
# 期望当前界面：任何界面
# 目标页面:再抽一次界面
# step_check_result_card_color
def step_full_card_draw(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_check_result_card_color
    target_page_types = [ce.PageType.DRAW_AGAIN_ONCE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type == ce.PageType.EDIT_PAGE:
        is_success = utils.swap_back_wish_list(hwnd,global_vars)
        if not is_success:
            # 如果跳转心愿单失败，重新开始调整心愿单
            return True,step_check_time
        else:
            current_page_type,ocr = utils.get_current_page_type(hwnd)
            
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_FULL_LIST_DRAW_ONECE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("抽卡失败,未找到按钮")
        return False,None
    return False,None

# 目标页面：全英雄界面
# 检查全英雄第一抽颜色
# 如果为绿色，重新开始，返回True,step_check_time
# 如果为蓝，紫，金，开始第二抽，返回True,step_second_full_card_draw
# 如果颜色未知：返回False,None
def step_check_result_card_color(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_second_full_card_draw
    target_page_types = [ce.PageType.FULL_CARD_DRAW]
    card_color = utils.get_card_color(hwnd)
    log.logger.info("普池第一抽颜色:%s",card_color.name)
    global_vars["white_tickets"] -= 1
    global_vars["draw_count"] += 1
    global_vars["full_draw_count"] += 1
    if card_color == ce.CardColor.GREEN:
        log.logger.info("普池第一抽绿色,重新开始")
        #普池绿卡，重新开始
        global_vars["count_white_streak"] += 1
        next_step = step_check_time
    elif card_color in [ce.CardColor.BLUE,ce.CardColor.PURPLE,ce.CardColor.GOLD]:
        global_vars["all_color_count_map"][card_color] += 1
        global_vars["full_color_count_map"][card_color] += 1
        global_vars["count_white_streak"] = 0
        next_step = step_second_full_card_draw
    else:
        return False,None
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    button_names = route.get_route_button_names(route.TO_FULL_CARD_DRAW_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("返回全英雄界面失败,未找到按钮")
        return False,None
    time.sleep(0.5)
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    return False,None

# 全英雄第二抽
# 期望当前界面：任何界面
# 目标页面:再抽一次界面
# 下一步： step_check_second_result_card_color 
def step_second_full_card_draw(**kwargs):
    log.logger.info("开始全英雄第二抽")
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_check_second_result_card_color
    target_page_types = [ce.PageType.DRAW_AGAIN_ONCE]
    # 如果出现需要编辑心愿单页面,使用备用心愿单替换
    if current_page_type == ce.PageType.EDIT_PAGE:
        is_success = utils.swap_back_wish_list(hwnd,global_vars)
        if not is_success:
            # 如果跳转心愿单失败，重新开始调整心愿单
            return True,step_check_time
        else:
            current_page_type,ocr = utils.get_current_page_type(hwnd)
            
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_FULL_LIST_DRAW_ONECE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("抽卡失败,未找到按钮")
        return False,None
    return False,None

# 检查全英雄第二抽颜色
# 如果为绿色，重新开始，返回True,step_check_time
# 如果为蓝，紫，金，跳转史诗界面，返回True,step_to_epic_card_draw
# 如果颜色未知：返回False,None
def step_check_second_result_card_color(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    card_color = utils.get_card_color(hwnd)
    log.logger.info("普池第二抽颜色:%s",card_color.name)
    global_vars["white_tickets"] -= 1
    global_vars["draw_count"] += 1
    global_vars["full_draw_count"] += 1
    if card_color == ce.CardColor.GREEN:
        log.logger.info("普池第二抽绿色,重新开始")
        #普池绿卡，重新开始
        global_vars["count_white_streak"] += 1
        return True,step_check_time
    elif card_color in [ce.CardColor.BLUE,ce.CardColor.PURPLE,ce.CardColor.GOLD]:
        log.logger.info("进入史诗页面")
        global_vars["all_color_count_map"][card_color] += 1
        global_vars["full_color_count_map"][card_color] += 1
        global_vars["count_white_streak"] = 0
        return True,step_to_epic_card_draw
    else:
        return False,None

# 跳转史诗界面
# 期望当前界面：任何界面
# 目标页面:史诗界面
# 下一步：step_epic_card_draw
def step_to_epic_card_draw(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_epic_card_draw
    target_page_types = [ce.PageType.EPIC_CARD_DRAW]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_EPIC_DRAW_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入史诗抽卡面失败,未找到按钮")
        return False,None
    return False,None

# 史诗第一抽
# 期望当前界面：任何界面
# 目标页面:再抽一次界面
# 下一步：step_check_epic_result_card_color
def step_epic_card_draw(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_check_epic_result_card_color
    target_page_types = [ce.PageType.DRAW_AGAIN_ONCE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    # 如果出现需要编辑心愿单页面,使用备用心愿单替换
    if current_page_type == ce.PageType.EDIT_PAGE:
        is_success = utils.swap_back_wish_list(hwnd,global_vars)
        if not is_success:
            # 如果跳转心愿单失败，重新开始调整心愿单
            return True,step_check_time
        else:
            current_page_type,ocr = utils.get_current_page_type(hwnd)
            
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_EPIC_DRAW_ONCE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("抽卡失败,未找到按钮")
        return False,None
    return False,None

# 检查史诗第一抽颜色
# 蓝，紫，继续史诗第二抽，返回True,step_second_epic_card_draw
# 绿，重新开始，返回True,step_check_time
# 史诗蒸馏模式：
#   金，重新开始，返回True,step_check_time
# 神魔蒸馏模式：
#   金，直接进入神魔界面：返回True,step_to_star_origin
# 未知颜色：返回False,None
def step_check_epic_result_card_color(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    target_page_types = [ce.PageType.EPIC_CARD_DRAW]
    next_step = step_second_epic_card_draw
    card_color = utils.get_card_color(hwnd)
    log.logger.info("史诗第一抽颜色:%s",card_color.name)
    global_vars["red_tickets"] -= 1
    global_vars["draw_count"] += 1
    global_vars["epic_draw_count"] += 1
    
    global_vars["all_color_count_map"][card_color] += 1
    global_vars["epic_color_count_map"][card_color] += 1
    if card_color == ce.CardColor.GREEN:
        log.logger.info("史诗第一抽绿色,重新开始")
        #普池绿卡，重新开始
        next_step = step_check_time
    if card_color in [ce.CardColor.BLUE,ce.CardColor.PURPLE]:
        next_step = step_second_epic_card_draw
    if card_color in [ce.CardColor.GOLD]:
        is_star_origin = global_vars["is_star_origin"]
        if is_star_origin:
            next_step = step_to_star_origin
        else:
            next_step = step_check_time

    current_page_type,ocr = utils.get_current_page_type(hwnd)
    button_names = route.get_route_button_names(route.TO_EPIC_DRAW_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("返回全英雄界面,未找到按钮")
        return False,None
    
    time.sleep(0.5)
    current_page_type,_ = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    return False,None

# 史诗第二抽
# 期望当前界面：任何界面
# 目标页面:再抽一次界面
# 下一步：step_check_second_epic_result_card_color
def step_second_epic_card_draw(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_check_second_epic_result_card_color
    target_page_types = [ce.PageType.DRAW_AGAIN_ONCE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    
    # 如果出现需要编辑心愿单页面,使用备用心愿单替换
    if current_page_type == ce.PageType.EDIT_PAGE:
        is_success = utils.swap_back_wish_list(hwnd,global_vars)
        if not is_success:
            # 如果跳转心愿单失败，重新开始调整心愿单
            return True,step_check_time
        else:
            current_page_type,ocr = utils.get_current_page_type(hwnd)
            
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names(route.TO_EPIC_DRAW_ONCE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("抽卡失败,未找到按钮")
        return False,None
    return False,None

# 检查史诗第二抽颜色
# 绿，重新开始，返回True,step_check_time
# 史诗蒸馏模式：
#   金，重新开始，返回True,step_check_time
#   蓝，紫，继续史诗抽卡：返回True,step_second_epic_card_draw
# 神魔蒸馏模式：
#   蓝，紫，金，进入神魔界面：返回True,step_to_star_origin
# 未知颜色：返回False,None
def step_check_second_epic_result_card_color(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    card_color = utils.get_card_color(hwnd)
    log.logger.info("史诗第二抽颜色:%s",card_color.name)
    global_vars["red_tickets"] -= 1
    global_vars["draw_count"] += 1
    global_vars["epic_draw_count"] += 1
    global_vars["all_color_count_map"][card_color] += 1
    global_vars["epic_color_count_map"][card_color] += 1
    if card_color == ce.CardColor.GREEN:
        log.logger.info("史诗第二抽绿色,重新开始")
        #普池绿卡，重新开始
        return True,step_check_time
    is_star_origin = global_vars["is_star_origin"]
    if is_star_origin:
        if card_color in [ce.CardColor.BLUE,ce.CardColor.PURPLE,ce.CardColor.GOLD]:
            return True,step_to_star_origin
    else:
        if card_color == ce.CardColor.GOLD:
            log.logger.info("史诗第二抽金色,重新开始")
            #普池绿卡，重新开始
            return True,step_check_time
        elif card_color in [ce.CardColor.BLUE,ce.CardColor.PURPLE]:
            return True,step_second_epic_card_draw
    return False,None

# 进入神魔界面
# 期望当前界面：任何界面
# 目标页面:神魔界面
# 下一步：step_star_origin_draw
def step_to_star_origin(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_star_origin_draw
    target_page_types = [ce.PageType.STAR_ORIGIN_DRAW]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    # 在up,全英雄，史诗开始，需要滑动底部列表找到神魔界面按钮
    if current_page_type in [ce.PageType.UP_DRAW,ce.PageType.EPIC_CARD_DRAW,ce.PageType.EPIC_CARD_DRAW]:
        slide_for_star(hwnd)
        # 重新读取屏幕内容
        current_page_type,ocr = utils.get_current_page_type(hwnd)
    button_names = route.get_route_button_names(route.TO_STAR_ORIGIN,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入神魔抽卡面失败,未找到按钮")
        return False,None
    return False,None

# 神魔抽卡界面
# 期望当前界面：任何界面
# 目标界面：再抽十次界面
# 下一步:step_check_time
def step_star_origin_draw(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_check_time
    target_page_types = [ce.PageType.DRAW_TENTH_AGAIN]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        # 保存十连结果
        utils.save_window_screenshot(hwnd)
        return True,next_step
    button_names = route.get_route_button_names(route.TO_ORIGIN_STAR_TEHTH,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("神魔十连抽卡失败,未找到按钮")
        return False,None
    return False,None

def stop_work():
    draw_count = global_vars["draw_count"]
    full_draw_count = global_vars["full_draw_count"]
    epic_draw_count = global_vars["epic_draw_count"]
    all_color_count_map = global_vars["all_color_count_map"]
    full_color_count_map = global_vars["full_color_count_map"]
    epic_color_count_map = global_vars["epic_color_count_map"]
    if draw_count > 0 and full_draw_count > 0 and epic_draw_count > 0:
        log.logger.info(f"抽卡统计:")
        log.logger.info(f"总金卡概率:{all_color_count_map[ce.CardColor.GOLD]}/{draw_count}={(all_color_count_map[ce.CardColor.GOLD]/draw_count):.2f}")
        log.logger.info(f"总紫卡概率:{all_color_count_map[ce.CardColor.PURPLE]}/{draw_count}={(all_color_count_map[ce.CardColor.PURPLE]/draw_count):.2f}")
        
        log.logger.info(f"全英雄卡池金卡概率:{full_color_count_map[ce.CardColor.GOLD]}/{full_draw_count}={(full_color_count_map[ce.CardColor.GOLD]/full_draw_count):.2f}")
        log.logger.info(f"全英雄卡池紫卡概率:{full_color_count_map[ce.CardColor.PURPLE]}/{full_draw_count}={(full_color_count_map[ce.CardColor.PURPLE]/full_draw_count):.2f}")
        
        log.logger.info(f"史诗卡池金卡概率:{epic_color_count_map[ce.CardColor.GOLD]}/{epic_draw_count}={(epic_color_count_map[ce.CardColor.GOLD]/epic_draw_count):.2f}")
        log.logger.info(f"史诗卡池紫卡概率:{epic_color_count_map[ce.CardColor.PURPLE]}/{epic_draw_count}={(epic_color_count_map[ce.CardColor.PURPLE]/epic_draw_count):.2f}")
    
def slide_for_star(hwnd):
    #截图
    imagePath,w,h,left,top = utils.window_screenshot(hwnd)
    os.remove(imagePath)
    mX = int(w / 2)
    mY = h - 10
    pyautogui.moveTo(mX+left, mY+top, duration=0.1)
    pyautogui.dragTo(mX+left - 200,mY+top, button='left',duration=0.3)
    time.sleep(0.5)
    

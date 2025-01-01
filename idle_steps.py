import utils
import cus_enum as ce
import route
import log
import time
success_count = 0
failed_count = 0
talent_fight = True
# 初始作业序号
init_plagiarize_number = 2
# 当前作业序号
current_plagiarize_number = init_plagiarize_number
# 当前挑战第几局
game_number = 1
# 是否需要切换作业
is_need_switch_plagiarize = True
# 是否需要切到第二局
# 切换作业后，当前局数为第二局时，需要切换
is_need_switch_to_game = False
# 是否需要切换挑战类型
is_need_change_fight_type = False

def step_begin(tf=True):
    # 默认天赋挂机模式
    global talent_fight
    talent_fight = tf
    return step_log_info
# 打印当前执行进度
# 如果第七个作业失败三次，则尝试切换到[赛季天赋挑战]或[赛季挑战]
# 如果当前作业失败7次，则使用下一个作业
def step_log_info(**kwargs): 
    global is_need_switch_plagiarize
    global current_plagiarize_number
    global failed_count
    global talent_fight
    global is_need_change_fight_type
    next_step = step_to_main
    
    log.logger.info(f"已成功通过{success_count}关")
    log.logger.info(f"当前使用第{current_plagiarize_number+1}个通关作业,当前尝试次数:{failed_count}")
    if current_plagiarize_number >= 6 and failed_count > 3:
        log.logger.info("失败次数太多，尝试切换挑战类型")
        talent_fight = not talent_fight
        is_need_change_fight_type = True
        failed_count = 0
        current_plagiarize_number = init_plagiarize_number
    if failed_count >= 7:
        failed_count = 0
        current_plagiarize_number += 1
        is_need_switch_plagiarize = True
    return True,next_step

# 进入主页面
# 期望当前页面：任何页面
# 目标页面：主页面
# 如果当前页面已经是准备战斗页面,或挂机页面，则直接返回True
# 如果需要切换挑战类型，必须先退出战斗界面回到主界面
def step_to_main(**kwargs):
    global is_need_change_fight_type
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_to_idle
    if is_need_change_fight_type:
        target_page_types = [ce.PageType.MAIN_PAGE]
        is_need_change_fight_type = False
    else:
        target_page_types = [ce.PageType.MAIN_PAGE,ce.PageType.IDLE_PAGE,ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    
    button_names = route.get_route_button_names(route.TO_MAIN_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入主页面失败,未找到按钮")
        return False,next_step
    return False,next_step
# 进入挂机页面
# 期望当前页面：主页面
# 目标页面：挂机页面
# 如果当前页面已经是准备战斗页面,或挂机页面，则直接返回True
def step_to_idle(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_to_fight_ready
    target_page_types = [ce.PageType.IDLE_PAGE,ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names([[ce.PageType.MAIN_PAGE,['当前进度','当前迸度']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入挂机页面失败,未找到按钮")
        return False,next_step
    return False,next_step
# 进入战斗准备页面
# 期望当前页面：挂机页面
# 目标页面：战斗准备页面
# 根据[talent_fight]判断进入[赛季天赋挑战]或[赛季挑战]
def step_to_fight_ready(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_to_plagiarize
    target_page_types = [ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    
    to_fight_route = []
    if talent_fight :
        to_fight_route = [[ce.PageType.IDLE_PAGE,['天赋挑战']]]
    else:
        to_fight_route = [[ce.PageType.IDLE_PAGE,['挑战']]]
    button_names = route.get_route_button_names(to_fight_route,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入准备战斗页面失败,未找到按钮")
        return False,next_step
    return False,next_step
# 进入抄作业页面
# 期望当前页面：战斗准备页面
# 目标页面：抄作业页面
# 根据[is_need_switch_plagiarize]判断是否需要抄作业
def step_to_plagiarize(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_choose_plagiarize
    if is_need_switch_plagiarize:
        target_page_types = [ce.PageType.PLAGIARIZE_PAGE]
    else:
        target_page_types = [ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names([[ce.PageType.READY_FIGHT_PAGE,['通关记录']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入抄作业战斗页面失败,未找到按钮")
        return False,next_step
    return False,next_step
# 选择作业
# 期望当前页面：抄作业页面
# 目标页面：无
# 根据[is_need_switch_plagiarize]判断是否需要选择作业
# 根据[current_plagiarize_number]选择作业
def step_choose_plagiarize(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_use_plagiarize
    if is_need_switch_plagiarize:
        current_page_type,ocr = utils.get_current_page_type(hwnd)
        if current_page_type != ce.PageType.PLAGIARIZE_PAGE:
            log.logger.info("选择作业失败,不在抄作业界面")
            return False,next_step
        for i in range(current_plagiarize_number):
            utils.clickIntoByButtonName(hwnd,['next.png'],ocr)
            time.sleep(0.5)
    return True,next_step

# 采用作业
# 期望当前页面：作业选择页面,准备战斗
# 目标页面：准备战斗
# 根据[is_need_switch_plagiarize]判断是否需要选择作业
# 选择作业后，设置[is_need_switch_plagiarize]为False
def step_use_plagiarize(**kwargs):
    global is_need_switch_plagiarize
    global is_need_switch_to_game
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_to_game2
    if is_need_switch_plagiarize:
        target_page_types = [ce.PageType.READY_FIGHT_PAGE]
        current_page_type,ocr = utils.get_current_page_type(hwnd)
        if current_page_type in target_page_types:
            return True,next_step
        button_names = route.get_route_button_names([[ce.PageType.PLAGIARIZE_PAGE,['一键采用']],[ce.PageType.NO_HERO_PAGE,['确定']]],current_page_type)
        if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
            log.logger.info("进入准备战斗页面失败,未找到按钮")
            return False,next_step
        is_need_switch_plagiarize = False
        if game_number == 2:
            is_need_switch_to_game = True
    return True,next_step

# 跳转第二局
# 条件：根据[is_need_switch_to_game]
# 切换成功后，[is_need_switch_to_game] = False
def step_to_game2(**kwargs):
    global is_need_switch_to_game
    next_step = step_start_fight
    if is_need_switch_to_game:
        hwnd = utils.get_hwnd_from_kwargs(kwargs)
        if not utils.clickIntoByButtonName(hwnd,['game2.png'],[]):
            log.logger.info("进入第二局战斗页面失败,未找到按钮")
            return False,next_step
        is_need_switch_to_game = False
    return True,next_step

# 开始战斗
# 预期当前页面：准备战斗页面,确认人数不足页面,确认天赋格未占页面
# 目标页面：战斗中页面
def step_start_fight(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_waiting_fight_result
    target_page_types = [ce.PageType.FIGHTING_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True,next_step
    button_names = route.get_route_button_names([[ce.PageType.READY_FIGHT_PAGE,['战斗']],[ce.PageType.NO_HERO_PAGE,['确定']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入战斗中页面失败,未找到按钮")
        return False,next_step
    return False,next_step
# 等待战斗结束
# 预期当前页面：战斗中
# 目标页面:战斗失败，战斗胜利1，战斗胜利2
# 如果等待超过100s或者出现其他页面，返回False
# 这里不想引入暂停和停止功能，只有在完成这一步时才能暂停或停止
def step_waiting_fight_result(**kwargs):
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_handle_fight_result
    target_page_types = [ce.PageType.FIGHT_FAIL_PAGE,ce.PageType.FIGHT_SUCCESS_1_PAGE,ce.PageType.FIGHT_SUCCESS_2_PAGE]
    # 等待时间
    count = 0
    while True:
        # 超过100秒退出循环
        if count > 100:
            break
        current_page_type,_ = utils.get_current_page_type(hwnd)
        if current_page_type == ce.PageType.FIGHTING_PAGE:
            time.sleep(2)
            count += 2
            continue
        if current_page_type in target_page_types:
            return True,next_step
        else:
            # 出现其他页面，直接退出
            break
    return False,next_step

# 处理战斗结果
# 预期当前页面：战斗失败，战斗成功1，战斗成功2
# 目标页面:战斗准备
# 如果第一局成功(成功页面1)继续战斗,game_nubmer = 2
# 如果失败页面，继续挑战，失败次数+1
# 如果第二局成功(成功页面2)继续战斗，作业序号重置为默认值，失败次数清零，成功数+1
def step_handle_fight_result(**kwargs):
    global success_count
    global failed_count
    global current_plagiarize_number
    global game_number
    global is_need_switch_plagiarize
    
    hwnd = utils.get_hwnd_from_kwargs(kwargs)
    next_step = step_log_info
    target_page_types = [ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
            return True,next_step
    if current_page_type == ce.PageType.FIGHT_FAIL_PAGE:
        log.logger.info("战斗失败,失败次数+1")
        failed_count += 1
        button_names = route.get_route_button_names([[ce.PageType.FIGHT_FAIL_PAGE,['继续挑战']]],current_page_type)
        if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
            log.logger.info("进入战斗准备页面失败,未找到按钮")
            return False,next_step
    elif current_page_type == ce.PageType.FIGHT_SUCCESS_1_PAGE:
        log.logger.info("第一局战斗成功！")
        game_number = 2
        button_names = route.get_route_button_names([[ce.PageType.FIGHT_SUCCESS_1_PAGE,['继续挑战']]],current_page_type)
        if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
            log.logger.info("进入战斗准备页面失败,未找到按钮")
            return False,next_step
    elif current_page_type == ce.PageType.FIGHT_SUCCESS_2_PAGE:
        log.logger.info("第二局战斗成功！")
        failed_count = 0
        current_plagiarize_number = init_plagiarize_number
        success_count += 1
        game_number = 1
        is_need_switch_plagiarize = True
        button_names = route.get_route_button_names([[ce.PageType.FIGHT_SUCCESS_2_PAGE,['天赋挑战','挑战']]],current_page_type)
        if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
            log.logger.info("进入战斗准备页面失败,未找到按钮")
            return False,next_step
    return False,next_step

# 停止重置所有信息
def stop_work():
    log.logger.info("执行结束！")
    global is_need_switch_plagiarize 
    global current_plagiarize_number
    global failed_count
    global is_need_switch_to_game
    global game_number
    global is_need_change_fight_type
    is_need_switch_plagiarize = True
    current_plagiarize_number = init_plagiarize_number
    failed_count = 0
    is_need_switch_to_game = False
    game_number = 1
    is_need_change_fight_type = False    
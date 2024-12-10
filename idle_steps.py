import utils
import cus_enum as ce
import route
import log
import time
success_count = 0
failed_count = 0
talent_fight = True
# 当前作业序号
current_plagiarize_number = 2
# 当前挑战第几局
game_number = 1
# 是否需要切换作业
is_need_switch_plagiarize = True

# 打印当前执行进度
# 如果第七个作业失败三次，则尝试切换到[赛季天赋挑战]或[赛季挑战]
# 如果当前作业失败7次，则使用下一个作业
def step_log_info(**kwargs): 
    global is_need_switch_plagiarize
    global current_plagiarize_number
    log.logger.info(f"已成功通过{success_count}关")
    log.logger.info(f"当前使用第{current_plagiarize_number+1}个通关作业,当前尝试次数:{failed_count}")
    if current_plagiarize_number >= 6 and failed_count > 3:
        log.logger.info("失败次数太多，尝试切换挑战类型")
        talent_fight = not talent_fight
    if failed_count >= 7:
        failed_count = 0
        current_plagiarize_number += 1
        is_need_switch_plagiarize = False

# 进入主页面
# 期望当前页面：任何页面
# 目标页面：主页面
# 如果当前页面已经是准备战斗页面,或挂机页面，则直接返回True
def step_to_main(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    target_page_types = [ce.PageType.MAIN_PAGE,ce.PageType.IDLE_PAGE,ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    
    button_names = route.get_route_button_names(route.TO_MAIN_PAGE,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入主页面失败,未找到按钮")
        return False
    
def step_2(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    target_page_types = [ce.PageType.IDLE_PAGE,ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    button_names = route.get_route_button_names([[ce.PageType.MAIN_PAGE,['当前进度','当前迸度']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入挂机页面失败,未找到按钮")
        return False
    
def step_3(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    target_page_types = [ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    if talent_fight :
        to_fight_route = [[ce.PageType.IDLE_PAGE,['天赋挑战']]]
    else:
        to_fight_route = [[ce.PageType.IDLE_PAGE,['挑战']]]
    button_names = route.get_route_button_names(to_fight_route,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入准备战斗页面失败,未找到按钮")
        return False
    
def step_4(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    if is_need_switch_plagiarize:
        target_page_types = [ce.PageType.PLAGIARIZE_PAGE]
    else:
        target_page_types = [ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    button_names = route.get_route_button_names([[ce.PageType.READY_FIGHT_PAGE,['通关记录']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入抄作业战斗页面失败,未找到按钮")
        return False
    
def step_5(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    if is_need_switch_plagiarize:
        current_page_type,ocr = utils.get_current_page_type(hwnd)
        if current_page_type != ce.PageType.PLAGIARIZE_PAGE:
            log.logger.info("选择作业失败,不在抄作业界面")
            return False
        for i in range(current_plagiarize_number):
            utils.clickIntoByButtonName(hwnd,['next.png'],ocr)
            time.sleep(0.3)
    return True

# 采用作业
# 期望当前页面：作业选择页面,准备战斗
# 目标页面：准备战斗
# 如果当前页面已经是准备战斗页面，则表示不需要选择作业，直接返回True
def step_use_plagiarize(**kwargs):
    global is_need_switch_plagiarize
    hwnd = get_hwnd_from_kwargs(kwargs)
    target_page_types = [ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    button_names = route.get_route_button_names([[ce.PageType.PLAGIARIZE_PAGE,['一键采用']],[ce.PageType.NO_HERO_PAGE,['确定']],[ce.PageType.CONFIMR_PAGE,['confirm.png']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入准备战斗页面失败,未找到按钮")
        return False
    is_need_switch_plagiarize = False
    return True

# 跳转第二局
# 条件：如果当前局数是第二局
def step_to_game2(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    # 如果当前挑战第二局，则跳转到第二局界面
    if game_number == 2:
        if not utils.clickIntoByButtonName(hwnd,['game2.png'],[]):
            log.logger.info("进入第二局战斗页面失败,未找到按钮")
            return False
    return True

# 开始战斗
# 预期当前页面：准备战斗页面,确认人数不足页面,确认天赋格未占页面
# 目标页面：战斗中页面
def start_fight(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
    target_page_types = [ce.PageType.FIGHTING_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    button_names = route.get_route_button_names([[ce.PageType.PLAGIARIZE_PAGE,['战斗']],[ce.PageType.NO_HERO_PAGE,['确定']],[ce.PageType.CONFIMR_PAGE,['confirm.png']]],current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        log.logger.info("进入战斗中页面失败,未找到按钮")
        return False
    return True

# 等待战斗结束
# 预期当前页面：战斗中
# 目标页面:战斗失败，战斗胜利1，战斗胜利2
# 如果等待超过100s或者出现其他页面，返回False
# 这里不想引入暂停和停止功能，只有在完成这一步时才能暂停或停止
def waiting_fight_result(**kwargs):
    hwnd = get_hwnd_from_kwargs(kwargs)
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
            return True
        else:
            # 出现其他页面，直接退出
            break
    return False
def idle_mode_steps():
    steps = []
    # 挑战信息日志打印
    steps.append(step_log_info)
    # 进入主界面
    # 如果已经在挂机界面或者战斗界面直接返回（避免每次循环都需要回到主页面）
    steps.append(step_to_main)
    steps.append(step_2)
    steps.append(step_3)
    steps.append(step_4)
    steps.append(step_5)
    steps.append(step_use_plagiarize)
    steps.append(step_to_game2)
    steps.append(start_fight)
    steps.append(waiting_fight_result)
    return steps

# 在参数中获取句柄参数
def get_hwnd_from_kwargs(kwargs):
    hwnd = kwargs['hwnd']
    return hwnd
    
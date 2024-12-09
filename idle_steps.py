import utils
import cus_enum as ce
import config

MAIN_PAGE_SETP = [
    [ce.PageType.CATEGORY,['./back2.png']],
    [ce.PageType.HERO_HALL,['./back2.png']],
    [ce.PageType.CLUB,['./back2.png']],
    [ce.PageType.SHEN_MI_WU,['./back2.png']],
    [ce.PageType.UP_DRAW,['./back2.png']],
    [ce.PageType.FULL_CARD_DRAW,['./back2.png']],
    [ce.PageType.EPIC_CARD_DRAW,['./back2.png']],
    [ce.PageType.STAR_ORIGIN_DRAW,['./back2.png']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
    [ce.PageType.IDLE_PAGE,['back.png']],
    [ce.PageType.READY_FIGHT_PAGE,['back.png']],
    [ce.PageType.PLAGIARIZE_PAGE,['点击空白处关闭']],
    [ce.PageType.FIGHT_FAIL_PAGE,['继续挑战']],
    [ce.PageType.FIGHT_SUCCESS_1_PAGE,['继续挑战']],
    [ce.PageType.FIGHT_SUCCESS_2_PAGE,['back.png']], 
]

def get_step_button_names(steps,current_page_type):
    steps.extend(config.COMMON_STEP)
    return steps[current_page_type]

def step_1(hwnd):
    target_page_types = [ce.PageType.MAIN_PAGE,ce.PageType.IDLE_PAGE,ce.PageType.READY_FIGHT_PAGE]
    current_page_type,ocr = utils.get_current_page_type(hwnd)
    if current_page_type in target_page_types:
        return True
    
    button_names = get_step_button_names(MAIN_PAGE_SETP,current_page_type)
    if not utils.clickIntoByButtonName(hwnd,button_names,ocr):
        return False

def idle_mode_steps():
    steps = []
    steps.append(step_1)
    return steps
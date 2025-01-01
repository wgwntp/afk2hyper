import cus_enum as ce
import config

TO_MAIN_PAGE = [
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
    [ce.PageType.MAP_PAGE,['back.png']],
]

TO_FULL_CARD_DRAW_PAGE = [
    [ce.PageType.MAIN_PAGE,['神秘屋']],
    [ce.PageType.CATEGORY,['神秘屋']],
    [ce.PageType.HERO_HALL,['神秘屋']],
    [ce.PageType.CLUB,['神秘屋']],
    [ce.PageType.SHEN_MI_WU,['月桂酒馆']],
    [ce.PageType.UP_DRAW,['全英雄招募']],
    [ce.PageType.EPIC_CARD_DRAW,['全英雄招募']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

TO_FULL_LIST_DRAW_ONECE = [
    [ce.PageType.MAIN_PAGE,['神秘屋']],
    [ce.PageType.CATEGORY,['神秘屋']],
    [ce.PageType.HERO_HALL,['神秘屋']],
    [ce.PageType.CLUB,['神秘屋']],
    [ce.PageType.SHEN_MI_WU,['月桂酒馆']],
    [ce.PageType.UP_DRAW,['全英雄招募']],
    [ce.PageType.EPIC_CARD_DRAW,['全英雄招募']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
    [ce.PageType.FULL_CARD_DRAW,['招募一次','招募-次']]
]

TO_EPIC_DRAW_PAGE = [
    [ce.PageType.MAIN_PAGE,['神秘屋']],
    [ce.PageType.CATEGORY,['神秘屋']],
    [ce.PageType.HERO_HALL,['神秘屋']],
    [ce.PageType.CLUB,['神秘屋']],
    [ce.PageType.SHEN_MI_WU,['月桂酒馆']],
    [ce.PageType.UP_DRAW,['史诗招募']],
    [ce.PageType.FULL_CARD_DRAW,['史诗招募']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

TO_EPIC_DRAW_ONCE = [
    [ce.PageType.MAIN_PAGE,['神秘屋']],
    [ce.PageType.CATEGORY,['神秘屋']],
    [ce.PageType.HERO_HALL,['神秘屋']],
    [ce.PageType.CLUB,['神秘屋']],
    [ce.PageType.SHEN_MI_WU,['月桂酒馆']],
    [ce.PageType.UP_DRAW,['史诗招募']],
    [ce.PageType.FULL_CARD_DRAW,['史诗招募']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
    [ce.PageType.EPIC_CARD_DRAW,['招募一次','招募-次']]
]

TO_STAR_ORIGIN = [
    [ce.PageType.MAIN_PAGE,['神秘屋']],
    [ce.PageType.CATEGORY,['神秘屋']],
    [ce.PageType.HERO_HALL,['神秘屋']],
    [ce.PageType.CLUB,['神秘屋']],
    [ce.PageType.SHEN_MI_WU,['月桂酒馆']],
    [ce.PageType.UP_DRAW,['星源占卜']],
    [ce.PageType.FULL_CARD_DRAW,['星源占卜']],
    [ce.PageType.EPIC_CARD_DRAW,['星源占卜']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

TO_ORIGIN_STAR_TEHTH = [ 
    [ce.PageType.MAIN_PAGE,['神秘屋']],
    [ce.PageType.CATEGORY,['神秘屋']],
    [ce.PageType.HERO_HALL,['神秘屋']],
    [ce.PageType.CLUB,['神秘屋']],
    [ce.PageType.SHEN_MI_WU,['月桂酒馆']],
    [ce.PageType.UP_DRAW,['星源占卜']],
    [ce.PageType.FULL_CARD_DRAW,['星源占卜']],
    [ce.PageType.EPIC_CARD_DRAW,['星源占卜']],
    [ce.PageType.STAR_ORIGIN_DRAW,['占卜十次']],
    [ce.PageType.READY_TO_DRAW_ORIGIN_PAGE,['长按或点击进行占星']],
    [ce.PageType.DRAW_AGAIN_ONCE,['back.png']],
    [ce.PageType.DRAW_AGAIN_TENTH,['back.png']],
]

def get_route_button_names(routes,current_page_type):
    button_names = []
    routes.extend(config.COMMON_ROUTE)
    for r in routes:
        if current_page_type == r[0]:
            button_names = r[1]
            break
    return button_names

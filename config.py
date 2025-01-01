import cus_enum
import easyocr

UI_TYPE_LIST = [
    (cus_enum.PageType.START_PAGE,['点击开始游戏']),
    (cus_enum.PageType.PAUSE_PAGE,['点击屏幕恢复']),
    (cus_enum.PageType.SHEN_MI_WU,['月桂酒馆']),
    (cus_enum.PageType.UP_DRAW,['英雄头饰']),
    (cus_enum.PageType.FULL_CARD_DRAW,['心愿单']),
    (cus_enum.PageType.EPIC_CARD_DRAW,['自选英雄']),
    (cus_enum.PageType.STAR_ORIGIN_DRAW,['占卜十次']),
    (cus_enum.PageType.CATEGORY,['挂机关卡','迷梦之域','竞技场']),
    (cus_enum.PageType.HERO_HALL,['共鸣骑士','共鸣之手']),
    (cus_enum.PageType.CLUB,['公会挑战']),
    (cus_enum.PageType.MAIN_PAGE,['神秘屋','玩法目录','英雄厅堂','公会']),
    (cus_enum.PageType.SECOND_PAGE,['月桂之旅','社区']),
    (cus_enum.PageType.DRAW_AGAIN_ONCE,['再招募一次']),
    (cus_enum.PageType.DRAW_AGAIN_TENTH,['再招募十次']),
    (cus_enum.PageType.MAP_PAGE,['启程篇章']),
    (cus_enum.PageType.GIFT_PAGE,['点击屏幕退出']),
    (cus_enum.PageType.PACK_PAGE,['全部']),
    (cus_enum.PageType.EDIT_PAGE,['编辑英雄']),
    (cus_enum.PageType.READY_TO_DRAW_ORIGIN_PAGE,['长按或者点击进行占星']),
    (cus_enum.PageType.DRAW_TENTH_AGAIN,['再招募十次']),
    (cus_enum.PageType.IDLE_PAGE,['天赋挑战','挑战']),
    (cus_enum.PageType.READY_FIGHT_PAGE,['战斗','自动挑战']),
    (cus_enum.PageType.PLAGIARIZE_PAGE,['一键采用']),
    (cus_enum.PageType.FIGHT_FAIL_PAGE,['失败','继续挑战']),
    (cus_enum.PageType.FIGHT_SUCCESS_1_PAGE,['胜利','继续挑战']),
    (cus_enum.PageType.FIGHT_SUCCESS_2_PAGE,['挂机收益提升']),
    (cus_enum.PageType.FIGHTING_PAGE,['fight_icon_2.png']),
    (cus_enum.PageType.OMIT_PAGE,['跳过']),
    (cus_enum.PageType.CLICK_GO_PAGE,['点击屏幕继续']),
    (cus_enum.PageType.NO_HERO_PAGE,['未拥有']),
    (cus_enum.PageType.CONFIMR_PAGE,['confirm_page_type.png']), 
    (cus_enum.PageType.OTHER_PAGE,['点击空白处关闭']),
    (cus_enum.PageType.OTHER_PAGE,['点击空自处关闭']),   
]

READER = easyocr.Reader(['ch_sim','en'])
CARDS_PATH = './images/cards'
IMAGES_PATH = './images/'
GOLD_CARD_PATH = './images/cards/gold/'

COMMON_ROUTE = [
    [cus_enum.PageType.START_PAGE,['点击开始游戏']],
    [cus_enum.PageType.PAUSE_PAGE,['点击屏幕恢复']],
    [cus_enum.PageType.OTHER_PAGE,['点击空白处关闭','点击空自处关闭']],
    [cus_enum.PageType.GIFT_PAGE,['点击屏幕退出']],
    [cus_enum.PageType.OMIT_PAGE,['跳过']],
    [cus_enum.PageType.CLICK_GO_PAGE,['点击屏幕继续']],
    [cus_enum.PageType.NO_HERO_PAGE,['确认','确定']],
    [cus_enum.PageType.CONFIMR_PAGE,['confirm.png']]
]
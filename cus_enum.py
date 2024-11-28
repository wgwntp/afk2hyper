from enum import Enum

class DrawMode(Enum):
    TURBO_DRAW_EPIC = '全联动模式-史诗'
    TURBO_DRAW_GD = '全联动模式-神魔'
    DIRECT_DRAW_FULL = '全英雄招募-定向金'
    DIRECT_DRAW_EPIC = '史诗招募-定向金'
    IDLE_MODE = '自动挂机模式'
    
    # FULL_LIST_DRAW = '全英雄招募'
    # EPIC_CARD_DRAW = '史诗招募'
    # STAR_ORIGIN_DRAW = '星源占卜'
    
    
class PageType(Enum):  
    START_PAGE = '开始界面'
    PAUSE_PAGE = '挂起界面' 
    SHEN_MI_WU = '神秘屋'
    UP_DRAW = 'UP招募'
    FULL_CARD_DRAW = '全英雄招募'
    EPIC_CARD_DRAW = '史诗招募'
    STAR_ORIGIN_DRAW = '星源占卜'
    CATEGORY = '玩法目录'
    HERO_HALL = '英雄厅堂'
    CLUB = '公会'
    MAIN_PAGE = '主界面'
    SECOND_PAGE = '次级界面'
    OTHER_PAGE = '其他页面'
    DRAW_AGAIN_ONCE = '再招募一次'
    DRAW_AGAIN_TENTH = '再招募十次'
    MAP_PAGE = '地图界面'
    GIFT_PAGE ='点击屏幕退出'
    PACK_PAGE = '背包界面'
    EDIT_PAGE = '心愿单提示编辑页面'
    OMIT_PAGE = '跳过页面'
    CLICK_GO_PAGE = '点击跳过页面'
    UNKNOWN_PAGE = '未知页面'
    READY_TO_DRAW_ORIGIN_PAGE = '长按点击抽取神魔页面'
    DRAW_TENTH_AGAIN = '再招募十次页面'
    IDLE_PAGE = '挂机页面'
    READY_FIGHT_PAGE = '准备战斗页面'
    PLAGIARIZE_PAGE = '抄作业页面'
    FIGHT_FAIL_PAGE = '战斗失败页面'
    FIGHT_SUCCESS_1_PAGE = '战斗成功页面'
    FIGHT_SUCCESS_2_PAGE = '战斗成功页面2'
    FIGHTING_PAGE = '战斗中页面'
    NO_HERO_PAGE = '存在末拥有的旧日回响或英雄'
    CONFIMR_PAGE = '待确认页面'
    
    

class CardColor(Enum):
    UNKNOWN = 0
    GREEN = 1
    BLUE = 2
    PURPLE = 3
    GOLD = 4

class CardType(Enum):
    PURPLE = 1
    GOLD = 2
    GOD = 3
from datetime import datetime
import cus_enum
import config
import time
import utils
import os
import pyautogui
import log

turbo_paused = False
turbo_stop = False

def hyper(hwnd,steps):
    while True:
        for step in steps:
            # 如果停止，退出循环
            if turbo_stop:
                break
            # 执行步骤
            if not execute_step(hwnd,step):
                log.logger.info("步骤失败，重新开始")
                break
            # 步骤执行成功，继续下一步
            
        # 如果停止，退出循环
        if turbo_stop:
            log.logger.info("停止退出")
            break
        time.sleep(0.5)

# 执行步骤，如果没有成功，则多次尝试，10次未成功重新开始
def execute_step(hwnd,step):
    try_times = 10
    for i in range(try_times):
        # 如果暂停，停在当前步骤
        paused(turbo_paused)
        # 如果停止，退出循环
        if turbo_stop:
            break
        print("try to run step")
        if not step(hwnd):
            time.sleep(1)
            continue    
        else:
            return True
    return False

def paused(turbo_paused):
    while True:
        if turbo_paused:
            time.sleep(0.1)
            continue
        break
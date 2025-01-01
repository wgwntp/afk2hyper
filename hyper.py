import time
import log

paused = False
stop = False

def hyper(hwnd,step,stop_work):
    current_step = step
    while True:
        # 执行步骤
        is_success,next_step = execute_step(hwnd,current_step)
        time.sleep(0.8)
        # 如果停止，退出循环
        if stop:
            stop_work()
            log.logger.info("停止退出")
            break
        
        if not is_success:
            # 如果失败从第一步开始
            current_step = step
            continue
        # 步骤执行成功，继续下一步
        current_step = next_step
        

# 执行步骤，如果没有成功，则多次尝试，10次未成功重新开始
def execute_step(hwnd_value,step):
    try_times = 10
    for i in range(try_times):
        # 如果暂停，停在当前步骤
        is_paused()
        # 如果停止，退出循环
        if stop:
            break
        # 执行当前步骤
        is_success,next_step = step(hwnd=hwnd_value)
        if not is_success:
            time.sleep(1)
            continue    
        else:
            return True,next_step
    return False,None

def is_paused():
    while True:
        if paused:
            time.sleep(0.1)
            continue
        break
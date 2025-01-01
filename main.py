import win32gui    

import os
import threading
import numpy as np
import tkinter as tk
import queue
from tkinter import scrolledtext

from tkinter import messagebox
import event
import cus_enum
import log
import page_test
import hyper
import idle_steps
import distillation_steps
import direct_full_draw_steps
import direct_epic_draw_steps

# 卡片模板路径  
CARDS_PATH = './images/cards'
# 当前选择句柄，默认:0
hwnd = 0
# 当前运行模式，默认:蒸馏史诗
draw_mode = cus_enum.DrawMode.TURBO_DRAW_EPIC
# 创建一个全局的队列对象,用于在线程之间传递消息  
message_queue = queue.Queue()
# 当前剩余白票数量
white_tickets = 0
# 当前剩余红票数量
red_tickets = 0
# 当前剩余神魔球数量
ball_tickets = 0
# 窗口期分钟开始时间,默认:58
limit_begin_m = 58
# 窗口期分钟结束时间,默认:3
limit_end_m = 3
# 窗口期小时开始时间,默认:1
limit_begin_h = 1
# 窗口期小时结束时间,默认:5
limit_end_h = 5

# 检查消息队列
# 参数:无
# 返回值:无
# 用于在主线程中检查队列并更新GUI
def check_queue():  
    try:  
        # 从队列中获取一条消息（如果队列为空，则此调用将阻塞直到有消息可用）  
        message = message_queue.get_nowait()
        # 更新GUI（例如，在Text组件中添加一条日志）  
        log_text.insert(tk.END, message + "\n")  
        log_text.see(tk.END)  # 确保滚动条显示到最后
        root.after(100, check_queue)
    except queue.Empty:  
        # 如果队列为空，则重新安排此函数稍后再次调用
        root.after(100, check_queue)  # 100毫秒后再次检查队列
      
def get_all_windows():  
    # 获取桌面窗口句柄  
    # hwnd_desktop = win32gui.GetDesktopWindow()  
    # 初始化一个空列表来存储窗口句柄  
    windows = []  
 
    # 枚举所有顶级窗口  
    def foreach_window(hwnd, lParam):  
        if win32gui.IsWindowVisible(hwnd): 
            title = win32gui.GetWindowText(hwnd)
            if title != "":
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))  
 
    # 使用 EnumWindows 函数枚举所有顶级窗口  
    win32gui.EnumWindows(foreach_window, 0)  
    return windows  
      
class DrawCardsThread(threading.Thread):  
    def __init__(self, name):  
        super().__init__()  
        self.name = name  
  
    def run(self):
        global draw_mode
        tickets = [white_tickets,red_tickets,ball_tickets]
        limit_times = [limit_begin_h,limit_end_h,limit_begin_m,limit_end_m]
        if draw_mode == cus_enum.DrawMode.TURBO_DRAW_EPIC:
            log.logger.info("开始史诗抽卡模式")
            full_back_up_wish_list=['18-m']
            epic_back_up_wish_list=['3-y']
            hyper.hyper(hwnd,distillation_steps.step_begin(False,limit_times,tickets,full_back_up_wish_list,epic_back_up_wish_list),distillation_steps.stop_work)
        elif draw_mode == cus_enum.DrawMode.TURBO_DRAW_GD:
            full_back_up_wish_list=['18-m']
            epic_back_up_wish_list=['3-y']
            log.logger.info("开始神魔抽卡模式")
            hyper.hyper(hwnd,distillation_steps.step_begin(True,limit_times,tickets,full_back_up_wish_list,epic_back_up_wish_list),distillation_steps.stop_work)
        elif draw_mode == cus_enum.DrawMode.DIRECT_DRAW_FULL:
            log.logger.info("开始全英雄定向金抽卡模式")
            target_full_list=["3-y","4-y","31-l","32-l","44-w","47-w","18-m","17-m"]
            target_epic_list=["32-l","4-y","47-w","18-m","17-m"]
            hyper.hyper(hwnd,direct_full_draw_steps.step_begin(limit_times,tickets,target_full_list,target_epic_list),direct_full_draw_steps.stop_work)
        elif draw_mode == cus_enum.DrawMode.DIRECT_DRAW_EPIC:
            log.logger.info("开史诗定向金抽卡模式")
            # target_full_list=["3-y","4-y","31-l","32-l","44-w","47-w","18-m","17-m"]
            # target_epic_list=["32-l","4-y","47-w","18-m","17-m"]
            target_full_list=["2-y","49-y","16-m","42-w","43-w","15-m","6-l","29-l"]
            target_epic_list=["30-l","16-m","15-m","6-l","29-l"]
            hyper.hyper(hwnd,direct_epic_draw_steps.step_begin(limit_times,tickets,target_full_list,target_epic_list),direct_epic_draw_steps.stop_work)
        elif draw_mode == cus_enum.DrawMode.IDLE_MODE:
            log.logger.info("开始自动天赋挂机模式")
            hyper.hyper(hwnd,idle_steps.step_begin(True),idle_steps.stop_work)
        elif draw_mode == cus_enum.DrawMode.IDLE_MODE_2:
            log.logger.info("开始自动普通挂机模式")
            hyper.hyper(hwnd,idle_steps.step_begin(False),idle_steps.stop_work)

drawCardsThread = DrawCardsThread('Draw Card Thread')           
#界面响应函数 
def on_select(name, index, mode):  
    # 当用户选择一个选项时，这个函数会被调用
    v = window_menu_var.get()
    global hwnd
    hwnd = int(v.split(':')[1]) 
    
def on_mode_select(name, index, mode):
    # 当用户选择一个选项时，这个函数会被调用
    v = mode_menu_var.get()
    global draw_mode
    for e in cus_enum.DrawMode:
        if e.value == v:
            draw_mode = e
   
def on_closing():
        # 这里我们不需要显式中断线程，因为我们将线程设置为守护线程  
        # 当主线程（即tkinter事件循环）结束时，守护线程会自动结束  
        print("Window is closing, exiting program.")
        try:
            for filename in os.listdir('./'):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    os.remove('./'+filename)
        except:
            print('无法删除图片')
        root.destroy()  # 销毁窗口  

def on_start_click(event):        
    if hwnd != 0:
        global white_tickets
        user_input = entry1.get()
        if not user_input.isdigit():
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry1.config(state=tk.DISABLED)
        white_tickets = int(user_input)
        
        global red_tickets
        user_input = entry2.get()
        if not user_input.isdigit():
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry2.config(state=tk.DISABLED)
        red_tickets = int(user_input)
        
        # 使用get()方法读取Entry中的值
        global ball_tickets
        user_input = entry3.get()
        if not user_input.isdigit():
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry3.config(state=tk.DISABLED)
        ball_tickets = int(user_input)
        
        if white_tickets == 0 or red_tickets == 0 or ball_tickets == 0:
            messagebox.showinfo("提示", "数量不足，无法开始！") 
        
        global limit_begin_h
        global limit_end_h
        global limit_begin_m
        global limit_end_m

        begin_h_input = entry1_s.get()
        if (not begin_h_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry1_s.config(state=tk.DISABLED)
        limit_begin_h = int(begin_h_input)
        
        end_h_input = entry2_s.get()
        if (not end_h_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry2_s.config(state=tk.DISABLED)
        limit_end_h = int(end_h_input)
        
        begin_m_input = entry3_s.get()
        if (not begin_m_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry3_s.config(state=tk.DISABLED)
        limit_begin_m = int(begin_m_input)
        
        end_m_input = entry4_s.get()
        if (not end_m_input.isdigit()):
            messagebox.showinfo("提示", "请输入数字！")
            return
        entry4_s.config(state=tk.DISABLED)
        limit_end_m = int(end_m_input)
        

        hyper.stop = False
        drawCardsThread = DrawCardsThread('Draw Card Thread')
        drawCardsThread.daemon = True
        drawCardsThread.start()

        # 禁用start_button  
        start_button.button.config(state=tk.DISABLED)
        paused_button.button.config(state=tk.ACTIVE)
        stop_button.button.config(state=tk.ACTIVE)
        
    else :
        messagebox.showinfo("错误", "请选择游戏窗口！") 
        
def on_paused_click(event):
    if hwnd != 0:
        hyper.paused = not hyper.paused
        if  hyper.paused:
            paused_button.button.config(text='继续')
        else :
            paused_button.button.config(text='暂停')
            
def on_stop_click(event):
    if hwnd != 0:
        hyper.stop = True
        hyper.paused = False
        stop_button.button.config(state=tk.DISABLED)
        paused_button.button.config(state=tk.DISABLED)
        paused_button.button.config(text='暂停')
        start_button.button.config(state=tk.ACTIVE)
        entry1_s.config(state=tk.NORMAL)
        entry2_s.config(state=tk.NORMAL)
        entry3_s.config(state=tk.NORMAL)
        entry4_s.config(state=tk.NORMAL)
        entry1.config(state=tk.NORMAL)
        entry2.config(state=tk.NORMAL)
        entry3.config(state=tk.NORMAL)
        
def on_test_ocr_click(event):
    if hwnd != 0:
        page_test.show_screen_ocr(hwnd)
        
        
 #自定义button    
class EventButton:
    def __init__(self, root,text,row,column):  
        self.root = root  
        self.button = tk.Button(root, text=text, command=self.on_click)  
        self.button.grid(row=row,column=column,pady=10,padx=10,sticky="nsew")
        self.event_handlers = {}  # 用于存储事件和对应处理函数的字典

    def on_click(self):
        # 当按钮被点击时，触发所有注册到这个按钮的事件处理函数  
        for _, handler in self.event_handlers.items():  
            handler(event) 
    def register_event_handler(self, event_name, handler):  
        # 注册一个事件处理函数到特定的事件上  
        self.event_handlers[event_name] = handler
    
    # 重写on_event方法以处理来自事件系统的通知  
    def on_event(self, event_name, *args, **kwargs):  
        # 检查是否有为这个事件注册的处理函数，并调用它  
        if event_name in self.event_handlers:  
            self.event_handlers[event_name](*args, **kwargs)    

# 获取所有窗口句柄列表
# 参数:无
# 返回值:句柄列表 格式 ["title:hwnd_id",...]
def get_window_hwnd_list():
    hwnd_list = []
    windows = get_all_windows()
    for w_hwnd, title in windows: 
        item =  title + ":" + str(w_hwnd)
        hwnd_list.append(item)
    return hwnd_list

# 创建一个事件系统  
event_system = {  
    "start_clicked": event.Event("start_clicked")  
}
        
if __name__ == "__main__":
    # 获取所有窗口句柄列表
    hwnd_list = get_window_hwnd_list()
    # 构建界面
    # 参数: hwndList 桌面窗口句柄列表
    root = tk.Tk()  
    root.title("AFK2Hyper")
    # 使用StringVar来存储选中的值  
    window_menu_var = tk.StringVar(value="请选择游戏窗口")
    window_menu = tk.OptionMenu(root, window_menu_var, *hwnd_list)  
    window_menu.pack(fill=tk.X,padx=5, pady=5)
    window_menu_var.trace("w", on_select)
    draw_mode_list = []
    for dm in cus_enum.DrawMode:
        draw_mode_list.append(dm.value)

    mode_menu_var = tk.StringVar(value=cus_enum.DrawMode.TURBO_DRAW_EPIC.value)
    mode_menu = tk.OptionMenu(root, mode_menu_var, *draw_mode_list)  
    mode_menu.pack(fill=tk.X,padx=5, pady=5)
    mode_menu_var.trace("w", on_mode_select)
    text = tk.Label(width=30,text="请输入背包库存")
    text.pack(padx=5, pady=20)
    # 创建父框架，使用pack布局
    parent_frame = tk.Frame(root)
    parent_frame.pack(padx=10, pady=10)
    

    # 在父框架内使用grid布局
    text1 = tk.Label(parent_frame,width=15,text="白票数量")
    text1.grid(row=0, column=0, padx=5, pady=5)

    text2 = tk.Label(parent_frame,text="红票数量")
    text2.grid(row=0, column=1, padx=5, pady=5)
    
    text3 = tk.Label(parent_frame,text="水晶球数量")
    text3.grid(row=0, column=2, padx=5, pady=5)
    
    # 创建第一个输入框
    entry1 = tk.Entry(parent_frame, width=15)
    entry1.grid(row=1, column=0, padx=5, pady=5)
    entry1.insert(tk.END,"60")
    # 创建第二个输入框
    entry2 = tk.Entry(parent_frame, width=15)
    entry2.grid(row=1, column=1, padx=5, pady=5)
    entry2.insert(tk.END,"30")
    # 创建第三个输入框
    entry3 = tk.Entry(parent_frame, width=15)
    entry3.grid(row=1, column=2, padx=5, pady=5)
    entry3.insert(tk.END,"40")
    
    text_s = tk.Label(width=30,text="设置抽卡窗口期")
    text_s.pack(padx=5, pady=20)
    
    # 创建父框架，使用pack布局
    parent_frame_2 = tk.Frame(root)
    parent_frame_2.pack(fill=tk.X, expand=True, padx=10, pady=10)
    # 在父框架内使用grid布局
    text1_s = tk.Label(parent_frame_2,width=15,text="小时开始时间(0-24)")
    text1_s.grid(row=0, column=0, padx=5, pady=5)

    text2_s = tk.Label(parent_frame_2,text="小时结束时间(0-24)")
    text2_s.grid(row=0, column=1, padx=5, pady=5)
    
    text3_s = tk.Label(parent_frame_2,text="分钟开始时间(0-60)")
    text3_s.grid(row=0, column=2, padx=5, pady=5)
    
    text4_s = tk.Label(parent_frame_2,text="分钟结束时间(0-60)")
    text4_s.grid(row=0, column=3, padx=5, pady=5)
    
    # 创建第一个输入框
    entry1_s = tk.Entry(parent_frame_2, width=15)
    entry1_s.grid(row=1, column=0, padx=5, pady=5)
    entry1_s.insert(tk.END,"1")
    # 创建第二个输入框
    entry2_s = tk.Entry(parent_frame_2, width=15)
    entry2_s.grid(row=1, column=1, padx=5, pady=5)
    entry2_s.insert(tk.END,"5")
    # 创建第三个输入框
    entry3_s = tk.Entry(parent_frame_2, width=15)
    entry3_s.grid(row=1, column=2, padx=5, pady=5)
    entry3_s.insert(tk.END,"58")
    # 创建第四个输入框
    entry4_s = tk.Entry(parent_frame_2, width=15)
    entry4_s.grid(row=1, column=3, padx=5, pady=5)
    entry4_s.insert(tk.END,"3")
    
    # 创建父框架，使用pack布局
    button_frame = tk.Frame(root)
    button_frame.pack( padx=10, pady=10)
    start_button = EventButton(button_frame,'开始',0,0)
    start_button.register_event_handler("start_clicked", on_start_click)
    paused_button = EventButton(button_frame,'暂停',0,1)
    paused_button.button.config(state=tk.DISABLED)
    paused_button.register_event_handler("start_clicked",on_paused_click)
    stop_button = EventButton(button_frame,'停止',0,2)
    stop_button.register_event_handler("start_clicked", on_stop_click)
    stop_button.button.config(state=tk.DISABLED)
    
    test_ocr_button = EventButton(button_frame,'识别文字',0,3)
    test_ocr_button.register_event_handler("start_clicked", on_test_ocr_click)
    
    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)  
    log_text.pack(padx=10, pady=10)
    log_text.config(state=tk.NORMAL)
    
    close_button = tk.Button(root, text="关闭", command=on_closing)
    close_button.pack(pady=5)

    
    # 安排check_queue函数在主线程的事件循环中定期运行  
    root.after(100, check_queue)
    # 绑定窗口关闭事件到on_closing函数  
    root.protocol("WM_DELETE_WINDOW", on_closing)  
   
    
    # 运行tkinter事件循环  
    root.mainloop()

    
    
   

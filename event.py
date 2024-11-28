# 定义一个事件类，用于存储事件信息  
class Event:  
    def __init__(self, name):  
        self.name = name  
        self.listeners = []  
  
    def add_listener(self, listener):  
        self.listeners.append(listener)  
  
    def notify(self, *args, **kwargs):  
        for listener in self.listeners:  
            listener(*args, **kwargs)  
  
# 定义一个观察者类，它可以是任何Tkinter组件或自定义类  
class Observer:  
    def on_event(self, event, *args, **kwargs):  
        # 这个方法应该被子类重写以处理特定的事件  
        pass
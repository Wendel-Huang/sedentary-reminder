import pynput
import time
from pynput import mouse, keyboard
#无键盘，鼠标输入后一分钟，将状态置位休息中(休息计时置为60并开始计时，工作计时暂停），（若工作计时未达50min开始主动休息，休息结束时工作计时继续）休息满五分钟restMax，允许进入工作（工作计时清零）
# ，工作状态时，计时满50分钟，弹出久坐提醒（保持最大化最前端），最小化所有其他窗口，显示按钮继续工作3-2-1分钟
import threading
import tkinter as tk

import tkinter.messagebox as messagebox

workTime = 0
maxWorkTime = 50*60 #最长连续工作50min
maxWorkTimeReset = 120
restTime = 0
restMax = 5*60

countMax = 60
count = 0#距离最后一次鼠标键盘操作的时间，若大于countMax，认为进入休息状态

maxZaigan = 3
zaigan = 3

backcolor = '#6B8E23'

window = tk.Tk()
window.title('久坐提醒')
window.geometry('2920x1080-2-5')
window.configure(bg=backcolor)

def getZaigan():
    global zaigan
    return zaigan
def setZaigan():
    global zaigan
    global maxWorkTime
    maxWorkTime += zaigan*60
    window.state('icon')
    if zaigan>1:
        zaigan-=1
def resetZaigan():
    global zaigan
    global maxZaigan
    global maxWorkTime
    zaigan = maxZaigan
    maxWorkTime = maxWorkTimeReset

varLabel = tk.StringVar()    # 这时文字变量储存器
l = tk.Label(window,
    textvariable=varLabel,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg=backcolor, font=('Arial', 12), width=50, height=10)
l.pack()
# window.attributes("-topmost", True)
window.state('icon')
window.resizable(0, 0)

varButton = tk.StringVar()
b = tk.Button(window,
              textvariable=varButton,  # 显示在按钮上的文字
              width=60, height=2, bg=backcolor,
              command=setZaigan)  # 点击按钮式执行的命令




def callback():
    messagebox.showwarning('警告','劝你不要关闭此程序！')
window.protocol("WM_DELETE_WINDOW", callback)



class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # 监听鼠标
        def on_click(x, y, button, pressed):
            if pressed:
                global count
                count = 0
                # print("pressed")

        def on_move(x, y):
            global count
            count = 0

        mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
        mouse_listener.start()

        def on_press(key):
            global count
            count = 0
            # print("key pressed")

        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.start()

        while True:
            global count
            global restTime
            global workTime
            window.geometry('2920x1000+0+0')
            time.sleep(1)
            count += 1
            if count<=countMax:
                workTime += 1
                restTime = 0
            if count>countMax:
                if restTime<60:
                    restTime = 60
                else:
                    restTime += 1
            if restTime>restMax:
                workTime = 0
                resetZaigan()
            if workTime<=maxWorkTime:
                varLabel.set('已工作{}min{}s'.format(workTime // 60, workTime%60))
                b.pack_forget()# 按钮隐藏
            if workTime>maxWorkTime:
                varButton.set('扶朕起来，还能再干{}分钟'.format(getZaigan()))
                varLabel.set('已久坐{}min，起来走动走动！\n已休息{}s'.format(workTime//60,restTime))
                b.pack()
                window.state('normal')
                window.geometry('2920x1000+0+0')
                window.attributes("-topmost", True)
            # print(count, workTime)

# 创建新线程
thread1 = myThread()
# 开启线程
thread1.start()




window.mainloop()



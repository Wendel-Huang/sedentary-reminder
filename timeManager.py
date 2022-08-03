import pynput
import time
from pynput import mouse, keyboard
#无键盘，鼠标输入后一分钟，将状态置位休息中(休息计时置为60并开始计时，工作计时暂停），（若工作计时未达50min开始主动休息，休息结束时工作计时继续）休息满五分钟restMax，允许进入工作（工作计时清零）
# ，工作状态时，计时满50分钟，弹出久坐提醒（保持最大化最前端），最小化所有其他窗口，显示按钮继续工作3-2-1分钟
import threading
# import mttkinter as tk
from mttkinter import mtTkinter as tk

import tkinter.messagebox as messagebox

workTime = 0
maxWorkTime = 20 #最长连续工作50min
maxWorkTimeReset = 50*60
restTime = 0
restMax = 5*60

countMax = 60
count = 0#距离最后一次鼠标键盘操作的时间，若大于countMax，认为进入休息状态

maxZaigan = 3
zaigan = 3

backcolor = '#6B8E23'
window2 = tk.Tk()
window2.title('久坐提醒2')
window2.geometry('1920x1080+3840+1080')
window2.configure(bg=backcolor)

window1 = tk.Tk()
window1.title('久坐提醒1')
window1.geometry('1920x1080+0+0')
window1.configure(bg=backcolor)


def getZaigan():
    global zaigan
    return zaigan
def setZaigan():
    global zaigan
    global maxWorkTime
    maxWorkTime += zaigan*60
    window1.state('icon')
    window2.state('icon')
    if zaigan>1:
        zaigan-=1
def resetZaigan():
    global zaigan
    global maxZaigan
    global maxWorkTime
    zaigan = maxZaigan
    maxWorkTime = maxWorkTimeReset

varLabel2 = tk.StringVar()    # 这时文字变量储存器
varLabel1 = tk.StringVar()    # 这时文字变量储存器

l1 = tk.Label(window1,
    textvariable=varLabel1,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg=backcolor, font=('Arial', 30), width=50, height=10)
l1.pack()
# window1.attributes("-topmost", True)
window1.state('icon')
window1.resizable(0, 0)

l2 = tk.Label(window2,
    textvariable=varLabel2,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg=backcolor, font=('Arial', 20), width=50, height=10)
l2.pack()
# window2.attributes("-topmost", True)
window2.state('icon')
window2.resizable(0, 0)

varButton = tk.StringVar()
b1 = tk.Button(window1,
              textvariable=varButton,  # 显示在按钮上的文字
              width=60, height=2, bg=backcolor,
              command=setZaigan)  # 点击按钮式执行的命令
b2 = tk.Button(window2,
              textvariable=varButton,  # 显示在按钮上的文字
              width=60, height=2, bg=backcolor,
              command=setZaigan)  # 点击按钮式执行的命令




def callback():
    messagebox.showwarning('警告','劝你不要关闭此程序！')
window1.protocol("WM_DELETE_WINDOW", callback)
window2.protocol("WM_DELETE_WINDOW", callback)






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

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while True:
            global count
            global restTime
            global workTime
            time.sleep(1)
            window1.geometry('1920x1080+0+0')
            window2.geometry('1920x1080+3840+1080')

            count += 1
            if count <= countMax:
                workTime += 1
                restTime = 0
            if count > countMax:
                if restTime < 60:
                    restTime = 60
                else:
                    restTime += 1
            if restTime > restMax:
                workTime = 0
                resetZaigan()
            if workTime <= maxWorkTime:
                varLabel1.set('已工作{}min{}s'.format(workTime // 60, workTime % 60))
                varLabel2.set('已工作{}min{}s'.format(workTime // 60, workTime % 60))
                b1.pack_forget()  # 按钮隐藏
                b2.pack_forget()  # 按钮隐藏
            if workTime > maxWorkTime:
                varButton.set('扶朕起来，还能再干{}分钟'.format(getZaigan()))
                varLabel1.set('已久坐{}min，起走动走动！\n已休息{}s'.format(workTime // 60, restTime))
                varLabel2.set('已久坐{}min，来走动走动！\n已休息{}s'.format(workTime // 60, restTime))
                b1.pack()
                b2.pack()
                window1.state('normal')
                window1.geometry('1920x1080+0+0')
                window1.attributes("-topmost", True)
                window2.state('normal')
                window2.geometry('1920x1080+3840+1080')
                window2.attributes("-topmost", True)
            # print(count, workTime)

# 创建新线程
thread = myThread()
# 开启线程
thread.start()

tk.mainloop()





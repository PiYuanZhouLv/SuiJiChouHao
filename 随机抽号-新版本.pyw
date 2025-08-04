import random
import sys
import threading
import time
import tkinter
from tkinter import messagebox as msgbox
import json
import os

__VERSION__ = "3.1.3(reverted change from 3.1.0re)"

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

root = tkinter.Tk()
root.title('随机抽号')

root.resizable(False, False)

topic = tkinter.StringVar(root, '点击下方随机抽号开始')
tt = tkinter.Label(textvariable=topic, border=10, font=('default', 20), width=20)
tt.grid(column=0, row=0, columnspan=2, sticky="NEWS", padx=5, pady=5)

n1 = tkinter.StringVar(root, '?')
n1l = tkinter.Label(textvariable=n1, bg="#FFC0C0", font=('default', 60), width=2)
n1l.grid(column=0, row=1, sticky='ens', padx=5, pady=5)

n2 = tkinter.StringVar(root, '?')
n2l = tkinter.Label(textvariable=n2, bg="#FFC0C0", font=('default', 60), width=2)
n2l.grid(column=1, row=1, sticky='wns', padx=5, pady=5)

try:
    os.makedirs(os.path.join(os.environ['APPDATA'], 'PiYuanZhouLv/sjch'), exist_ok=True)
    with open(os.path.join(os.environ['APPDATA'], 'PiYuanZhouLv/sjch', 'sjch.setting')) as f:
        setting = json.loads(f.read())
        assert "out" in setting
        # for (k, v) in list(setting['lasttime'].items()):
        #     setting['lasttime'].pop(k)
        #     setting['lasttime'][int(k)] = v
except:
    msgbox.showwarning('启用默认设置', '配置文件无法读取，已启用默认设置')
    setting = {
        "setting":{
            "left": 1,
            "right": 65,
            # "decay": 10
        },
        "out": []
        # "lasttime":{i: -1 for i in range(1, 66)}
    }

def save_setting():
    with open(os.path.join(os.environ['APPDATA'], 'PiYuanZhouLv/sjch', 'sjch.setting'), 'w') as f:
        f.write(json.dumps(setting))

running = False
left = [i for i in range(setting['setting']['left'], setting['setting']['right']+1) if i not in setting['out']]

def running_text(text):
    global running
    text = list(text)
    topic.set(''.join(text[:8]))
    time.sleep(0.3)
    running = True
    while running:
        topic.set(''.join(text[:8]))
        text.append(text.pop(0))
        time.sleep(0.2)

# def calculate_weights():
#     return list(map(lambda x: 1 if x[1] < 0 else 1 - (1/2)**((time.time()-x[1])/(setting['setting']['decay']*24*60*60)), sorted(list(setting['lasttime'].items()), key=lambda x: x[0])))

# print(setting['lasttime'])
# print(calculate_weights())

def start(*args):
    global running, left
    if running:
        running = False
    sb['state'] = 'disabled'
    # print(list(enumerate(calculate_weights(), setting['setting']['left'])))
    # lucky = random.choices(list(range(setting['setting']['left'], setting['setting']['right']+1)), calculate_weights(), k=1)[0]
    # print(list(enumerate(calculate_weights(), setting['setting']['left']))[lucky-setting['setting']['left']], f"{calculate_weights()[lucky-setting['setting']['left']]/sum(calculate_weights()):.2%} max: {max(calculate_weights())/sum(calculate_weights()):.2%}")
    # setting['lasttime'][lucky] = time.time()
    lucky = random.choice(left)
    setting['out'].append(lucky)
    left.remove(lucky)
    save_setting()
    n1l['bg'] = "#FFC0C0"
    n2l['bg'] = "#FFC0C0"
    n1.set('?')
    n2.set('?')
    topic.set('这次会是谁呢?')
    time.sleep(0.7)
    t = time.time()
    while True:
        n1.set(str(random.randint(0, 9)))
        n2.set(str(random.randint(0, 9)))
        if time.time() >= t + 0.7:
            break
        time.sleep(0.01)
    n1l['bg'] = "#C0FFC0"
    topic.set(f'第一位是{lucky // 10}')
    n1.set(str(lucky // 10))
    t = time.time()
    while True:
        n2.set(str(random.randint(0, 9)))
        if time.time() >= t + 0.7:
            break
        time.sleep(0.01)
    n2l['bg'] = "#C0FFC0"
    topic.set(f'第二位是{lucky % 10}')
    n2.set(str(lucky % 10))
    time.sleep(0.2)
    n1l['bg'] = "#FF8000"
    n2l['bg'] = "#FF8000"
    time.sleep(0.2)
    n1l['bg'] = "#FFFF00"
    n2l['bg'] = "#FFFF00"
    time.sleep(0.2)
    n1l['bg'] = "#00FFFF"
    n2l['bg'] = "#00FFFF"
    time.sleep(0.2)
    n1l['bg'] = "#C0FFC0"
    n2l['bg'] = "#C0FFC0"
    topic.set(f'恭喜第{lucky}号被抽中')
    sb['state'] = 'normal'
    if not left:
        left = list(range(setting['setting']['left'], setting['setting']['right']+1))
        setting['out'] = []
        save_setting()
        time.sleep(0.3)
        running_text("新的一轮即将开始，请大家做好准备！")


sb = tkinter.Button(root, font=('default', 20), text='随机抽号',
                    command=lambda *args: threading.Thread(target=start).start())
sb.grid(column=0, row=2, columnspan=2, sticky='news', padx=5, pady=5)


def configure_setting(*_):
    global sbt
    sw = tkinter.Toplevel(root)
    setting_var = {}
    sw.resizable(False, False)
    sw.title("设置")
    fwlf = tkinter.LabelFrame(sw, text='抽号范围', font=('default', 15))

    ready = False

    def on_change(*event):

        def on_real_change(*event):
            if not ready:
                # print('not ready')
                return True
            global sbt
            # print('go ahead')
            try:
                if (setting_var['left'].get() <= setting_var['right'].get()
                    and not (setting['setting']['left'] == setting_var['left'].get()
                             and setting_var['right'].get() == setting['setting']['right'])):
                    sbt['state'] = 'normal'
                    # print('normal')
                else:
                    sbt['state'] = 'disabled'
                    # print('disabled')
            except tkinter.TclError:
                sbt['state'] = 'disabled'
                # print('error')
        sw.after(1, on_real_change)
        return True

    def on_save(*event):
        setting['setting']['left'] = setting_var['left'].get()
        setting['setting']['right'] = setting_var['right'].get()
        setting['out'] = list(filter(lambda x: setting['setting']['left'] <= x <= setting['setting']['right'], setting['out']))
        global sbt, left
        left = [i for i in range(setting['setting']['left'], setting['setting']['right']+1) if i not in setting['out']]
        sbt['state'] = 'disabled'
        save_setting()

    tkinter.Label(fwlf, text="抽取自", font=('default', 15)).pack(side="left")
    setting_var['left'] = tkinter.IntVar(value=setting['setting']['left'])
    tkinter.Entry(fwlf, textvariable=setting_var['left'], width=3, font=('default', 15),
                  validate='key', validatecommand=(root.register(on_change),)).pack(side='left')
    tkinter.Label(fwlf, text='号至', font=('default', 15)).pack(side="left")
    setting_var['right'] = tkinter.IntVar(value=setting['setting']['right'])
    tkinter.Entry(fwlf, textvariable=setting_var['right'], width=3, font=('default', 15),
                  validate='key', validatecommand=(root.register(on_change),)).pack(side='left')
    tkinter.Label(fwlf, text='号的同学', font=('default', 15)).pack(side="left")
    sbt = tkinter.Button(fwlf, text='保存', font=('default', 15), state='disabled', command=on_save)
    sbt.pack(side="left")
    fwlf.pack(padx=5, pady=5, fill='both')

    # hflf = tkinter.LabelFrame(sw, text='恢复系数', font=('default', 15))

    # def on_change2(*event):

    #     def on_real_change2(*event):
    #         if not ready:
    #             # print('not ready')
    #             return True
    #         nonlocal sbt2
    #         # print('go ahead')
    #         try:
    #             if (0 <= setting_var['decay'].get() != setting['setting']['decay']):
    #                 sbt2['state'] = 'normal'
    #                 # print('normal')
    #             else:
    #                 sbt2['state'] = 'disabled'
    #                 # print('disabled')
    #         except tkinter.TclError:
    #             sbt2['state'] = 'disabled'
    #             # print('error')
    #     sw.after(1, on_real_change2)
    #     return True

    # def on_save2(*event):
    #     setting['setting']['decay'] = setting_var['decay'].get()
    #     nonlocal sbt2
    #     sbt2['state'] = 'disabled'
    #     save_setting()

    # setting_var['decay'] = tkinter.DoubleVar(value=setting['setting']['decay'])
    # tkinter.Entry(hflf, textvariable=setting_var['decay'], font=('default', 15), validate='key', validatecommand=(root.register(on_change2),)).pack(side='left')
    # sbt2 = tkinter.Button(hflf, text='保存', font=('default', 15), state='disabled', command=on_save2)
    # sbt2.pack(side="left")
    # tkinter.Button(hflf, text='?', command=lambda *_: msgbox.showinfo('恢复系数', '恢复系数是一大于零的数值，其数值等于被抽中后相对概率被调回1/2的天数。\n值越大，其行为越类似使用抽样池的版本；\n值越小，其行为越接近无限制的版本。')).pack(side='left')
    # hflf.pack()

    about = tkinter.LabelFrame(sw, text='关于', font=('default', 15))
    tkinter.Label(about, text=f"随机抽号版本：{__VERSION__}").pack()
    tkinter.Label(about, text=f"Python运行环境：{sys.version.split(' ')[0]}").pack()
    tkinter.Label(about, text=f"Tk/Tcl版本：{tkinter.TkVersion} / {tkinter.TclVersion}").pack()
    tkinter.Label(about, text="作者：温予乐").pack()
    about.pack(padx=5, pady=5, fill='both')

    ready = True


sb2 = tkinter.Button(root, font=('default', 15), text='设置',
                     command=configure_setting)
sb2.grid(column=0, row=3, columnspan=2, sticky='news', padx=5, pady=5)

root.rowconfigure("all", weight=1)
root.columnconfigure("all", weight=1)


def on_close(*args):
    global running
    running = False
    root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close)

root.mainloop()

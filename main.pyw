import random
import re
import threading
import time
import tkinter
from tkinter import messagebox

root = tkinter.Tk()
root.title('随机抽号')
root.attributes('-topmost', True)

geo = ""
hiding = False
hide = False
showing = False


def hiding_finished():
    global hiding
    hiding = False


def show_finished():
    global showing
    showing = False


def hide_me(event):
    global geo, hiding, hide
    if not hiding and not hide and not showing:
        hiding = True
        print("hm", hide, hiding, showing)
        geo = root.geometry()
        w, h, x, y = re.split('[+x]', geo)
        root.geometry(f'+{1 - int(w)}+{y}')
        hide = True
        root.after(500, hiding_finished)


def show_me(event):
    global hide, showing
    if hide and not hiding and not showing:
        showing = True
        print("sm", hide, hiding, showing)
        root.geometry(geo)
        root.after(500, show_finished)
        hide = False


root.bind('<Enter>', lambda *args: root.attributes('-alpha', 1.0))
root.bind('<Leave>', lambda *args: root.attributes('-alpha', 0.4))
# root.bind('<Enter>', show_me)
# root.bind('<Leave>', hide_me)


def fine(event):
    tl = tkinter.Toplevel(root)
    tl.title('加罚号码')
    ll_box = tkinter.Listbox(tl)
    for lli in lucky_list:
        ll_box.insert(0, lli)

    def on_fine(event2):
        n = int(ll_box.get(ll_box.curselection()))
        if messagebox.askokcancel('加罚确认', f'你确认要加罚{n}号吗?'):
            left.append(n)
            out.remove(n)
            messagebox.showinfo('加罚成功', f'成功, 已将{n}号加罚')

    ll_box.bind('<Double-Button-1>', on_fine)
    ll_box.pack()


topic = tkinter.StringVar(root, '点击下方随机抽号开始')
tt = tkinter.Label(textvariable=topic, border=10, font=('default', 15), width=20)
tt.grid(column=0, row=0, columnspan=2, sticky='news')
tt.bind('<Double-Button-1>', fine)

n1 = tkinter.StringVar(root, '?')
n1l = tkinter.Label(textvariable=n1, bg="#FFC0C0", font=('default', 30), width=2)
n1l.grid(column=0, row=1, sticky='e')

n2 = tkinter.StringVar(root, '?')
n2l = tkinter.Label(textvariable=n2, bg="#FFC0C0", font=('default', 30), width=2)
n2l.grid(column=1, row=1, sticky='w')

try:
    out = [int(i) for i in open('sjch.setting').read().split(',')]
except (FileNotFoundError, ValueError):
    out = []
left = list(range(1, 66))
for o in out[:]:
    if o in left:
        left.remove(o)
    elif o < 0:
        pass
lucky_list = []

running = False


def running_text(text):
    global running
    text = list(text)
    topic.set(''.join(text[:8]))
    time.sleep(0.6)
    running = True
    while running:
        topic.set(''.join(text[:8]))
        text.append(text.pop(0))
        time.sleep(0.3)


def start(*args):
    global out, left, running
    if running:
        running = False
    sb['state'] = 'disabled'
    lucky = random.choice(left)
    left.remove(lucky)
    out.append(lucky)
    if not left:
        left = list(range(1, 66))
        out = []
    lucky = abs(lucky)
    lucky_list.append(lucky)
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
    if not out:
        threading.Thread(target=running_text, args=('新的一轮抽号开始，请所有同学做好准备！',)).start()
    else:
        topic.set(f'恭喜第{lucky}号被抽中')
    sb['state'] = 'normal'


sb = tkinter.Button(root, font=('default', 15), text='随机抽号',
                    command=lambda *args: threading.Thread(target=start).start())
sb.grid(column=0, row=2, columnspan=2, sticky='news')


def on_close(*args):
    global running
    running = False
    open('sjch.setting', 'w').write(','.join([str(i) for i in out]))
    root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close)

root.mainloop()

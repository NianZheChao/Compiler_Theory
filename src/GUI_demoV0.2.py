# from tkinter import *
import tkinter as tk
from tkinter.filedialog import *
from PIL import Image

window = tk.Tk()
window.title('Compiler Theory Demo')
window.geometry('800x600')

l = tk.Label(window, bg='gray', width=25, height=2, text='Demo V0.2')
l.pack()

counter = 0


def do_job():
    global counter
    l.config(text='do' + str(counter))
    counter += 1


def openFile():
    filePath = askopenfilename()
    with open(filePath, encoding='UTF-8') as f:
        text1.insert(1.0, f.read())


menubar = tk.Menu(window)
fileMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='文件', menu=fileMenu)
fileMenu.add_command(label='新建', command=do_job)
fileMenu.add_command(label='打开', command=openFile)
fileMenu.add_command(label='保存', command=do_job)
fileMenu.add_separator()
fileMenu.add_command(label='退出', command=window.quit)

editMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='编辑', menu=editMenu)
editMenu.add_command(label='剪切', command=do_job)
editMenu.add_command(label='复制', command=do_job)
editMenu.add_command(label='粘贴', command=do_job)

text1 = tk.Text(window, width=55, height=40)
text1.pack(side='left', padx=1, pady=1)

text2 = tk.Text(window, width=55, height=40)
text2.pack(side='right', padx=1, pady=1)

# text3 = tk.Text(window, width=55, height=20)
# text3.pack(side='right', padx=1, pady=1)
# text.pack(fill=tk.X, side=tk.TOP)
# 填充用法


# root = Tk()
# root.title("compiler theory Demo")
# root.geometry('600x800')
# root.resizable(width=True, height=True)


# 输入框的简单尝试
# t = Text(root)
# t.insert(1.0, 'hello\n')
# t.insert(END, 'hello000000\n')
# t.insert(END, 'nono')
# t.pack()
window.config(menu=menubar)
window.mainloop()

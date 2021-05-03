# from tkinter import *
import tkinter as tk
from tkinter.filedialog import *
import os
import cifa

global filePath

window = tk.Tk()
window.title('Compiler Theory Demo')
window.geometry('800x600')
window.resizable(width=False, height=False)

l = tk.Label(window, bg='gray', width=25, height=2, text='Demo V0.2')
l.pack()

counter = 0


def openFile():
    global filePath
    filePath = askopenfilename()
    # with open(filePath, encoding='UTF-8') as f:
    #     text1.insert(1.0, f.read())
    with open(filePath) as f:
        text1.insert(1.0, f.read())


def cut():
    s = text1.get('1.0', END)
    text3.insert(1.0, s)
    text1.delete('1.0', END)


def save():
    fh = open('temp.log', 'w')
    s = text1.get('1.0', END)
    fh.write(s)
    fh.close()


def help():
    os.system('D:\\pythonProject\\help.CHM')


def lexicialAnalysisGUI():
    global filePath
    # todo: 只能通过filePath的方式引入文件做词法分析
    wordList = cifa.lexAnalyse(filePath)
    text2.insert("insert", "%s  %s  %s \n" % ('单词', '类型', '行数'))
    for i in wordList:
        text2.insert("insert", " %s   %s   %s \n" % (i['word'], i['type'], i["line"]))


menubar = tk.Menu(window)

fileMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='文件', menu=fileMenu)
fileMenu.add_command(label='打开', command=openFile)
fileMenu.add_command(label='保存', command=save)
fileMenu.add_separator()
fileMenu.add_command(label='退出', command=window.quit)

editMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='分析', menu=editMenu)
editMenu.add_command(label='词法分析', command=lexicialAnalysisGUI)
# editMenu.add_command(label='语法分析', command=cifa.lexAnalyse())

aboutMenu = tk.Menu(menubar, tearoff=0)
menubar.add_command(label='帮助', command=help)

text1 = tk.Text(window, width=55, height=44)
text1.pack(side=tk.LEFT, padx=1, pady=1)

text2 = tk.Text(window, width=55, height=21)
text2.pack(side='top', padx=1, pady=1)

text3 = tk.Text(window, width=55, height=21)
text3.pack(side='bottom', padx=1, pady=1)

window.config(menu=menubar)
window.mainloop()

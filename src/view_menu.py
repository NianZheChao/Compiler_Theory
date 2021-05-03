import tkinter
from lexical_analysis import get_seed_code, get_source_file, get_txt, remove_note, get_token, wri_txt
from syntax_analysis import get_data


# 菜单界面
def menu():
    view = tkinter.Tk()
    view.geometry("620x520")

    # 源文件栏
    txt = tkinter.Text(view, width=45, height=60)
    txt.pack()
    txt.place(x=0, y=0)

    # 词法分析后
    txt1 = tkinter.Text(view, width=45, height=25)
    txt1.pack()
    txt1.place(x=320, y=0)

    # 错误信息
    txt2 = tkinter.Text(view, width=45, height=15)
    txt2.insert('end', '-------------------错误信息----------------')
    txt2.insert('end', '\n')
    txt2.pack()
    txt2.place(x=320, y=340)

    menus = tkinter.Menu(view)
    view.config(menu=menus)

    menus1 = tkinter.Menu(menus, tearoff=False)

    seed = get_seed_code()

    for item in ["新建", "打开", "编辑", "删除", "退出"]:
        if item == "退出":
            menus1.add_command(label=item, command=view.quit)  # #退出窗体程序
        if item == "打开":
            menus1.add_command(label=item, command=lambda: get_source_file(get_txt(txt)))
        else:
            menus1.add_command(label=item, command=txt.delete(0.0, 'end'))

    def get_value(k):
        global word
        word = k[0]
        global num
        num = k[1]

    menus.add_cascade(label='文件', menu=menus1)
    menus.add_cascade(label='词法分析', command=lambda: get_value(wri_txt(txt1, get_token(seed, remove_note(
        txt.get('0.0', 'end').split("\n")), txt2))))
    menus.add_cascade(label='语法分析', command=lambda: get_data(word, num, txt1, txt2))
    menus.add_cascade(label='中间代码')
    menus.add_cascade(label='目标代码生成')
    menus.add_cascade(label='查看')
    menus.add_cascade(label='帮助')

    view.mainloop()


if __name__ == '__main__':
    menu()

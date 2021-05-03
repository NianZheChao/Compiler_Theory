# 全局变量
word = []  # token串
num = []  # token值
# txt1 = None  # 输出解析进度
# txt2 = None  # 输出错误信息
row = 0  # 当前所在行
col = 0  # 当前所在列
error = 0  # 错误个数


# <说明语句>→<变量定义>│<函数声明>
def declare_statement():
    txt1.insert('end', '函数头部分析中!\n')
    global row, col, error
    if word[row][-1] == ';':
        parameter()
        main_con()
    if word[row][-1] == ')':
        func_declare()
    else:
        txt2.insert('end', '第' + str(row + 1) + '行语句定义出现错误！')
        txt2.insert('end', '\n')
        error += 1


# <参数> -> int/ char / ... <变量>,|int/ char / ... <变量>;|int/ char / ... <变量>)|空
def parameter():
    global row, col, error
    if col <= len(word[row]) - 1:
        # 判断参数-无参
        if word[row][col] == ')' and (word[row][col - 1] == '(' or num[row][col - 1] == 700):
            return
        # 形式参数
        if word[row][col] in ['int', 'float', 'char', 'double']:
            col += 1
            if col <= len(word[row]) - 1:
                if num[row][col] == 700:
                    col += 1
                    if col <= len(word[row]) - 1:
                        # 判断符号
                        if word[row][col] == ',':
                            col += 1
                            parameter()
                        elif word[row][col] == ')' and col == len(word[row]) - 1:
                            row += 1
                            col = 0
                            return
                        elif word[row][col] == ';' and '(' or ')' not in word[row]:
                            row += 1
                            col = 0
                            return
                        # 变量定义
                        elif word[row][col] == '=':
                            math_exper()
                        else:
                            txt2.insert('end', '第' + str(row + 1) + '行符号错误！')
                            txt2.insert('end', '\n')
                            error += 1
                    else:
                        txt2.insert('end', '第' + str(row + 1) + '行语句缺失符号！')
                        txt2.insert('end', '\n')
                        error += 1
                        return
                else:
                    txt2.insert('end', '第' + str(row + 1) + '行标识符错误！')
                    txt2.insert('end', '\n')
                    error += 1
                    return
            else:
                txt2.insert('end', '第' + str(row + 1) + '行缺失标识符！')
                txt2.insert('end', '\n')
                error += 1
                return
        else:
            txt2.insert('end', '第' + str(row + 1) + '行参数错误！')
            txt2.insert('end', '\n')
            error += 1
            return


# 函数声明 int / char / ...  <标识符> (<参数>){<函数体>}
def func_declare():
    global row, col, error
    # 判断标识符
    if col <= len(word[row]) - 1:
        if word[row][col] in ['int', 'float', 'char', 'double']:
            col += 1
            if col <= len(word[row]) - 1:
                if num[row][col] == 700:
                    col += 1
                    if col <= len(word[row]) - 1:
                        # 判断符号
                        if word[row][col] == '(':
                            col += 1
                            parameter()
                        else:
                            txt2.insert('end', '第' + str(row + 1) + '行缺失 （ ！')
                            txt2.insert('end', '\n')
                            error += 1
                    else:
                        txt2.insert('end', '第' + str(row + 1) + '行缺失符号！')
                        txt2.insert('end', '\n')
                        error += 1
                else:
                    txt2.insert('end', '第' + str(row + 1) + '行非标识符！')
                    txt2.insert('end', '\n')
                    error += 1
            else:
                txt2.insert('end', '第' + str(row + 1) + '行缺失标识符')
                txt2.insert('end', '\n')
                error += 1
    txt1.insert('end', '函数头部分析完成！')
    txt1.insert('end', '\n')

    func_body()


# <函数体> -><执行语句>；
def func_body():
    global row, col, error
    row += 1
    if row <= len(word) - 1:
        if word[row][col] == '{':
            col = 0
            exec_state()
            row += 1
            col = 0

            if row <= len(word) - 1 and col <= len(word[row]) - 1:
                if word[row][col] == '}':
                    return
                else:
                    txt2.insert('end', '第' + str(row + 1) + '行缺失 }!')
                    txt2.insert('end', '\n')
                    error += 1


# <执行语句> -> <赋值语句>| <条件语句>
def exec_state():
    global row, col, error
    while row <= len(word) - 1:
        row += 1
        col = 0
        # 赋值语句
        if row <= len(word) - 1:
            if word[row][col] in ['int', 'char', 'float', 'double'] or num[row][col] == 700:
                txt1.insert('end', '对第' + str(row + 1) + '行进行赋值分析！')
                txt1.insert('end', '\n')
                assign_state()

            # 条件语句
            elif word[row][col] == 'if':
                txt1.insert('end', '第' + str(row + 1) + '行进行 if 语句分析！')
                txt1.insert('end', '\n')
                condition_statement()

            # for 循环
            elif word[row][col] == 'for':
                txt1.insert('end', '第' + str(row + 1) + '行进行 for 语句分析！')
                txt1.insert('end', '\n')
                col += 1
                get_for()

            elif word[row][col] == 'void':
                declare_statement()
            else:
                return


# for 循环
def get_for():
    global row, col, error
    if word[row][col] == '(':
        col += 1
        if col <= len(word[row]) - 1:
            assign_state()

            if row <= len(word) - 1:
                condition_expression()
                if num[row][col] == 'i' or 'j':
                    col += 1
                    if col <= len(word[row]) - 1:
                        if word[row][col] == '++' or '--':
                            col += 1
                            if col <= len(word[row]) - 1:
                                if word[row][col] == ')':
                                    func_body()
                                else:
                                    txt2.insert('end', '第' + str(row + 1) + '行缺失 ）！')
                                    txt2.insert('end', '\n')
                                    error += 1
                            else:
                                txt2.insert('end', '第' + str(row + 1) + '行缺失参数！')
                                txt2.insert('end', '\n')
                                error += 1
        else:
            txt2.insert('end', '第' + str(row + 1) + '行缺失（ ！')
            txt2.insert('end', '\n')
            error += 1


# 读取{}内容
def get_brackets():
    global row, col, error
    col += 1

    if col <= len(word[row]):
        if num[row][col] == '900' or '1000':
            col += 1
            if col <= len(word[row]):
                if word[row][col] == ',':
                    get_brackets()
                if word[row][col] == '}':
                    col += 1
                    if col <= len(word[row]):
                        if word[row][col] == ';':
                            row += 1
                            col = 0
                            return
                        else:
                            txt2.insert('end', '第' + str(row + 1) + '行缺失 ; !')
                            txt2.insert('end', '\n')
                            error += 1
                    else:
                        txt2.insert('end', '第' + str(row + 1) + '行缺失 ; ！')
                        txt2.insert('end', '\n')
                        error += 1


# <赋值语句> -> <变量> = <算术表达式>
def assign_state():
    global row, col, error
    # int a = b
    if word[row][col] in ['int', 'char', 'float', 'double']:
        col += 1
        if col <= len(word[row]) - 1:
            if num[row][col] == 700:
                col += 1
                if col <= len(word[row]) - 1:
                    # int a = b
                    if word[row][col] == '=':
                        col += 1
                        if col <= len(word[row]) - 1:
                            if word[row][col] != '{':
                                math_exper()
                            elif word[row][col] == '{':
                                get_brackets()
                            elif word[row][col] == '[':
                                col += 1
                                if col <= len(word[row]) - 1:
                                    if num[row][col] == 900 or 1000 or 700:
                                        math_exper()
                                        if col <= len(word[row]) - 1:
                                            if word[row][col] == ']':
                                                col += 1
                            else:
                                txt2.insert('end', '第' + str(row + 1) + '行缺失符号！')
                                txt2.insert('end', '\n')
                                error += 1
                        else:
                            txt2.insert('end', '第' + str(row + 1) + '行缺失符号！')
                            txt2.insert('end', '\n')
                            error += 1
                    elif word[row][col] == ';':
                        return
                    else:
                        txt2.insert('end', '第' + str(row + 1) + '行缺失 ; 或 标识符 ！')
                        txt2.insert('end', '\n')
                        error += 1
                else:
                    txt2.insert('end', '第' + str(row + 1) + '行缺失 ; ！')
                    txt2.insert('end', '\n')
                    error += 1
            else:
                txt2.insert('end', '第' + str(row + 1) + '行缺失标识符！')
                txt2.insert('end', '\n')
                error += 1
        else:
            txt2.insert('end', '第' + str(row + 1) + '行缺失关键字！')
            txt2.insert('end', '\n')
            error += 1

    elif num[row][col] == 700:
        col += 1
        if col <= len(word[row]) - 1:
            # a = b
            if word[row][col] == '=':
                col += 1
                if col <= len(word[row]) - 1:
                    if num[row][col] == 700:
                        col += 1
                        if col < len(word[row]) - 1:
                            if word[row][col] == ';':
                                return
                            else:
                                txt2.insert('end', '第' + str(row + 1) + '行缺失 ; ！')
                                txt2.insert('end', '\n')
                                error += 1
                    else:
                        txt2.insert('end', '第' + str(row + 1) + '行缺失参数 ！')
                        txt2.insert('end', '\n')
                        error += 1

            # a[<算术表达式>] = temp
            elif word[row][col] == '[':
                col += 1
                if col <= len(word[row]) - 1:
                    math_exper()
                    col += 1
                    if col <= len(word[row]) - 1:
                        if word[row][col] == ']':
                            col += 1
                            if col <= len(word[row]) - 1:
                                if word[row][col] == '=':
                                    col += 1
                                    if col <= len(word[row]) - 1:
                                        if num[row][col] == 700 and col == len(word[row]) - 2:
                                            if word[row][col] == ';':
                                                return
                                            else:
                                                txt2.insert('end', '第' + str(row + 1) + '行缺失 ; !')
                                                txt2.insert('end', '\n')
                                                error += 1
                                        # a[<算术表达>] = a[<算术表达式>]
                                        elif num[row][col] == 700:
                                            col += 1
                                            if col <= len(word[row]) - 1:
                                                if word[row][col] == '[':
                                                    col += 1
                                                    if col <= len(word[row]) - 1:
                                                        math_exper()
                                                        col += 1
                                                        if col <= len(word[row]) - 1:
                                                            if word[row][col] == ']':
                                                                col += 1
                                                                if col <= len(word[row]) - 1:
                                                                    if word[row][col] == ';':
                                                                        return
                                                                    else:
                                                                        txt2.insert('end',
                                                                                    '第' + str(row + 1) + '行缺失 ; !')
                                                                        txt2.insert('end', '\n')
                                                                        error += 1
                                                                else:
                                                                    txt2.insert('end', '第' + str(row + 1) + '行缺失 ] !')
                                                                    txt2.insert('end', '\n')
                                                                    error += 1
                                                        else:
                                                            txt2.insert('end', '第' + str(row + 1) + '行缺少参数！')
                                                            txt2.insert('end', '\n')
                                                            error += 1
                                                else:
                                                    txt2.insert('end', '第' + str(row + 1) + '行缺失 [ !')
                                                    txt2.insert('end', '\n')
                                                error += 1
                                        else:
                                            txt2.insert('end', '第' + str(row + 1) + '行缺失符号！')
                                            txt2.insert('end', '\n')
                                            error += 1
    # 返回语句
    exec_state()


# <算术表达式> -> <项><算术表达式A>|空
def math_exper():
    item()
    math_exper_a()


# <算术表达式A> -> +<项><算术表达式A>|-<项><算术表达式A>|空
def math_exper_a():
    global row, col
    col -= 1
    if col <= len(word[row]) - 1:
        if word[row][col] == '+' or '-':
            col += 1
            item()
            math_exper_a()
        else:
            return


# <项> -> <因子><项A>
def item():
    factor()
    item_a()


# <项A> -> *<因子><项A>|/<因子><项A>|空
def item_a():
    global row, col
    if col <= len(word[row]) - 1:
        if word[row][col] == '*' or '/':
            col += 1
            if col <= len(word[row]) - 1:
                factor()
                item_a()
        else:
            return


# <因子>→<变量>│<常数>
def factor():
    global row, col, error
    col += 1
    if col <= len(word[row]) - 1:
        if num[row][col] in [700, 900, 1000]:
            return
        if word[row][col] == ';' or '++':
            return
        else:
            txt2.insert('end', '第' + str(row + 1) + '行因子错误')
            txt2.insert('end', '\n')
            error += 1


# <条件语句>→if<条件表达式>then<执行语句>else <执行语句>
def condition_statement():
    global row, col, error
    col += 1
    if col <= len(word[row]) - 1:
        if word[row][col] == '(':
            condition_expression()
            if word[row][col] == ')':
                col = 0
                func_body()
                row += 1
                col = 0

        if row <= len(word) - 1:
            if word[row][col] == 'else':
                col = 0
                func_body()
        else:
            txt2.insert('end', '第' + str(row + 1) + '行缺失 ; !')
            txt2.insert('end', '\n')
            error += 1


# <条件表达式>→<算术表达式><关系运算符><算术表达式>
def condition_expression():
    global row, col, error
    if col <= len(word[row]) - 1:
        if num[row][col] == 700:
            col += 1
            if col <= len(word[row]) - 1:

                # a rop b || （a+b）rop (c+d)
                if word[row][col] != '[':
                    col -= 1
                    math_exper()
                    relation_operator()
                    math_exper()

                # a[<算术表达式>] rop a[<算术表达式>]
                elif word[row][col] == '[':
                    col += 1
                    if col <= len(word[row]) - 1:
                        math_exper()
                        col += 1
                        if col <= len(word[row]) - 1:
                            if word[row][col] == ']':
                                condition_statement()
                                if num[row][col] == 700:
                                    col += 1
                                    if col <= len(word[row]) - 1:
                                        if word[row][col] == '[':
                                            col += 1
                                            if col <= len(word[row]) - 1:
                                                math_exper()
                                                col += 1
                                                if col <= len(word[row]) - 1:
                                                    if word[row][col] == ']':
                                                        return
                                                    else:
                                                        txt2.insert('end', '第' + str(row + 1) + '行缺失 ] !')
                                                        txt2.insert('end', '\n')
                                                        error += 1


# <关系运算符> →<│<=│>│>=│=│<>
def relation_operator():
    global error, row, col
    if word[row][col] in ['<', '<=', '>', '>=', '==']:
        return
    else:
        txt2.insert('end', '第' + str(row + 1) + '行关系运算符错误！')
        txt2.insert('end', '\n')
        error += 1


# 总控程序
def main_con():
    global row, col, error
    row = 0
    col = 0
    error = 0
    print(word)
    if word:
        if word[row][col] in ['int', 'char', 'float', 'double', 'void']:
            declare_statement()
        else:
            txt2.insert('end', '-------------------错误信息----------------')
            txt2.insert('end', '\n')
            print('未找到函数头部')
    else:
        return


def get_data(a, b, t1, t2):
    global word, num, txt1, txt2, error
    word = a
    num = b
    txt1 = t1
    txt2 = t2
    txt1.delete(0.0, 'end')
    txt2.delete(0.0, 'end')
    txt2.insert('end', '-------------------错误信息----------------')
    txt2.insert('end', '\n')
    main_con()
    txt2.insert('end', 'error(' + str(error) + ')  warring(0)')

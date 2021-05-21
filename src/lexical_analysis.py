import csv
from collections import defaultdict
import tkinter
from tkinter import filedialog


# 读取种别码文件
def get_seed_code():
    seed = defaultdict(int)
    with open('D:\\2020\\GitHub\\Compiler_Theory\\src\\test.csv', 'r', encoding='UTF-8') as f:
        k = csv.reader(f)
        for i in k:
            seed[str(i[0])] = i[1]
    return seed


# 得到源文件
def get_source_file(filename):
    src = []
    with open(filename, 'r') as f:
        for i in f.readlines():
            if i != '\n':
                src.append(i)
    return src
# ['void main()\n', '{\n', '    int a;\n', '    int result ;\n', '    a=2;\n', '    result =a+10*a ;\n', '}\n', '//comment test']

# 去掉注释


def remove_note(src):
    for i in src:
        for j in range(len(i)):
            if i[j] == '/':
                if i[j+1] == '/' or i[j+1] == '*':
                    src[src.index(i)] = i[:j]
                    break
            break
    for i in src:
        if not i:
            del src[src.index(i)]
    return src


# 标识
def get_identifier(token_word, token_num, line, index, txt2):
    string = ''
    error = 0
    string += str(line[index])
    index += 1
    while index != len(line):
        if line[index].isalpha() or line[index].isdigit():
            string += str(line[index])
            index += 1
        else:
            if line[index] == '_':
                error += 1
                txt2.insert('end', '第'+str(index) +
                            '行存在错误：'+string+line[index]+'\n')
            break
    token_word.append(string)
    token_num.append(700)

    return index, error


# 标识或者关键字
def get_identifier_or_alpha(token_word, token_num, seed, line, index, txt2):
    string = ''
    error = 0
    while index != len(line):
        if line[index].isalpha() or line[index].isdigit() or line[index] == '_':
            string += str(line[index])
            index += 1
        else:
            break
    if token_word:
        if token_word[-1] != '"':
            if string in seed:
                token_word.append(string)
                token_num.append(seed[string])
            else:
                token_word.append(string)
                token_num.append(700)
        else:
            token_word.append(string)
            token_num.append(1100)
    else:
        if string in seed:
            token_word.append(string)
            token_num.append(seed[string])
        else:
            token_word.append(string)
            token_num.append(700)
    return index, error


# 数
def get_number(token_word, token_num, line, index, txt2):
    string = ''
    error = 0
    while index != len(line):
        # 十六进制
        if line[index] == '0':
            if index + 1 != len(line):
                string += str(line[index])
                index += 1
                if line[index].isdigit():
                    error += 1
                    txt2.insert('end', '第' + str(index) +
                                '行存在错误：' + string + line[index] + '\n')
                    break
                if line[index] in ['x', 'X']:
                    string += str(line[index])
                    index += 1
                    while index != len(line):
                        if line[index] in ['x', 'X']:
                            error += 1
                            txt2.insert('end', '第' + str(index) +
                                        '行存在错误：' + string + line[index] + '\n')
                            break
                        if line[index].isalpha() or line[index].isdigit():
                            string += str(line[index])
                            index += 1
                        else:
                            break
                    token_word.append(string)
                    token_num.append(800)
                else:
                    token_word.append(str(0))
                    token_num.append(900)
                    break
            else:
                token_word.append(str(0))
                token_num.append(900)
                break
        # 十进制
        if index != len(line):
            if line[index].isalpha():
                error += 1
                txt2.insert('end', '第' + str(index) + '行存在错误：' +
                            string + line[index] + '\n')
                break
            if line[index].isdigit() and line[index] != 0:
                string += str(line[index])
                index += 1
                while index != len(line):
                    if line[index].isdigit():
                        string += str(line[index])
                        index += 1
                    else:
                        break
                token_word.append(string)
                token_num.append(1000)
            else:
                break

    return index, error


# 判断 +, -, *, /, >, <, =, &
def get_one(token_word, token_num, seed, line, index, txt2):
    string = ''
    error = 0
    string += line[index]
    index += 1
    while index != len(line):
        if line[index] == string or line[index] == '=':
            string += str(line[index])
            index += 1
            break
        else:
            break

    if string in seed:
        token_word.append(string)
        token_num.append(seed[line[index]])

    if string == '**':
        token_word.append(string)
        token_num.append(1200)

    return index, error


# 判断 %, !, :, ?
def get_two(token_word, token_num, seed, line, index, txt2):
    string = ''
    error = 0
    string += line[index]
    index += 1
    while index != len(line):
        if line[index] == '=':
            string += str(line[index])
            index += 1
            break
        else:
            break
    token_word.append(string)
    token_num.append(seed[line[index]])

    return index, error


# 其他字符
def get_other(token, token_word, token_num, seed, line, index, txt2, i, temp_word_row, temp_num_row):
    error = 0
    while index != len(line):
        if not line[index].isalpha() and not line[index].isdigit():
            if line[index] in ['+', '-', '*', '/', '>', '<', '=', '&']:
                index, error_1 = get_one(
                    token_word, token_num, seed, line, index, txt2)
                error += error_1
                token[token_word[-1]].append([i, index - len(token_word[-1])])
                temp_word_row.append(token_word[-1])
                temp_num_row.append(token_num[-1])
                if index == len(line):
                    break

            if line[index] in ['%', '!', ':', '?']:
                index, error_1 = get_two(
                    token_word, token_num, seed, line, index, txt2)
                error += error_1
                token[token_word[-1]].append([i, index - len(token_word[-1])])
                temp_word_row.append(token_word[-1])
                temp_num_row.append(token_num[-1])
                if index == len(line):
                    break

            k = ['{', '}', '[', ']', '(', ')', ';', '.', ';', '"', "'", ',']
            if line[index] in k:
                token_word.append(line[index])
                token_num.append(seed[line[index]])
                index += 1
                token[token_word[-1]].append([i, index - len(token_word[-1])])
                temp_word_row.append(token_word[-1])
                temp_num_row.append(token_num[-1])
                if index == len(line):
                    break
        else:
            break

    return index, error


# 处理数据
def get_token(seed, src, txt2):
    token = defaultdict(list)
    token_word = []
    token_num = []
    error = 0

    token_word_row = []
    token_num_row = []

    for i in src:
        temp_word_row = []
        temp_num_row = []

        # 去掉最后的\n
        line = i.strip('\n')
        # 根据空格分割字符串
        line = line.split()

        for string in line:
            if string in seed:
                token[string].append([src.index(i), line.index(string)])
                token_word.append(string)
                token_num.append(seed[string])
                temp_word_row.append(string)
                temp_num_row.append(seed[string])
            else:
                # 记录当前字符串长度
                line_length = len(string)
                # 当前字符位置
                index = 0

                while index != line_length:
                    # 是否为下划线
                    if string[index] == '_':
                        index, error_1 = get_identifier(
                            token_word, token_num, string, index, txt2)
                        error += error_1
                        token[token_word[-1]
                              ].append([src.index(i), line.index(string)])
                        temp_word_row.append(token_word[-1])
                        temp_num_row.append(token_num[-1])
                        if index == line_length:
                            break
                        else:
                            continue
                    # 是否为字母
                    if string[index].isalpha():
                        index, error_1 = get_identifier_or_alpha(
                            token_word, token_num, seed, string, index, txt2)
                        error += error_1
                        token[token_word[-1]
                              ].append([src.index(i), line.index(string)])
                        temp_word_row.append(token_word[-1])
                        temp_num_row.append(token_num[-1])
                        if index == line_length:
                            break
                        else:
                            continue
                    # 是否为数字
                    if string[index].isdigit():
                        index, error_1 = get_number(
                            token_word, token_num, string, index, txt2)
                        error += error_1
                        token[token_word[-1]
                              ].append([src.index(i), line.index(string)])
                        temp_word_row.append(token_word[-1])
                        temp_num_row.append(token_num[-1])
                        if index == line_length:
                            break
                        else:
                            continue
                    # 是否为其他字符
                    else:
                        index, error_1 = get_other(token, token_word, token_num, seed, string, index, txt2, src.index(
                            i), temp_word_row, temp_num_row)
                        error += error_1
                        if index == line_length:
                            break

        token_word_row.append(temp_word_row)
        token_num_row.append(temp_num_row)
    txt2.insert('end', 'error('+str(error)+')  warring(0)')
    k = [token, token_word, token_num, token_word_row, token_num_row]
    return k


# 读取文件
def get_txt(txt):
    txt.delete(0.0, 'end')
    filename = filedialog.askopenfilename(
        initialdir=r'C:\Users\yu\PycharmProjects\Compile')
    with open(filename) as file:
        text = file.read()
        txt.insert('end', text)
    return filename


# 读取文件
def wri_txt(txt1, k):
    token = k[0]
    token_word = k[1]
    token_num = k[2]
    for i in range(len(token_word)):

        txt1.insert('end', (str(token[token_word[i]][0]) +
                            '\t\t'+str(token_word[i])+'\t'+str(token_num[i])))
        txt1.insert('end', '\n')
        del token[token_word[i]][0]
    return [k[3], k[4]]

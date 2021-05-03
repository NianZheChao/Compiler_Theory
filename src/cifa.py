global wordCount
wordCount = 0
global errorCount
errorCount = 0
global wordList
wordList = []  # 单词表
global errorList
errorList = []  # 错误信息列表
global note_flag
note_flag = False
global error_flag
error_flag = False
# 关键字
key_word = {'char': 101, 'int': 102, 'double': 104, 'break': 105, 'return': 106,
            'void': 107, 'continue': 108, 'if': 109, 'main': 110, 'float': 111, 'else': 112, 'while': 113, 'for': 114,
            'printf': 115, 'scanf': 116}
# 运算符
operator = {'!': 205, '*': 206, '/': 207, '%': 208, '+': 209, '-': 210, '<': 211, '>': 212, '&': 213, '|': 214,
            '=': 215, '.': 216}
# 界符
delima = {'{': 301, '}': 302, ';': 303, ',': 304, '(': 305, ')': 306}


def isID(word):
    # 判断是否是标识符
    flag = False
    if word in key_word:
        # print("关键字")
        return flag
    if word[0].isalpha() or word[0] == "_":
        # print(word[0])
        i = 1
        while i < len(word):
            # print(word[i])
            if word[i].isalpha() or word[i].isdigit() or word[i] == '_':
                i += 1
                continue
            else:
                break
        if i >= len(word):
            # print(i)
            flag = True
    else:
        return flag
    return flag


def isInteger(word):  # 判断是否是int常量
    flag = False
    i = 0
    while i < len(word):
        # print(word[i])
        if word[i].isdigit():
            i += 1
            continue
        else:
            break
    if i >= len(word):
        # print(i)
        flag = True
    return flag


def analyse(string, line):
    global note_flag
    global errorCount
    global wordCount
    global wordList
    global errorList
    global error_flag
    begin_index = 0
    end_index = 0
    index = 0
    length = len(string)
    info = {}
    while index < length:
        temp = string[index]
        # print(temp)
        if note_flag is False:
            # print(note_flag)
            if temp.isalpha() or temp == "_":  # 判断是否是标识符
                begin_index = index
                index = index + 1
                while ((index < length) and (string[index] != ' ') and (string[index] != '\\n') and (
                        string[index:index + 1] not in operator) and (string[index:index + 1] not in delima)):
                    index += 1
                end_index = index
                # info={}
                wordCount = wordCount + 1
                word = string[begin_index:end_index]
                if word in key_word:
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '关键字'}
                    # wordList.append(info)
                elif isID(word):
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '标识符'}
                    # wordList.append(info)
                else:
                    errorCount = errorCount + 1
                    info = {'word': word, 'number': errorCount, 'line': line, 'type': '非法标识符'}
                    errorList.append(info)
                    error_flag = True

                index -= 1
            elif temp.isdigit():  # 判断是否是数字
                begin_index = index
                index += 1
                while ((index < length) and (string[index] != ' ') and (string[index] != '\\n') and (
                        string[index:index + 1] not in operator) and (string[index:index + 1] not in delima)):
                    index += 1
                end_index = index
                # info={}
                wordCount = wordCount + 1
                word = string[begin_index:end_index]
                if isInteger(word):
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '常量'}
                    # wordList.append(info)
                else:
                    errorCount = errorCount + 1
                    info = {'word': word, 'number': errorCount, 'line': line, 'type': '非法标识符'}
                    errorList.append(info)
                    error_flag = True
                index -= 1

            elif temp == '=':
                begin_index = index
                index += 1
                if index < length and string[index] == '=':
                    end_index = index + 1
                    # info={}
                    wordCount = wordCount + 1
                    word = string[begin_index:end_index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                    index -= 1

            elif temp == '!':
                begin_index = index
                index += 1
                if index < length and string[index] == '=':
                    end_index = index + 1
                    # info={}
                    wordCount = wordCount + 1
                    word = string[begin_index:end_index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                    index -= 1

            elif temp == '&':
                begin_index = index
                index += 1
                if index < length and string[index] == '&':
                    end_index = index + 1
                    # info={}
                    wordCount = wordCount + 1
                    word = string[begin_index:end_index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                    index -= 1

            elif temp == '|':
                begin_index = index
                index += 1
                if index < length and string[index] == '|':
                    end_index = index + 1
                    # info={}
                    wordCount = wordCount + 1
                    word = string[begin_index:end_index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                    index -= 1

            elif temp == '+':
                begin_index = index
                index += 1
                if index < length and string[index] == '+':
                    end_index = index + 1
                    # info={}
                    wordCount = wordCount + 1
                    word = string[begin_index:end_index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                    index -= 1

            elif temp == '-':
                begin_index = index
                index += 1
                if index < length and string[index] == '-':
                    end_index = index + 1
                    # info={}
                    wordCount = wordCount + 1
                    word = string[begin_index:end_index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                    index -= 1

            elif temp == '/':
                index += 1
                if index < length and string[index] == '/':
                    break
                elif index < length and string[index] == '*':
                    note_flag = True
                else:
                    # info={}
                    wordCount = wordCount + 1
                    word = string[index - 1:index]
                    info = {'word': word, 'number': wordCount, 'line': line, 'type': '运算符'}
                index -= 1



            else:
                if (temp == ' ') or (temp == '\\t') or (temp == '\\r') or (temp == '\\n'):
                    # print("检测到空格")
                    index += 1
                    continue
                elif ((temp in delima) or (temp == '"') or (temp == ',') or (temp == ';') or (temp == '*') or (
                        temp == '%') or (temp == '>')
                      or (temp == '<') or (temp == '?') or (temp == '#')):
                    # info={}
                    wordCount = wordCount + 1
                    # word=string[index-1:index]
                    if temp in operator:
                        info = {'word': temp, 'number': wordCount, 'line': line, 'type': '运算符'}
                    elif temp in delima:
                        info = {'word': temp, 'number': wordCount, 'line': line, 'type': '界符'}
                    else:
                        info = {'word': temp, 'number': wordCount, 'line': line, 'type': '结束符'}
                    # index+=1
                    # continue
                else:
                    # info={}
                    wordCount = wordCount + 1
                    info = {'word': temp, 'number': wordCount, 'line': line, 'type': '未知类型'}
                    errorCount = errorCount + 1
                    info = {'word': temp, 'number': errorCount, 'line': line, 'type': '非法标识符'}
                    errorList.append(info)
                    error_flag = True

        else:
            # print(note_flag)
            if temp == '*':
                index += 1
                if index < length and string[index] == '/':
                    note_flag = False
                else:
                    index += 1
                    continue
            else:
                index += 1
                continue

            # print(note_flag)
            # j=string.index("*/")
            # print("j:")
            # print(j)
            # if(j is not -1):
            #     note_flag=False
            #     index=j+2
            #     continue
            # else:
            #     break
        # if(word is null):
        #     index+=1
        #     continue
        if len(info) > 0:
            wordList.append(info)
            info = {}
        index += 1


def lexAnalyse(filePath):
    with open(filePath, 'r') as f:
        for line in f:
            buffer = line.rstrip('\n').strip(' ').split(' ')
            # print(buffer)
            line = 1
            for i in range(0, len(buffer)):
                # print(buffer[i])
                analyse(buffer[i], line)
                line += 1
    return wordList


# def lexAnaltest(s):
#     for line in s:
#         buffer = line.rstrip('\n').strip(' ').split(' ')
#         line = 1
#         for i in range(0, len(buffer)):
#             analyse(buffer[i], line)
#             line += 1
#     return wordList


if __name__ == '__main__':
    filePath = 'D:\\pythonProject\\LAB1.txt'
    wordList = lexAnalyse(filePath)
    # print(wordList)
    print("%s  %s  %s" % ('单词', '类型', '行数'))
    for i in wordList:
        print(" %s   %s   %s" % (i['word'], i['type'], i["line"]))

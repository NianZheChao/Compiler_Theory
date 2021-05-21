wordList = []

key_word = {'char': 101, 'int': 102, 'double': 104, 'break': 105, 'return': 106,
            'void': 107, 'continue': 108, 'if': 109, 'main': 110, 'float': 111, 'else': 112, 'while': 113, 'for': 114,
            'printf': 115, 'scanf': 116}
operator = {'!': 205, '*': 206, '/': 207, '%': 208, '+': 209, '-': 210, '<': 211, '>': 212, '&': 213, '|': 214,
            '=': 215, '.': 216}
delima = {'{': 301, '}': 302, ';': 303, ',': 304, '(': 305, ')': 306}


def readFile(path):
    src = []
    with open(path, 'r', encoding='UTF-8') as f:
        src = f.read().splitlines()
        # for i in f.readlines():
        #     if i != '\n':
        #         src.append(i)
    return src


def removeNote(src):
    for i in src:
        for j in range(len(i)):
            if i[j] == '/':
                if i[j + 1] == '/' or i[j + 1] == '*':
                    src[src.index(i)] = i[:j]
                    break
            break
    for i in src:
        if not i:
            del src[src.index(i)]
    return src


def combineProg(src):
    strSrc = ' '.join(str(i) for i in src)
    return strSrc


def addWord(word, type):
    global wordList
    if type == 'operation':
        wordList.append(operator[word])
        wordList.append(word)
        # w = '(' + operator[word] + ',\"' + word + '\"' + ')\n'
        # wordList = wordList + w
    elif type == 'keyWord':
        wordList.append(key_word[word])
        wordList.append(word)
    elif type == 'identifier':
        wordList.append(700)
        wordList.append(word)
    elif type == 'integer':
        wordList.append(400)
        wordList.append(word)
    elif type == 'delima':
        wordList.append(delima[word])
        wordList.append(word)


def lexAnalyse(str):
    i = 0
    j = 0
    exitFlag = 0
    while exitFlag == 0:
        if str[i] == ' ':
            i += 1
            j = i

        if str[j].isalpha() or str[j] == '_':
            # 识别保留字、标识符
            for j in range(i, len(str)):
                if str[j].isalpha() or str[j] == '_':
                    if j >= len(str) - 1:
                        word = str[i:j + 1]
                        if word in key_word:
                            addWord(word, 'keyWord')
                        else:
                            addWord(word, 'identifier')
                        exitFlag = 1
                        i = j + 1
                        j = i
                        break
                    continue
                elif j >= len(str):
                    word = str[i:j + 1]
                    if word in key_word:
                        addWord(word, 'keyWord')
                    else:
                        addWord(word, 'identifier')
                    exitFlag = 1
                    i = j + 1
                    j = i
                    break
                else:
                    word = str[i:j]
                    if word in key_word:
                        addWord(word, 'keyWord')
                    else:
                        addWord(word, 'identifier')
                    i = j
                    break
                    # 完成一个单词的识别 跳出for循环
            if exitFlag == 1:
                i = j
                break

        elif str[i].isdigit():
            # 识别整数
            for j in range(i, len(str)):
                if str[j].isdigit():
                    # 只能判断整数
                    if j >= len(str) - 1:
                        word = str[i:j + 1]
                        addWord(word, 'integer')
                        exitFlag = 1
                        i = j + 1
                        j = i
                        break
                    continue
                else:
                    word = str[i:j]
                    addWord(word, 'integer')
                    i = j
                    break
                    # 完成一个数字的识别 跳出for循环
            if exitFlag == 1:
                i = j
                break

        # 识别界符delima
        elif str[i] in delima:
            addWord(str[i], 'delima')
            i += 1
            j = i
            if i >= len(str):
                exitFlag = 1
                break

        # 识别运算符
        elif str[i] in operator:
            addWord(str[i], 'operation')
            i += 1
            j = i
            if i >= len(str):
                exitFlag = 1
                break

        if exitFlag == 1:
            break


if __name__ == '__main__':
    srcS = combineProg(removeNote(readFile('testProgram.txt')))
    print(srcS)
    lexAnalyse(srcS)
    print(wordList)
    # todo: 程序中出现转义字符无法跳出循环

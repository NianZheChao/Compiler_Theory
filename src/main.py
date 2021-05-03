import collections
import copy

import parse
import cifa


def parseToken(inputToken, grammar, terminalSymbols, nonTerminalSymbols, analyzeTable):
    parseStack = ['#']
    grammarTop = list(grammar.keys())[0]
    parseStack.append(grammarTop)

    i = 0
    f3 = open('analyze_process.txt', 'w')
    print("[ANALYSE PROCESS]", file=f3)
    while True:
        if i < len(inputToken):
            for key, value in inputToken[i].items():
                # global word
                # global type_
                word = key
                type_ = value
                # print(word)
                # print(type_)

            if parseStack[-1] in terminalSymbols and (word in terminalSymbols or type_ in terminalSymbols):
                if parseStack[-1] == '#' and word == '#':
                    print('匹配成功!', file=f3)
                    break
                elif (parseStack[-1] == word or parseStack[-1] == type_) and parseStack[-1] != '#':
                    parseStack.pop()
                    # k = i
                    i = i + 1
                    print(parseStack, word, file=f3)
                    # j = i
                    # if(k>0):
                    # k = k - 1
                    # for key,value in inputToken[j].items():
                    #   next_word=key
                    #   next_type_=value
                    # for key,value in inputToken[k].items():
                    #   pre_word=key
                    #   pre_type_=value
                    # if(type_=='id' and next_word=='('):
                    #   function_table.append({word:pre_word})
                    # if(type_=='id' and next_type_=='op' and pre_type_=='keyword'):
                    # h=j+1
                    # for key,value in inputToken[h].items():
                    #   next_word2=key
                    #   next_type_2=value
                    # if(next_type_2=='integer_constant'):
                    #   variable_table.append({word:[pre_word,next_word2]})

                else:
                    if type_ == 'end_of_file':
                        print("函数末尾处缺少 } ")
                        # parseStack.pop()
                        # i=i+1
                        break
                    elif type_ == 'delimiter':
                        if word == ';':
                            print(word + "处缺少 ; ")
                        elif word == '(':
                            print(word + "处缺少 ( ")
                        elif word == ')':
                            print(word + "处缺少 ) ")
                        # parseStack.pop()
                        # i+i+1
                        break
                    else:
                        print("其他错")
                        break

            elif parseStack[-1] in nonTerminalSymbols:
                row = analyzeTable[parseStack[-1]]
                # print("row:")
                # print(row)
                #   for node in PostOrderIter(tree):
                #     if node.name == parseStack[-1]:
                #       currentRoot = node
                #       break

                if word in row.keys():
                    rule = row[word]
                    # print("rule1:")
                    # print(rule)
                    parseStack.pop()
                    for item in reversed(rule):
                        if item != '$':
                            parseStack.append(item)
                    # for item in rule:
                    #   if item != '$':
                    #     Node(item, parent=currentRoot)
                    print(parseStack, word, rule, file=f3)

                elif type_ in row.keys():
                    rule = row[type_]
                    # print("rule2")
                    # print(rule)
                    parseStack.pop()
                    for item in reversed(rule):
                        if item != '$':
                            parseStack.append(item)
                    # for item in rule:
                    #   if item != '$':
                    #     Node(item, parent=currentRoot)
                    print(parseStack, word, rule, file=f3)

                else:
                    print(word + " 前出现缺失" + type_ + " 的错误")

                    break


def main():
    # 文法文件路径
    grammarFilePath = 'grammar.txt'

    # 1. 读入文法
    grammar = parse.readGrammar(grammarFilePath)

    # print('[Grammar]:')
    # for grammaritem in grammar.items():
    #     print(' ', grammaritem)

    # 2. 划分终结符与非终结符
    terminalSymbols, nonTerminalSymbols = parse.differentiateSymbols(grammar)
    # print('[Terminal Symbols]:\n ', terminalSymbols)
    # print('[Nonterminal Symbols]:\n ', nonTerminalSymbols)

    # 3-1. 递归求 FIRST 集
    grammarFirstSet = collections.defaultdict(list)
    grammarFirstSet = parse.getFIRST(grammarFirstSet, grammar, terminalSymbols, nonTerminalSymbols)
    while True:
        originalFirstSet = copy.deepcopy(grammarFirstSet)
        # 查看递归情况的 LOG
        # print(originalFirstSet)
        grammarFirstSet = parse.getFIRST(
            grammarFirstSet, grammar, terminalSymbols, nonTerminalSymbols)
        if grammarFirstSet == originalFirstSet:
            break
    f = open('firstset.txt', 'w')
    print('[FIRST SET]:', file=f)
    for item in grammarFirstSet.items():
        print(' ', item, file=f)

    # 3-2. 递归求 FOLLOW 集
    grammarTop = list(grammar.keys())[0]
    grammarFollowSet = collections.defaultdict(list, {grammarTop: ['#']})

    grammarFollowSet = parse.getFOLLOW(grammarFirstSet, grammarFollowSet, grammar, terminalSymbols, nonTerminalSymbols)
    while True:
        originalFollowSet = copy.deepcopy(grammarFollowSet)
        # print(originalFollowSet)
        grammarFollowSet = parse.getFOLLOW(
            grammarFirstSet, grammarFollowSet, grammar, terminalSymbols, nonTerminalSymbols)
        if grammarFollowSet == originalFollowSet:
            break
    print('[FOLLOW SET]:', file=f)
    for item in grammarFollowSet.items():
        print(' ', item, file=f)
    f.close()
    # 4. 创建 LL1 分析表
    analyzeTable = parse.createAnalyzeTable(
        grammar, terminalSymbols, nonTerminalSymbols, grammarFirstSet, grammarFollowSet)

    f1 = open('analyze_table.txt', 'w')
    print('[ANALYZE TABLE]:', file=f1)
    for item in analyzeTable.items():
        print(' ', item, file=f1)

    # filePath = 'test2.txt'
    # 词法分析
    # tokenList1 = cifa.lexAnalyse(filePath)
    # # print(tokenList1)
    # tokenList = []
    # for i in tokenList1:
    #     info = {}
    #     if (i['type'] == '标识符'):
    #         # print(i['type'])
    #         info = {i['word']: 'id'}
    #     elif (i['type'] == '运算符'):
    #         info = {i['word']: 'op'}
    #     elif (i['type'] == '界符'):
    #         info = {i['word']: 'delia'}
    #     elif (i['type'] == '关键字'):
    #         info = {i['word']: 'key_'}
    #     elif (i['type'] == '常量'):
    #         info = {i['word']: 'num'}
    #     tokenList.append(info)
    # info = {'#': 'end_of_file'}
    # tokenList.append(info)
    # print(tokenList)

    # 分析输入 Token 文件
    tokenList = [
        # {'int': 'keyword'}, {'main': 'identifier'}, {'(': 'delimiter'}, {')': 'delimiter'}, {'{': 'delimiter'},
        # {'int': 'keyword'}, {'a': 'identifier'}, {'=': 'unary_operator'}, {'1': 'integer_constant'}, {';': 'delimiter'},
        # {'float': 'keyword'}, {'b': 'identifier'}, {'=': 'unary_operator'}, {'5': 'integer_constant'}, {';': 'delimiter'},
        # {'while': 'keyword'}, {'(': 'delimiter'}, {')': 'delimiter'}, {'{': 'delimiter'},
        # {'if': 'keyword'}, {'(': 'delimiter'}, {'a': 'identifier'}, {')': 'delimiter'}, {'{': 'delimiter'},
        # {'a': 'identifier'}, {'=': 'unary_operator'}, {'0': 'integer_constant'}, {';': 'delimiter'}, {'}': 'delimiter'},
        # {'else': 'keyword'}, {'{': 'delimiter'}, {'a': 'identifier'}, {'=': 'unary_operator'}, {'1': 'integer_constant'}, {';': 'delimiter'}, {'}': 'delimiter'},
        # {'}': 'delimiter'}, {'}': 'delimiter'},

        {'int': 'keyword'}, {'main': 'identifier'}, {'(': ')'}, {')': ')'}, {'{': '{'},
        {'int': 'keyword'}, {'a': 'identifier'}, {'=': 'unary_operator'}, {'1': 'integer_constant'}, {';': ';'},
        {'float': 'keyword'}, {'b': 'identifier'}, {'=': 'unary_operator'}, {'5': 'integer_constant'},
        {';': ';'},
        {'while': 'keyword'}, {'(': '('}, {')': ')'}, {'{': '{'},
        {'if': 'keyword'}, {'(': '('}, {'a': 'identifier'}, {')': ')'}, {'{': '{'},
        {'a': 'identifier'}, {'=': 'unary_operator'}, {'0': 'integer_constant'}, {';': ';'}, {'}': '}'},
        {'else': 'keyword'}, {'{': '{'}, {'a': 'identifier'}, {'=': 'unary_operator'},
        {'1': 'integer_constant'}, {';': 'delimiter'}, {'}': '}'},
        {'}': '}'}, {'}': '}'},

        # #  {'b':'identifier'},
        #  {'=':'unary_operator'}, {'b':'identifier'},{'*':'unary_operator'},{'a':'identifier'},
        #  {'-':'unary_operator'},{'1':'integer_constant'}, #  {';':'delimiter'}, #   # {'1':'integer_constant'},
        #  {';':'delimiter'},{'a':'identifier'}, {'=':'unary_operator'},{'a':'identifier'},{'*':'unary_operator'},
        #  {'2':'integer_constant'},{';':'delimiter'}, # {'if':'keyword'},{'(':'delimiter'},{'a':'identifier'},
        #   # {')':'delimiter'}, #   # {'{':'delimiter'}, {'a':'identifier'},{'=':'unary_operator'},
        #   {'a':'identifier'},{'-':'unary_operator'},{'1':'integer_constant'}, {';':'delimiter'},
        #   # {'}':'delimiter'}, #   # {'double':'keyword'},{'add':'identifier'}, {'(':'delimiter'},
        #   {')':'delimiter'},{'{':'delimiter'},{'char':'keyword'}, #   # {'c':'identifier'}, {'=':'unary_operator'},
        #   {'1':'integer_constant'},{';':'delimiter'},{'}':'delimiter'}, #   # {'}':'delimiter'},
        # {'void': 'key_word'}, {'main': 'id'}, {'(': 'delima'}, {')': 'delima'}, {'{': 'delima'}, {'a': 'id'},
        # {'&&': 'unary_operator'}, {'b': 'id'}, {'>': 'unary_operator'}, {'c': 'id'}, {';': 'delima'}, {'}': 'delima'},
        {'#': 'end_of_file'}]
    # f3 = open('analyze_process.txt', 'w')
    # print("[ANALYSE PROCESS]",file=f3)
    parseToken(tokenList, grammar, terminalSymbols, nonTerminalSymbols, analyzeTable)
    # print("function_table:")
    # print(function_table)
    # print("variable_table:")
    # print(variable_table)
    # print("函数名"+"        "+"类型")
    # i=0
    # while(i<len(function_table)):
    #   for key,value in  function_table[i].items():
    #     print(" "+key+"         "+value)
    #     i=i+1
    # print("变量名"+"        "+"类型"+""+"        变量值")
    # i=0
    # while(i<len(variable_table)):
    #   for key,value in  variable_table[i].items():
    #     print(" "+key+"            "+value[0]+"        "+value[1])
    #     i=i+1


if __name__ == "__main__":
    main()

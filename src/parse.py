import collections
import copy


# 读取文法
def readGrammar(filePath):
    grammar = collections.defaultdict(list)
    with open(filePath, 'r') as f:
        # 按行读取，加入文法字典
        for line in f:
            preGrammar, postGrammar = line.rstrip('\n').split(
                '->')  # rstrip用于去除右边的\n字符; "split分裂" split()以括号内容为指定界切分字符串，以列表形式输出
            preGrammar = preGrammar.rstrip(' ')
            postGrammar = postGrammar.lstrip(' ').split('|')
            # print("ok")
            for eachPostGrammar in postGrammar:
                eachPostGrammar = eachPostGrammar.strip(' ').split(' ')  # strip() 移除首尾指定内容，默认移除空格
                grammar[preGrammar].append(eachPostGrammar)

    return grammar


# 区分终结符与非终结符
def differentiateSymbols(grammar):
    # 终结符
    terminalSymbols = []
    # 非终结符
    nonTerminalSymbols = []
    # 中间处理符号
    tempSymbols = []

    for eachPreGrammar in grammar:
        if eachPreGrammar not in nonTerminalSymbols:
            nonTerminalSymbols.append(eachPreGrammar)

        postGrammarList = grammar[eachPreGrammar]
        for eachPostGrammar in postGrammarList:
            for eachPostGrammarItem in eachPostGrammar:
                tempSymbols.append(eachPostGrammarItem)

    for eachTempSymbol in tempSymbols:
        if eachTempSymbol not in nonTerminalSymbols and eachTempSymbol not in terminalSymbols:
            terminalSymbols.append(eachTempSymbol)

    terminalSymbols.append('#')
    if '$' in terminalSymbols:
        terminalSymbols.remove('$')
    return terminalSymbols, nonTerminalSymbols


# 求first集
def getFIRST(firstSet, grammar, terminalSymbols, nonTerminalSymbols):
    for eachGrammar in grammar:
        for eachPostGrammar in grammar[eachGrammar]:
            # 例子中大写字母表示非终结符，小写字母表示终结符：
            # 1. 遇到了终结符、产生式右侧子式首符号是终结符，直接加入
            if eachPostGrammar[0] in terminalSymbols:
                if not eachPostGrammar[0] in firstSet[eachGrammar]:
                    firstSet[eachGrammar].append(eachPostGrammar[0])
            elif eachPostGrammar[0] == '$':
                if not eachPostGrammar[0] in firstSet[eachGrammar]:
                    firstSet[eachGrammar].append(eachPostGrammar[0])
            # 2. 产生式右侧子式首符号，递归（比如：A -> B C c）
            else:
                for eachPostGrammarItem in eachPostGrammar:
                    # 遇到终结符就可以停
                    if eachPostGrammarItem in terminalSymbols:
                        if not eachPostGrammarItem in firstSet[eachGrammar]:
                            firstSet[eachGrammar].append(eachPostGrammarItem)
                        break
                    # 遇到 First 集合中含有空串的还要继续
                    elif '$' in firstSet[eachPostGrammarItem]:
                        for item in firstSet[eachPostGrammarItem]:
                            if not item in firstSet[eachGrammar]:
                                firstSet[eachGrammar].append(item)
                    # 但是如果 First 集合没有空串就可以停下来
                    else:
                        for item in firstSet[eachPostGrammarItem]:
                            if not item in firstSet[eachGrammar]:
                                firstSet[eachGrammar].append(item)
                        break

    return firstSet


# 求follow集
def getFOLLOW(firstSet, followSet, grammar, terminalSymbols, nonTerminalSymbols):
    for eachGrammarStartSymbol in grammar.keys():
        for eachGrammar in grammar:
            for eachPostGrammar in grammar[eachGrammar]:
                if eachGrammarStartSymbol in eachPostGrammar:
                    index = eachPostGrammar.index(eachGrammarStartSymbol)
                    lastItemIndex = len(eachPostGrammar) - 1
                    # 1. 产生式形如：S->aX，将集合 Follow(S) 中的所有元素加入 Follow(X) 中
                    if index == lastItemIndex:
                        for item in followSet[eachGrammar]:
                            if not item in followSet[eachGrammarStartSymbol]:
                                followSet[eachGrammarStartSymbol].append(item)
                    # 2. 产生式形如：S->aXb
                    else:
                        # 2.1 b 为终结符：将 b 加入 Follow(X) 中
                        if eachPostGrammar[index + 1] in terminalSymbols:
                            if not eachPostGrammar[index + 1] in followSet[eachGrammarStartSymbol]:
                                followSet[eachGrammarStartSymbol].append(
                                    eachPostGrammar[index + 1])
                        # 2.2 b 为非终结符
                        else:
                            # 从 b 开始往后扫描
                            for i in range(index + 1, lastItemIndex + 1):
                                # 遇到终结符就可以停下来
                                if eachPostGrammar[i] in terminalSymbols:
                                    if not eachPostGrammar[i] in followSet[eachGrammarStartSymbol]:
                                        followSet[eachGrammarStartSymbol].append(
                                            eachPostGrammar[i])
                                    break
                                # 要看看 First 集合里面有没有空串，有的话就可以加入 Follow
                                elif '$' in firstSet[eachPostGrammar[i]]:
                                    for item in firstSet[eachPostGrammar[i]]:
                                        if not item in followSet[eachGrammarStartSymbol] and item != '$':
                                            followSet[eachGrammarStartSymbol].append(item)
                                    # 如果扫描到最后一项，First 集合里面还有空串，就要把集合 Follow(S) 中的所有元素加入 Follow(X) 中
                                    if i == lastItemIndex:
                                        for item in followSet[eachGrammar]:
                                            if not item in followSet[eachGrammarStartSymbol]:
                                                followSet[eachGrammarStartSymbol].append(item)
                                # 如果没有空串，把这一项的 First 集合里除了空串以为的内容加入 Follow 集合就可以停下来
                                else:
                                    for item in firstSet[eachPostGrammar[i]]:
                                        if not item in followSet[eachGrammarStartSymbol] and item != '$':
                                            followSet[eachGrammarStartSymbol].append(item)
                                    break

    return followSet


# 求预测分析表
def getRuleFirstSet(preRule, postRule, terminalSymbols, nonTerminalSymbols, firstSet):
    ruleFirstSet = []
    for eachRule in postRule:
        # 1. 遇到了终结符、产生式右侧子式首符号是终结符，直接加入
        if eachRule in terminalSymbols:
            if not eachRule in ruleFirstSet:
                ruleFirstSet.append(eachRule)
            break
        elif eachRule == '$':
            if not eachRule in ruleFirstSet:
                ruleFirstSet.append(eachRule)
            break
        # 2. 产生式右侧子式首符号，递归
        else:
            # 遇到终结符就可以停
            if eachRule in terminalSymbols:
                if not eachRule in ruleFirstSet:
                    ruleFirstSet.append(eachRule)
                break
            # 遇到 First 集合中含有空串的还要继续
            elif '$' in firstSet[eachRule]:
                for item in firstSet[eachRule]:
                    if not item in ruleFirstSet:
                        ruleFirstSet.append(item)
            # 但是如果 First 集合没有空串就可以停下来
            else:
                for item in firstSet[eachRule]:
                    if not item in ruleFirstSet:
                        ruleFirstSet.append(item)
                break
    return ruleFirstSet


def createAnalyzeTable(grammar, terminalSymbols, nonTerminalSymbols, firstSet, followSet):
    analyzeTable = collections.defaultdict(dict)

    # 对每个文法的生成式 A -> γ
    for eachGrammar in grammar:
        for eachPostGrammar in grammar[eachGrammar]:
            # 先求一个 First(γ)
            postGrammarFirstSet = getRuleFirstSet(
                eachGrammar, eachPostGrammar, terminalSymbols, nonTerminalSymbols, firstSet)
            # print(eachPostGrammar, postGrammarFirstSet)

            # 1. 对每个终结符：
            for eachTerminalSymbol in terminalSymbols:
                # 如果终结符在 First(γ) 里面，那么就加入 LL1 分析表
                if eachTerminalSymbol in postGrammarFirstSet:
                    analyzeTable[eachGrammar].update(
                        {eachTerminalSymbol: eachPostGrammar})
            # 2. 如果 First(γ) 中含有空串，那么就把所有在 Follow(A) 集合中的终结符加入 LL1 分析表
            if '$' in postGrammarFirstSet:
                for eachTerminalSymbol in terminalSymbols:
                    if eachTerminalSymbol in followSet[eachGrammar]:
                        analyzeTable[eachGrammar].update(
                            {eachTerminalSymbol: eachPostGrammar})

    return analyzeTable

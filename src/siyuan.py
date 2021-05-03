already = ['a','b','c','x']
four = [[0 for i in range(4)] for i in range(11)]

def expresion2(tokenlist,i,j):
    state = 0
    error = 0
    t = []
    opers = []
    while state != 6:
        tt = 't' + str(j)
        if state == 0:
            if tokenlist[i].isalpha() and tokenlist[i] in already:
                if tokenlist[i] in already:
                    ki = tokenlist[i]
            state = 1
            i += 1
        elif state == 1:
            if tokenlist[i] == '=':
                pass
            state = 2
            i += 1
        elif state == 2:
            if (tokenlist[i] in already) or tokenlist[i].isdigit():
                if tokenlist[i+1] not in ['+','-']:
                    four[j][1] = tokenlist[i]
                pass
            state = 3
            i += 1
        elif state == 3:
            if tokenlist[i] in ['+', '-', '*', '/']:
                if tokenlist[i] in ['+', '-']:
                    opers.append(tokenlist[i])
                    t.append(tokenlist[i-1])
                else:
                    four[j][0] = tokenlist[i]
            state = 4
            i += 1
        elif state == 4:
            if (tokenlist[i] in already) or tokenlist[i].isdigit():
                if tokenlist[i+1] in ['*','/'] and (tokenlist[i-1] not in ['*','/']):
                    i -= 1
                    state = 2
                else:
                    if tokenlist[i-1] in ['+','-']:
                        t.append(tokenlist[i])
                    else:
                        four[j][2] = tokenlist[i]
                    state = 5
            elif tokenlist[i] == '(':
                state = 4
            i += 1
        elif state == 5:
            if tokenlist[i] == ';':
                state = 6
                if tokenlist[i-2] in ['*','/']:
                    four[j][3] = tt
                    t.append(tt)
                    j += 1
                # print(t)
                # print(opers)
                while len(t)>1:
                    four[j][0] = opers[0]
                    four[j][1] = t[0]
                    four[j][2] = t[1]
                    four[j][3] = 't'+ str(j)
                    opers.remove(opers[0])
                    t.remove(t[0])
                    t.remove(t[0])
                    t.append('t'+ str(j))
                    j += 1
                four[j][0] = '='
                four[j][1] = t[0]
                four[j][2] = ' '
                four[j][3] = ki
                pass
            elif tokenlist[i] in ['+', '-', '*', '/']:
                four[j][3] = tt
                t.append(tt)
                # print(t)
                j += 1
                if tokenlist[i] in ['+', '-']:
                    opers.append(tokenlist[i])
                else:
                    four[j][0] = tokenlist[i]
                if (tokenlist[i] in ['*','/'] and tokenlist[i+2] in ['*','/']):
                    four[j][1] = tt
                    t.remove(tt)
                elif (tokenlist[i] in ['*','/'] and tokenlist[i-2] in ['*','/']):
                    four[j][1] = tt
                    t.remove(tt)
                state = 4
            i += 1
    j += 1
    return i,j


if __name__ == '__main__':
    demo3= [ 'x','=', 'a', '+', 'b', '*', '6', '/', 'c', ';']
    j = 0
    i = 0
    print(str(demo3))
    while i<len(demo3):
        (i, j) = expresion2(demo3,i,j)
        i += 1
    m = 0
    for kk in four:
        print(m, ' ', kk)
        m += 1
                





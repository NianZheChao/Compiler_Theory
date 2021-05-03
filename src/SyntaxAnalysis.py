global string
global ERR
global i
string = '(i*9)'
ERR = 0
i = 0


def error():
    print(error)


def main():
    global string
    global ERR
    global i
    string = string.ljust(len(string) + 1, '#')
    print(string)
    E()
    if string[i] == '#':
        print('success')
    else:
        print('ERROR')
    return 0


def E():
    global ERR
    if ERR == 0:
        T()
        E1()


def T():
    global ERR
    if ERR == 0:
        F()
        T1()


def E1():
    global string
    global ERR
    global i
    if ERR == 0:
        if string[i] == '+':
            i = i + 1
            T()
            E1()
        elif string[i] != '#' and string[i] != ')':
            print('fail')
            ERR = 1


def T1():
    global string
    global ERR
    global i
    if ERR == 0:
        if string[i] == '*':
            i = i + 1
            F()
            T1()
        elif (string[i] != '#' and string[i] != ')') and string[i] != '+':
            print('fail')
            ERR = 1


def F():
    global string
    global ERR
    global i
    if ERR == 0:
        if string[i] == '(':
            i = i + 1
            E()
            if string[i] == ')':
                i = i + 1
            elif string[i] == '#':
                print('fail')
                ERR = 1
                i = i + 1
        elif string[i] == 'i' or string[i].isdigit():
            i = i + 1
        else:
            print('fail')
            ERR = 1


if __name__ == '__main__':
    main()

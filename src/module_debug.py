def get_token(seed, src):
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
    print('error('+str(error)+')  warring(0)')
    k = [token, token_word, token_num, token_word_row, token_num_row]
    return k

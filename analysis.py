"""
词法分析-单词识别
"""
import pandas


# 判断字符是否为字母
def is_letter(ch):
    if 'z' >= ch >= 'a' or 'Z' >= ch >= 'A':
        return True
    return False


# 判断字符是否为数字
def is_digit(ch):
    if '0' <= ch <= '9':
        return True
    return False


# 识别标识符/关键字
def get_identifier(string: str, index: int):
    status = 0
    idf = ''
    while index < len(string):
        if status == 0:
            if is_letter(string[index]) or string[index] == '_':
                idf += string[index]
                status = 1
            else:
                status = 2
        elif status == 1:
            if is_letter(string[index]) or is_digit(string[index]) or string[index] == '_':
                idf += string[index]
                status = 1
            else:
                status = 2
        else:
            if idf != '':
                return idf
            else:
                status = 0
        index += 1


# 识别整数
def get_number(string, index):
    status = 0
    number = ''
    while index < len(string):
        if status == 0:
            if string[index] == '0':
                status = 3
                number += string[index]
            elif '1' <= string[index] <= '9':
                status = 1
                number += string[index]
        elif status == 1:
            if is_digit(string[index]):
                status = 1
                number += string[index]
            else:
                status = 2
        elif status == 2:
            return number
        elif status == 3:
            if '0' <= string[index] <= '7':
                status = 3
                number += string[index]
            elif string[index] == 'x' or string[index] == 'X':
                number += string[index]
                status = 5
            else:
                status = 4
        elif status == 4:
            return number

        elif status == 5:
            if is_digit(string[index]) or 'a' <= string[index] <= 'f' or 'A' <= string[index] <= 'F':
                status = 6
                number += string[index]
        elif status == 6:
            if is_digit(string[index]) or 'a' <= string[index] <= 'f' or 'A' <= string[index] <= 'F':
                status = 6
                number += string[index]
            else:
                status = 7
        else:
            return number
        index += 1


# 识别注释
def get_notes(string: str, i: int):
    status = 0
    notes = ''
    while i < len(string):
        if status == 0:
            if string[i] == '/':
                status = 1
                notes += string[i]
            else:
                status = 5
        elif status == 1:
            if string[i] == '/':
                status = 2
                notes += string[i]
            elif string[i] == '*':
                status = 3
                notes += string[i]
        elif status == 2:
            if string[i] == '\n':
                status = 5
                notes += string[i]
            else:
                status = 2
                notes += string[i]
        elif status == 3:
            if string[i] == '*':
                status = 4
                notes += string[i]
            else:
                status = 3
                notes += string[i]
        elif status == 4:
            if string[i] == '/':
                status = 5
                notes += string[i]
            else:
                status = 3
                notes += string[i]
        else:
            return notes
        i += 1


# 错误识别
def get_mistake():
    pass


# 单词识别
def analysis_word(code):
    key = pandas.read_json('Sample.json')
    i = 0
    output = []
    error = []
    while i < len(code):

        if code[i] not in ['\n', '\t', ' ', '']:
            if is_letter(code[i]) or code[i] == '_':
                temp = get_identifier(code, i)
                i += len(temp)
                if key.get(temp) is not None:
                    print('关键字', (temp, key.get(temp)[0]))
                    output.append((temp, key.get(temp)[0]))
                else:
                    print('标识符', (temp, key.get('标识符')[0]))
                    output.append((temp, key.get('标识符')[0]))
                continue
            elif is_digit(code[i]):
                temp = get_number(code, i)
                i += len(temp)
                print('整数', (temp, key.get('整数')[0]))
                output.append((temp, key.get('整数')[0]))
                continue
            elif code[i] == '/':
                temp = get_notes(code, i)
                i += len(temp)
                print("注释", temp)
                continue
            else:
                if key.get(code[i]) is not None:
                    print((code[i], key.get(code[i])[0]))
                    output.append((code[i], key.get(code[i])[0]))
                else:
                    print(f'不能识别{code[i]}')
                    error.append(code[i])
        i += 1
    return output, error

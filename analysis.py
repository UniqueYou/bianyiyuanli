"""
词法分析-单词识别
"""
import pandas
from main import get_code

digit_split = ['+', '-', '>', '<', '=', ';', ' ', '\n']  # 数字之间分隔符
identifier_split = ['+', '-', '=', '(', ')', '{', '}', ';', ' ', '\n']  # 标识符分割
other_split = [' ', '\t', '\n']


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
            break
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
            break

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
            break
        index += 1
    return number


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


def get_error(str, pre, next, temp, split_token):
    error = None
    output = None

    if next < len(str):  # 如果识别还没有到末尾
        if str[next] not in split_token:  # 如果下一个识别符与标识符之间没有分割，则这一串是错误的
            while next < len(str):  # 匹配错串
                if str[next] not in split_token:
                    next += 1
                else:
                    break
            error = str[pre:next]
        else:
            output = temp
    else:
        output = temp
    return error, output, next


# 单词识别
def analysis_word(code):
    key = pandas.read_json('Sample.json')
    i = 0
    output = []
    error = []
    while i < len(code):

        if code[i] in ['\n', '\t', ' ', '']:
            i += 1
            continue
        if is_digit(code[i]):  # 识别整数
            temp = get_number(code, i)  # 识别出来的数字
            next_i = i + len(temp)  # 指针指向下一个识别的字符
            errorT, outputT, next_i = get_error(str=code, pre=i, next=next_i, temp=temp, split_token=digit_split)
            i = next_i
            if errorT is not None:
                error.append(errorT)
            if outputT is not None:
                output.append(outputT)
        elif is_letter(code[i]):  # 识别标识符
            temp = get_identifier(code, i)
            next_i = i + len(temp)  # 指针指向下一个识别的字符
            errorT, outputT, next_i = get_error(str=code, pre=i, next=next_i, temp=temp, split_token=identifier_split)
            i = next_i
            if errorT is not None:
                error.append(errorT)
            if outputT is not None:
                output.append(outputT)
        else:
            errorT, outputT, next_i = get_error(str=code, pre=i, next=i, temp=[code[i]], split_token=identifier_split)
            i = next_i
            if errorT is not None:
                error.append(errorT)
            if outputT is not None:
                output.append(outputT)

    return output, error


if __name__ == '__main__':
    string = get_code('/home/song/PycharmProjects/bianyiyuanli/demo.cpp', encoding='utf-8')
    result, err = analysis_word(string)
    print(result)
    print(err)

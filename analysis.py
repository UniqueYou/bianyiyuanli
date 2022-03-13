"""
词法分析-单词识别
"""
from main import get_code
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


# 识别空白
# def is_space(string: str, index: int):
#     status = 0
#     space = ''
#     while index < len(string):
#         if status == 0:
#             if string[index] == "\\":
#                 status = 1
#                 space += string[index]
#             elif string[index] == ' ':
#                 status = 2
#                 space += string[index]
#             else:
#                 status = 2
#         elif status == 1:
#             if string[index] in ["t", "v", "f", "n", "r"]:
#                 space += string[index]
#                 status = 1
#             else:
#                 status = 2
#         else:
#             if space != '':
#                 return space
#         index += 1


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


def get_number(string, index):
    status = 0
    number = ''
    while index < len(string):
        if status == 0:
            if string[index] == '0':
                number += '0'
                status = 2
            elif '1' <= string[index] <= '9':
                status = 1
                number += string[index]
        elif status == 1:
            if is_digit(string[index]):
                number += string[index]
            else:
                status = 2
        else:
            if number != '':
                return number
            status = 0
        index += 1


def main():
    code = get_code(r'demo.cpp')
    key = pandas.read_json('Sample.json')
    i = 0
    while i < len(code):

        if code[i] not in ['\n', '\t', ' ', '']:
            if is_letter(code[i]) or code[i] == '_':
                temp = get_identifier(code, i)
                i += len(temp)
                if key.get(temp) is not None:
                    print('关键字', (temp, key.get(temp)[0]))
                else:
                    print('标识符', (temp, key.get('标识符')[0]))
                continue
            elif is_digit(code[i]):
                temp = get_number(code, i)
                i += len(temp)
                print('整数', (temp, key.get('整数')[0]))
                continue
            else:
                if key.get(code[i]) is not None:
                    print((code[i], key.get(code[i])[0]))
                else:
                    print(f'不能识别{code[i]}')
        i += 1


if __name__ == '__main__':
    main()

"""
词法分析-单词识别
"""
from main import get_code
import pandas

#

def get_identifier(string):
    identifier = []  # 保存标识符
    status = 0
    temp = ''
    for i in range(len(string)):
        if status == 0:
            if 'z' >= string[i] >= 'a' or 'Z' >= string[i] >= 'A' or string[i] == '_':
                temp += string[i]
                status = 1
            else:
                status = 2
        elif status == 1:
            if 'a' <= string[i] <= 'z' or 'A' <= string[i] <= 'Z' or '0' <= string[i] <= '9' or string[i] == '_':
                temp += string[i]
                status = 1

            else:
                status = 2
        else:
            if temp != '':
                print(temp)
                identifier.append(temp)
            status = 0
            temp = ''
    print(identifier)


def get_number(string):
    num = []  # 保存数字
    status = 0  # 状态码
    temp = ''
    for i in range(len(string)):
        if status == 0:
            if string[i] == '0':
                status = 2
            elif '1' <= string[i] <= '9':
                status = 1
                temp += string[i]
        elif status == 1:
            if '0' <= string[i] <= '9':
                temp += string[i]
            else:
                status = 2
        else:
            if temp != '':
                num.append(temp)
            status = 0
            temp = ''
    print(num)


def main():
    code = get_code(r'demo.cpp')
    get_number(code)
    get_identifier(code)


if __name__ == '__main__':
    # main()
    df = pandas.read_json('Sample.json')

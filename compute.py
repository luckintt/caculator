import re

op = ('+','-','*','/')

def inputFormat(expression):
    i = 0
    if expression.count('(') != expression.count(')'):  # 左右括号的数目不一致
        return False
    while i < len(expression):
        if i == 0:
            if expression[i].isdigit() == False and expression[i] != '(' and expression[i] != '-' and expression[i] != '+':   #首字母既不是数字也不是左括号，则输入非法
                return False
        elif i == len(expression)-1:
            if expression[i].isdigit() == False and expression[i] != ')':   #最后一个字母既不是数字也不是右括号，则输入非法
                return False
        elif expression[i] == '.':                   #是一个小数点或操作符
            if expression[i-1].isdigit() == False or expression[i+1].isdigit() == False:         #表达式的小数点前或后不是数字
                return False
        elif expression[i] == ' ':                                    #是一个空格
            pass
        elif expression[i].isdigit() == False and expression[i] != '(' and expression[i] != ')' and expression[i] not in op:  #既不是数字也不是括号，即是其他非法字符
            return False

        i += 1
    else:
        return True

def outputFormat(expression):
    expression = expression.strip()            #处理字符串前面和末尾的空格
    i = 0
    while i < len(expression):
        if expression[i] == ' ':       #处理空格
           expression = expression.replace(' ','')
        if expression[i] == '*' or expression[i] == '/':  #乘除后面直接跟负数
            if i < len(expression)-1 and expression[i+1] == '-':
                expression = ''.join([expression[:i+1], expression[i+2:]])
                k = i - 1
                while k >= 0:
                    if expression[k] == '-':
                        expression = ''.join([expression[:k], '+', expression[k + 1:]])
                        break
                    elif expression[k] == '+':
                        expression = ''.join([expression[:k], '-', expression[k + 1:]])
                        break
                    k -= 1
                else:
                    expression = ''.join([ '-', expression])
        i += 1
    if expression[0] == '+':
        expression = ''.join([ '', expression[1:]])
    expression = expression.replace('+-', '-')
    expression = expression.replace('++', '+')
    expression = expression.replace('--', '+')
    expression = expression.replace('-+', '-')
    # print('expression = ' + expression)
    return expression

def operator(ret_temp, index):
    temp1 = ''  # 操作符前面的数
    temp2 = ''  # 操作符后面的数
    j = index - 1
    while j >= 0 and ret_temp[j] not in op:  # 获取第一个操作数
        temp1 = ''.join([ret_temp[j], temp1])
        j -= 1
    if j >= 0 and ret_temp[j] == '-':
        temp1 = ''.join([ret_temp[j], temp1])
    k = index + 1
    # print('temp1=%s' % (temp1))
    while k < len(ret_temp) and ret_temp[k] not in op:  # 获取第二个操作数
        temp2 = ''.join([temp2, ret_temp[k]])
        k += 1
    # print('temp2=%s' % (temp2))
    # print(temp1 + ret_temp[index] + temp2)
    if ret_temp[index] == '*':
        temp = (float)(temp1) * (float)(temp2)
        ret_temp = ret_temp.replace(temp1 + ret_temp[index] + temp2, (str)(temp))
    elif ret_temp[index] == '/':
        temp = (float)(temp1) / (float)(temp2)
        ret_temp = ret_temp.replace(temp1 + ret_temp[index] + temp2, (str)(temp))
    elif ret_temp[index] == '+':
        temp = (float)(temp1) + (float)(temp2)
        ret_temp = ret_temp.replace(temp1 + ret_temp[index] + temp2, (str)(temp))
    else:
        temp = (float)(temp1) - (float)(temp2)
        ret_temp = ret_temp.replace(temp1 + ret_temp[index] + temp2, (str)(temp))
    # print('temp=%s' % (temp))
    return ret_temp

def calculate(ret_temp):
    i = 0
    while i < len(ret_temp):
        if ret_temp[i] == '*' or ret_temp[i] == '/':
            ret_temp = operator(ret_temp, i)
            ret_temp = outputFormat(ret_temp)  #对进行运算后的字符串进行格式化处理
            i = -1      #从头开始遍历表达式
        i += 1
    i = 1   #第一位为+ - 表示的是符号不是操作
    while i < len(ret_temp):
        if ret_temp[i] == '+' or ret_temp[i] == '-' :
            ret_temp = operator(ret_temp, i)
            ret_temp = outputFormat(ret_temp)
            i = 0
        i += 1
    return ret_temp

s = input('>>>:')
# s = '1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# s = '-12*-13-19'
tag = True  # 标志运算是否结束
if inputFormat(s):
    s = outputFormat(s)
    while tag:
        ret = re.search('\([^()]*\)',s)  #括号里面没有嵌套的括号
        if ret == None:   #没有内层括号，只有一个表达式
            ret_temp = s
            tag = False
        else:
            ret_temp = ''
            i = ret.span()[0] + 1
            while i < ret.span()[1] - 1:
                ret_temp = ''.join([ret_temp,s[i]])
                i += 1
        # print('ret_temp = ' + ret_temp)
        tmp = calculate(ret_temp)
        if tag:
            s = s.replace('('+ ret_temp + ')', str(tmp))
        else:
            s = s.replace(ret_temp, str(tmp))
        s = outputFormat(s)
    print(s)
else:
    print('输入的表达式格式错误')














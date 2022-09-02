import time
import random

def 生成器(位数1, 位数2, 操作符=None):
    if 操作符 == None or 操作符 == '':
        操作符 = random.choice(('+', '-', '*', '/'))
    
    操作数1 = random.randint(10 ** (位数1 - 1), 10 ** 位数1 - 1)
    操作数2 = random.randint(10 ** (位数2 - 1), 10 ** 位数2 - 1)
    
    表达式 = f'{操作数1}{操作符}{操作数2}'
    answer = eval(表达式)
    
    return (表达式, answer)

def main():
    位数1,操作符,位数2 = input('请输入位数1 操作符 位数2：').split(' ')
    位数1,位数2 = int(位数1),int(位数2)
    次数 = int(input('请输入你要练习的题目数：'))
    
    now = time.time()
    正确个数 = 0
    for _ in range(次数):
        表达式, answer = 生成器(位数1, 位数2, 操作符)
        your_answer = float(input(表达式 + '='))
        if your_answer == answer:
            print('正确')
            正确个数 += 1
        else:
            print(f'错误，正确答案为:{answer}')
    
    print(f'''
练习结束!
题目{次数}个，共花费{round(time.time()-now,3)}s
作对{正确个数}个，正确率{round(正确个数/次数*100,1)}%''')
    input()


if __name__ == '__main__':
    main()
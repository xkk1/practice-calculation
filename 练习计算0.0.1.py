import sys
import time
import random
import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import tkinter.scrolledtext


version = '0.0.1'
account_list = ['公用']
# account = '公用'
question_number_list = ['1', '2', '3', '4', '5', '10', '15', '20', '25', '30', '35',
                        '40', '45', '50', '55', '60', '65', '70', '75', '80', '85',
                        '90', '95', '100']
# 默认
question_form = (1, '+', 1)
question_number = 10
now_question_number = 0
right_question_number = 0
now_time = time.time()
answer = 0
order_of_units = 1


def generator(question_form):
    """generator 生成器
digit 位数
operator 操作符/运算符
operand 操作数;运算数;运算元;运算对象;作数
expression 表达式
"""
    digit1, operator, digit2 = question_form
    if operator == None or operator == '' or operator == '+-*/':
        operator = random.choice(('+', '-', '*', '/'))
    if operator == '+-':
        operator = random.choice(('+', '-'))
    if operator == '*/':
        operator = random.choice(('*', '/'))
    
    operand1 = random.randint(10 ** (digit1 - 1), 10 ** digit1 - 1)
    operand2 = random.randint(10 ** (digit2 - 1), 10 ** digit2 - 1)
    
    expression = f'{operand1}{operator}{operand2}'
    answer = eval(expression)
    
    return {'expression': expression, 'answer': answer}

def show_help():
    global help_window
    try:
        help_window.deiconify()
    except:
        help_information = '''“+-”是随机两数相加或相减
“*/”是随机两数相乘或相除
“+-*/”是随机两数相加或相减或相乘或相除'''
        # help_window = tk.Tk()
        help_window = tk.Toplevel(root)
        help_window.title(f'练习计算v{version}帮助信息')
        
        help_scrolledtext = tkinter.scrolledtext.ScrolledText(
            help_window,
            width=50,
            height=20,
            font=('宋体', 12)
            )  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        # scr.place(x=50, y=50) #滚动文本框在页面的位置
        help_scrolledtext.pack(fill=tk.BOTH, padx=5, pady=5)
        
        help_scrolledtext.insert(tk.INSERT, help_information)
        help_window.mainloop()

def show_practice_information():
    information = f'''练习结果:
模式：{question_form[0]}{question_form[1]}{question_form[2]} 精确到小数点后{order_of_units}位
总题数：{question_number}
正确个数：{right_question_number}
正确率：{round(right_question_number/(now_question_number-1)*100, 1)}%
耗时：{round(time.time()-now_time,3)}s （{round((time.time()-now_time)/question_number,3)}s/题）'''
    
    # information_window = tk.Tk()
    information_window = tk.Toplevel(root)
    information_window.title('练习结果')
    
    information_scrolledtext = tkinter.scrolledtext.ScrolledText(
        information_window,
        width=50,
        height=20,
        font=('宋体', 12)
        )  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
    # scr.place(x=50, y=50) #滚动文本框在页面的位置
    information_scrolledtext.pack(fill=tk.BOTH, padx=5, pady=5)
    
    information_scrolledtext.insert(tk.INSERT, information)
    information_window.mainloop()

def GUI():
    def start_practice():
        global question
        global question_form
        global question_number
        global now_question_number
        global right_question_number
        global order_of_units
        global now_time
        global answer
        question_form = (int(digit1_entry.get()), mode_button['text'], int(digit2_entry.get()))
        question_number = int(question_number_combobox.get())
        order_of_units = int(order_of_units_combobox.get())
        now_question_number = 1
        right_question_number = 0
        now_time =time.time()
        # 第一道题
        question = generator(question_form)
        question_label['text'] = question['expression'] + '='
        answer = round(question['answer'], order_of_units)
        # 目前做题统计初始化
        answer_status_label['text'] = f'(0)1/{question_number}  --%'
        
        
        # 恢复
        answer_status_label['state'] = tk.NORMAL
        question_label['state'] = tk.NORMAL
        answer_entry['state'] = tk.NORMAL
        number1_button['state'] = tk.NORMAL
        number2_button['state'] = tk.NORMAL
        number3_button['state'] = tk.NORMAL
        number4_button['state'] = tk.NORMAL
        number5_button['state'] = tk.NORMAL
        number6_button['state'] = tk.NORMAL
        number7_button['state'] = tk.NORMAL
        number8_button['state'] = tk.NORMAL
        number9_button['state'] = tk.NORMAL
        number0_button['state'] = tk.NORMAL
        next_question_button['state'] = tk.NORMAL
        delete_button['state'] = tk.NORMAL
        clear_button['state'] = tk.NORMAL
        point_button['state'] = tk.NORMAL
        minus_button['state'] = tk.NORMAL
        # finish_practice_button['state'] = tk.NORMAL
        # 禁用
        account_label['state'] = tk.DISABLED
        account_combobox['state'] = tk.DISABLED
        digit1_entry['state'] = tk.DISABLED
        digit1_label['state'] = tk.DISABLED
        mode_button['state'] = tk.DISABLED
        digit2_entry['state'] = tk.DISABLED
        question_number_label['state'] = tk.DISABLED
        question_number_combobox['state'] = tk.DISABLED
        #start_practice_button['state'] = tk.DISABLED
        order_of_units_combobox['state'] = tk.DISABLED
        order_of_units_label_1['state'] = tk.DISABLED
        order_of_units_label_2['state'] = tk.DISABLED
        
        start_finish_practice_button['text'] = '结束练习'
        before_answer_label['text'] = '请输入您计算的结果'
    
    def finish_practice():
        # 恢复
        account_label['state'] = tk.NORMAL
        account_combobox['state'] = tk.NORMAL
        digit1_entry['state'] = tk.NORMAL
        digit1_label['state'] = tk.NORMAL
        mode_button['state'] = tk.NORMAL
        digit2_entry['state'] = tk.NORMAL
        question_number_label['state'] = tk.NORMAL
        question_number_combobox['state'] = tk.NORMAL
        # start_practice_button['state'] = tk.NORMAL
        order_of_units_combobox['state'] = tk.NORMAL
        order_of_units_label_1['state'] = tk.NORMAL
        order_of_units_label_2['state'] = tk.NORMAL
        # 禁用
        answer_status_label['state'] = tk.DISABLED
        question_label['state'] = tk.DISABLED
        answer_entry['state'] = tk.DISABLED
        number1_button['state'] = tk.DISABLED
        number2_button['state'] = tk.DISABLED
        number3_button['state'] = tk.DISABLED
        number4_button['state'] = tk.DISABLED
        number5_button['state'] = tk.DISABLED
        number6_button['state'] = tk.DISABLED
        number7_button['state'] = tk.DISABLED
        number8_button['state'] = tk.DISABLED
        number9_button['state'] = tk.DISABLED
        number0_button['state'] = tk.DISABLED
        next_question_button['state'] = tk.DISABLED
        delete_button['state'] = tk.DISABLED
        clear_button['state'] = tk.DISABLED
        point_button['state'] = tk.DISABLED
        minus_button['state'] = tk.DISABLED
        # finish_practice_button['state'] = tk.DISABLED
        
        start_finish_practice_button['text'] = '开始练习'
        before_answer_label['text'] = '选好题目后请点击开始练习'
        before_answer_label['fg'] = 'orange'
        question_label['text'] = 'x+y='
        answer_status_label['text'] = '(正确数)目前数/总数  正确率'
    
    def start_finish_practice():
        if start_finish_practice_button['text'] == '开始练习':
            start_practice()
        else:
            finish_practice()
    
    def add_answer(string):
        answer_entry.insert(tk.INSERT, string)
    
    def delete():
        string = answer_entry.get()
        if len(string) != 0:
            answer_entry.delete(0, tk.END)
            answer_entry.insert(tk.INSERT, string[:-1])
    
    def clear():
        answer_entry.delete(0, tk.END)
    
    def change_mode():
        mode_list = ['+', '-', '*', '/', '+-', '*/', '+-*/']
        index = mode_list.index(mode_button['text'])
        if index == len(mode_list) - 1:
            index = 0
        else:
            index += 1
        mode_button['text'] = mode_list[index]
    
    def next_question():
        global question
        global answer
        global now_question_number
        global right_question_number
        
        your_answer = answer_entry.get() # 得到答案
        clear() # 清空答案
        now_question_number += 1
        try:
            if round(float(your_answer)) == answer:
                right_question_number += 1
                before_answer_label['text'] = f"正确,{question['expression']}={your_answer}"
                before_answer_label['fg'] = 'green'
            else:
                raise SyntaxError
        except:
            before_answer_label['text'] = f"错误,{question['expression']}≠{your_answer}  ={answer}"
            before_answer_label['fg'] = 'red'
        
        # 更新做题统计
        answer_status_label['text'] = f'({right_question_number}){now_question_number}/{question_number}\
  {round(right_question_number/(now_question_number-1)*100, 1)}%'
        
        if now_question_number - 1 != question_number:
            # 下一道题
            question = generator(question_form)
            question_label['text'] = question['expression'] + '='
            answer = round(question['answer'], order_of_units)
        else:
            # 做题结束
            finish_practice() # 结束练习
            show_practice_information() # 显示练习信息
            

    
    def answer_entry_function(event):
        # print(repr(event.char))
        if event.char == '\r' or event.char == ' ' or event.char == '\n':
            next_question()
            # print('next_question')
    
    global root
    root = tk.Tk()
    root.title(f'练习计算v{version}')
    root.resizable(0,0) # 禁止调节窗口大小
    
    root_frame = tk.Frame(root)
    root_frame.pack()
    
    first_frame = tk.Frame(root_frame)
    first_frame.pack()
    
    account_label = tk.Label(first_frame, text='账号:')
    account_label.pack(side=tk.LEFT)
    
    account_combobox = ttk.Combobox(first_frame, width=20)
    account_combobox['value'] = account_list # 设置下拉菜单中的值
    account_combobox.current(0) # 设置默认值，即默认下拉框中的内容
    account_combobox.pack(side=tk.LEFT)
    
    show_help_button = tk.Button(first_frame, text='帮助', command=show_help)
    show_help_button.pack(side=tk.RIGHT)
    
    statistics_button = tk.Button(first_frame, text='统计')
    statistics_button.pack(side=tk.RIGHT)
    
    # 位数框架
    digit_frame = tk.Frame(root_frame)
    digit_frame.pack()
    
    digit1_entry = tk.Entry(digit_frame, width=3)
    digit1_entry.insert(tk.INSERT, '1')
    digit1_entry.pack(side=tk.LEFT)
    
    digit1_label = tk.Label(digit_frame, text='位数')
    digit1_label.pack(side=tk.LEFT)
    
    mode_button = tk.Button(digit_frame, text='+', command=change_mode)
    mode_button.pack(side=tk.LEFT, padx=5)
    
    digit2_entry = tk.Entry(digit_frame, width=3)
    digit2_entry.insert(tk.INSERT, '1')
    digit2_entry.pack(side=tk.LEFT)
    
    digit2_label = tk.Label(digit_frame, text='位数')
    digit2_label.pack(side=tk.LEFT)
    
    # 精确到小数点
    order_of_units_frame = tk.Frame(root_frame)
    order_of_units_frame.pack()
    
    order_of_units_label_1 = tk.Label(order_of_units_frame, text='小数结果时精确到小数点后')
    order_of_units_label_1.pack(side=tk.LEFT)
    
    order_of_units_combobox = ttk.Combobox(order_of_units_frame, width=2)
    order_of_units_combobox['value'] = ['0', '1', '2','3', '4', '5', '6', '7', '8', '9', '10'] # 设置下拉菜单中的值
    order_of_units_combobox.current(1) # 设置默认值，即默认下拉框中的内容
    order_of_units_combobox.pack(side=tk.LEFT)
    
    order_of_units_label_2 = tk.Label(order_of_units_frame, text='位')
    order_of_units_label_2.pack(side=tk.LEFT)
    
    # 题目数框架
    question_number_frame = tk.Frame(root_frame)
    question_number_frame.pack()
    
    question_number_label = tk.Label(question_number_frame, text='题目数:')
    question_number_label.pack(side=tk.LEFT)
    
    question_number_combobox = ttk.Combobox(question_number_frame, width=6)
    question_number_combobox['value'] = question_number_list # 设置下拉菜单中的值
    question_number_combobox.current(5) # 设置默认值，即默认下拉框中的内容
    question_number_combobox.pack(side=tk.LEFT)
    
    start_finish_practice_button = tk.Button(question_number_frame,
                                      text='开始练习',
                                      command=start_finish_practice)
    start_finish_practice_button.pack(side=tk.LEFT, padx=10)
    
    answer_status_frame = tk.Frame(root_frame) # 应答状态
    answer_status_frame.pack()
    
    before_answer_label = tk.Label(answer_status_frame,
                                   text='选好题目后请点击开始练习',
                                   fg='orange')
    before_answer_label.pack()
    
    answer_status_label = tk.Label(answer_status_frame,
                                   text='(正确数)目前数/总数  正确率')
    answer_status_label.pack()
    
    # 问题
    question_frame = tk.Frame(root_frame)
    question_frame.pack()
    
    question_label = tk.Label(question_frame, text='x+y=')
    question_label.pack(side=tk.LEFT)
    
    answer_entry = tk.Entry(question_frame)
    answer_entry.bind("<Key>", answer_entry_function)
    #focus_set()方法是按键获取焦点，这个是按键类必须的。
    answer_entry.focus_set()
    answer_entry.pack(side=tk.LEFT)
    
    # 输入
    input_frame = tk.Frame(root_frame)
    input_frame.pack(padx=5, pady=5)
    
    number7_button = tk.Button(input_frame, text=' 7 ', command=lambda :add_answer('7'))
    number7_button.grid(row=0 ,column=0, padx=3, pady=3)
    
    number8_button = tk.Button(input_frame, text=' 8 ', command=lambda :add_answer('8'))
    number8_button.grid(row=0 ,column=1, padx=3, pady=3)
    
    number9_button = tk.Button(input_frame, text=' 9 ', command=lambda :add_answer('9'))
    number9_button.grid(row=0 ,column=2, padx=3, pady=3)
    
    number4_button = tk.Button(input_frame, text=' 4 ', command=lambda :add_answer('4'))
    number4_button.grid(row=1 ,column=0, padx=3, pady=3)
    
    number5_button = tk.Button(input_frame, text=' 5 ', command=lambda :add_answer('5'))
    number5_button.grid(row=1 ,column=1, padx=3, pady=3)
    
    number6_button = tk.Button(input_frame, text=' 6 ', command=lambda :add_answer('6'))
    number6_button.grid(row=1 ,column=2, padx=3, pady=3)
    
    next_question_button = tk.Button(input_frame, text='确定\n\n下一题', command=next_question)
    next_question_button.grid(row=0 ,column=3,rowspan=2, padx=3, pady=3, sticky=tk.N+tk.E+tk.W+tk.S)
    
    number1_button = tk.Button(input_frame, text=' 1 ', command=lambda :add_answer('1'))
    number1_button.grid(row=2 ,column=0, padx=3, pady=3)
    
    number2_button = tk.Button(input_frame, text=' 2 ', command=lambda :add_answer('2'))
    number2_button.grid(row=2 ,column=1, padx=3, pady=3)
    
    number3_button = tk.Button(input_frame, text=' 3 ', command=lambda :add_answer('3'))
    number3_button.grid(row=2 ,column=2, padx=3, pady=3)
    
    delete_button = tk.Button(input_frame, text='删除', command=delete)
    delete_button.grid(row=2 ,column=3, padx=3, pady=3, sticky=tk.E+tk.W)
    
    number0_button = tk.Button(input_frame, text=' 0 ', command=lambda :add_answer('0'))
    number0_button.grid(row=3 ,column=0, padx=3, pady=3)
    
    point_button = tk.Button(input_frame, text=' . ', command=lambda :add_answer('.'))
    point_button.grid(row=3 ,column=1, padx=3, pady=3)
    
    minus_button = tk.Button(input_frame, text=' - ', command=lambda :add_answer('-'))
    minus_button.grid(row=3 ,column=2, padx=3, pady=3)
    
    clear_button = tk.Button(input_frame, text='清空', command=clear)
    clear_button.grid(row=3 ,column=3, padx=3, pady=3, sticky=tk.E+tk.W)

    # finish_practice_button = tk.Button(input_frame,
    #                                    text='结束练习',
    #                                    command=finish_practice)
    # finish_practice_button.grid(row=3 ,column=4, padx=3, pady=3, sticky=tk.E+tk.W)
    
    answer_status_label['state'] = tk.DISABLED
    question_label['state'] = tk.DISABLED
    answer_entry['state'] = tk.DISABLED
    number1_button['state'] = tk.DISABLED
    number2_button['state'] = tk.DISABLED
    number3_button['state'] = tk.DISABLED
    number4_button['state'] = tk.DISABLED
    number5_button['state'] = tk.DISABLED
    number6_button['state'] = tk.DISABLED
    number7_button['state'] = tk.DISABLED
    number8_button['state'] = tk.DISABLED
    number9_button['state'] = tk.DISABLED
    number0_button['state'] = tk.DISABLED
    next_question_button['state'] = tk.DISABLED
    delete_button['state'] = tk.DISABLED
    clear_button['state'] = tk.DISABLED
    point_button['state'] = tk.DISABLED
    minus_button['state'] = tk.DISABLED
    # finish_practice_button['state'] = tk.DISABLED
    
    root.mainloop()

def old_generator(digit1, digit2, operator=None):
    """generator 生成器
digit 位数
operator 操作符/运算符
operand 操作数;运算数;运算元;运算对象;作数
expression 表达式
"""
    if operator == None or operator == '':
        operator = random.choice(('+', '-', '*', '/'))
    
    operand1 = random.randint(10 ** (digit1 - 1), 10 ** digit1 - 1)
    operand2 = random.randint(10 ** (digit2 - 1), 10 ** digit2 - 1)
    
    expression = f'{operand1}{operator}{operand2}'
    answer = eval(expression)
    
    return (expression, answer)

def old_main():
    digit1,operator,digit2 = input('请输入位数1 运算符 位数2：').split(' ')
    digit1,digit2 = int(digit1),int(digit2)
    number_of_times = int(input('请输入你要练习的题目数：')) # 次数
    
    now = time.time()
    correct_number = 0 # 正确个数
    for _ in range(number_of_times):
        expression, answer = old_generator(digit1, digit2, operator)
        your_answer = float(input(expression + '='))
        if your_answer == answer:
            print('正确')
            correct_number += 1
        else:
            print(f'错误，正确答案为:{answer}')
    
    print(f'''
练习结束!
题目{number_of_times}个，共花费{round(time.time()-now,3)}s
作对{correct_number}个，正确率{round(correct_number/number_of_times*100,1)}%''')
    input()

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'command':
            old_main()
    else:
        GUI()


if __name__ == '__main__':
    main()
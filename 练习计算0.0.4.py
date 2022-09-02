import sys
import time
import random
import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import tkinter.messagebox
import tkinter.scrolledtext
import os.path
import webbrowser


version = '0.0.4'
# account_list = ['公用']
data_file = f'练习计算{version}.pydata'
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
spend_time = 0.0
answer = 0
order_of_units = 1
# best = {} # '1+1 1 10':('公用', 9, 30) 账号 正确数 时间
data = {
'account_list': ['公用'],
'data': {}, # '账号': {} '1 + 1 1 10':(9, 30) 正确数 时间
'best': {} # # '1 + 1 1 10':('公用', 9, 30) 账号 正确数 时间
}
best_new_record = False 
personal_new_record = False # 个人新纪录


# undo=True
# expand=tk.YES, fill=tk.BOTH
class SetRightClickMenu:
    '''创建一个弹出菜单'''
    def __init__(self, text, undo=True):
        menu = tk.Menu(text,
                    tearoff=False,
                    )

        menu.add_command(label="剪切", command=lambda:text.event_generate('<<Cut>>'))
        menu.add_command(label="复制", command=lambda:text.event_generate('<<Copy>>'))
        menu.add_command(label="粘贴", command=lambda:text.event_generate('<<Paste>>'))
        menu.add_command(label="删除", command=lambda:text.event_generate('<<Clear>>'))
        if undo:
            menu.add_command(label="撤销", command=lambda:text.event_generate('<<Undo>>'))
            menu.add_command(label="重做", command=lambda:text.event_generate('<<Redo>>'))
        menu.add_separator()
        menu.add_command(label="个人网站", command=lambda:webbrowser.open("https://xkk1.github.io/"))
        menu.add_command(label="哔哩哔哩", command=lambda:webbrowser.open("https://space.bilibili.com/513689605"))

        def popup(event):
            menu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单

        text.bind("<Button-3>", popup)


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

def read_data():
    if os.path.isfile(data_file):
        with open(data_file, mode='r', encoding='utf-8') as f:
            new_data = eval(f.read())
        global data
        data = new_data

def save_data():
    with open(data_file, mode='w', encoding='utf-8') as f:
        f.write(repr(data))

def update_data():
    global data
    global best_new_record
    global personal_new_record
    best_new_record = False
    personal_new_record = False
    # 个人信息更新
    """now_question_detail = f'{question_form[0]}位数{question_form[1]}{question_form[2]}位数、\
精确到小数点后{order_of_units}位、题目数{question_number}'"""
    now_question_detail = f'{question_form[0]} {question_form[1]} {question_form[2]} \
{order_of_units} {question_number}'
    account_information = data['data'].get(account_combobox.get())
    if account_information == None:
        data['data'].setdefault(account_combobox.get(), {now_question_detail: (right_question_number, spend_time)})
        personal_new_record = True
    else:
        question_information = account_information.get(now_question_detail)
        if question_information == None:
            data['data'][account_combobox.get()].setdefault(now_question_detail,(right_question_number, spend_time))
            personal_new_record = True
        else:
            if question_information[0] < right_question_number:
                # 对比正确数
                data['data'][account_combobox.get()][now_question_detail] = (right_question_number, spend_time)
                personal_new_record = True
            elif question_information[0] == right_question_number:
                if question_information[1] > spend_time:
                    # 对比时间
                    data['data'][account_combobox.get()][now_question_detail] = (right_question_number, spend_time)
                    personal_new_record = True
    # 排行榜更新
    question_information = data['best'].get(now_question_detail)
    if question_information == None:
        data['best'].setdefault(now_question_detail, (account_combobox.get(), right_question_number, spend_time))
        best_new_record = True
    else:
        if question_information[1] < right_question_number:
            data['best'][now_question_detail] = (account_combobox.get(), right_question_number, spend_time)
            best_new_record = True
        elif question_information[1] == right_question_number:
            if question_information[2] > spend_time:
                data['best'][now_question_detail] = (account_combobox.get(), right_question_number, spend_time)
                best_new_record = True

def show_help():
    global help_window
    try:
        help_window.deiconify()
    except:
        help_information = '''练习计算帮助信息

程序会记录账号下的同类型练习的最好成绩，默认账号为：公用
输入新账号并完成一次练习即可创建新账号
“统计”可显示某一账号、所有账号同类型练习的最好成绩
“帮助”可显示帮助信息
可练习的计算有：+加、-减、乘*、/除、+-加减随机、*/乘除随机、+-*/加减乘除随机
“位数”即练习时随机生成整数的位数
“小数结果时精确到小数点后  位”，字面意思，但值得注意的是若已经除尽则不用输后面的零
除法即使整除、精确小数点后0位也要有小数点：1/1=1.0
选好后点“开始练习”按钮即可开始练习
结果输入支持鼠标等点击按钮和键盘输入
键盘输完结果后按回车键即可切换到下一题
做完所有题目后程序会显示该次做题结果并保存最好做题结果
练习结果包括：账号、模式、总题数、正确个数、正确率、耗时等
若本次练习创造了新纪录也会有提示

有问题，找作者
 联系方式：
  邮箱：3434623263@qq.com
  QQ：3434623263
  哔哩哔哩(www.bilibili.com)：
    用户名：小喾苦
    UID：513689605
    空间：https://space.bilibili.com/513689605
  个人网站：
    Github Pages：https://xkk1.github.io/
    Gitee Pages：https://xkk2.gitee.io/

更新日志：
1. 文本框增加右键菜单
2. 更好看的统计信息
3. 更详细的帮助信息
4. 优化了用户体验
5 .修复了已知BUG

创作缘由：
本人高中数学考试中经常因计算失误导致失分，故做此以提升计算能力
'''
        # help_window = tk.Tk()
        help_window = tk.Toplevel(root)
        help_window.title(f'练习计算{version}帮助信息')
        
        help_scrolledtext = tkinter.scrolledtext.ScrolledText(
            help_window,
            width=50,
            height=20,
            # font=('宋体', 12),
            undo=True
            )  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        # scr.place(x=50, y=50) #滚动文本框在页面的位置
        help_scrolledtext.pack(expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)
        
        help_scrolledtext.insert(tk.INSERT, help_information)

        # 简单的加右键菜单
        SetRightClickMenu(help_scrolledtext)
        
        help_window.mainloop()

def show_practice_information():
    global best_new_record
    global personal_new_record
    information = f'''账号：{account_combobox.get()}
模式：{question_form[0]}位数{question_form[1]}{question_form[2]}位数 精确到小数点后{order_of_units}位
总题数：{question_number}
正确个数：{right_question_number}
正确率：{round(right_question_number/(now_question_number-1)*100, 1)}%
耗时：{spend_time}秒 （{round(spend_time/question_number,3)}题/秒）'''
    if personal_new_record:
        information += f"\n恭喜{account_combobox.get()}创造了个人新纪录"
    if best_new_record:
        information += f"\n恭喜{account_combobox.get()}创造了新纪录"
    # information_window = tk.Tk()
    information_window = tk.Toplevel(root)
    information_window.title('练习结果')
    information_window.resizable(0,0) # 禁止调节窗口大小
    """
    information_scrolledtext = tkinter.scrolledtext.ScrolledText(
        information_window,
        width=50,
        height=20,
        font=('宋体', 12),
        undo=True
        )  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
    # scr.place(x=50, y=50) #滚动文本框在页面的位置
    information_scrolledtext.pack(fill=tk.BOTH, padx=5, pady=5)

    # 简单的加右键菜单
    SetRightClickMenu(information_scrolledtext)
    
    information_scrolledtext.insert(tk.INSERT, information)
    """
    tk.Label(information_window, text="练习结果").pack(padx=5)
    information_label = tk.Label(information_window, text=information, justify=tk.LEFT)
    information_label.pack(padx=5, pady=5, expand=tk.YES, fill=tk.BOTH)
    information_window.mainloop()

def show_statistics_information():
    global statistics_window
    try:
        statistics_window.destroy()
    except:
        pass
    statistics_columns = ["账号","类型 精确位数 题目数", "正确数", "正确率", "耗时(秒)", "题/秒"]
    def get_statistics_information(account):
        # information = f'账号：{account}\n'
        account_information = data['data'].get(account)
        if account_information == None:
            # information += '暂无信息'
            statistics_data = [['暂无信息'] * 7]
        else:
            statistics_data = []
            for form in account_information:
                # information += f'类型:{form},正确个数:{account_information[form][0]},所用时间:{account_information[form][1]}s\n'
                list_form = form.split(" ")
                # format_form = f"{list_form[0]}位数{list_form[1]}{list_form[2]}位数、精确到小数点后{list_form[3]}位、题目数{list_form[4]}"
                # information += f"类型:{format_form},正确个数:{account_information[form][0]},所用时间:{account_information[form][1]}、{round(account_information[form][1]/int(list_form[4]), 3)}题/s\n"
                statistics_data.append([
                    account,
                    f"{list_form[0]}位数{list_form[1]}{list_form[2]}位数 小数点后{list_form[3]}位 题数{list_form[4]}",
                    account_information[form][0], f"{round(account_information[form][0]*100/int(list_form[4]), 1)}%", account_information[form][1],
                    round(account_information[form][1]/int(list_form[4]), 3)
                    ])
        # print(statistics_data)
        # return information
        return statistics_data
    
    # def set_statistics_information1(information):
    #     statistics_scrolledtext.delete(0.0, tk.END)
    #     statistics_scrolledtext.insert(tk.INSERT, information)

    def set_statistics_information(statistics_data):
        # del
        x=statistics_treeview.get_children()
        for item in x:
            statistics_treeview.delete(item)
        # statistics_data = [['公用', '1位数+1位数', '1', '2', 2, 7.677, 3.838], ['小喾苦', '1位数+1位数', '1', '1', 1, 13.854, 13.854], ['小喾苦', '1位数+1位数', '1', '3', 3, 26.973, 8.991]]
        for i in range(len(statistics_data)):
            statistics_treeview.insert('','end',values=statistics_data[i])

    
    def show_best():
        statistics_account_combobox.set("")
        # information = '历史最高\n'
        if data['best'] == {}:
            # information += '暂无信息'
            statistics_data = [['暂无信息'] * 7]
        else:
            statistics_data = []
            for form in data['best']:
                list_form = form.split(" ")
                # format_form = f"{list_form[0]}位数{list_form[1]}{list_form[2]}位数、精确到小数点后{list_form[3]}位、题目数{list_form[4]}"
                # information += f"账号:{data['best'][form][0]},类型:{format_form},正确数:{data['best'][form][1]},所用时间:{data['best'][form][2]}、{round(data['best'][form][2]/int(list_form[4]), 3)}题/s\n"
                statistics_data.append([
                    data['best'][form][0],
                    f"{list_form[0]}位数{list_form[1]}{list_form[2]}位数 小数点后{list_form[3]}位 题数{list_form[4]}",
                    data['best'][form][1], f"{round(data['best'][form][1]*100/int(list_form[4]), 1)}%", data['best'][form][2],
                    round(data['best'][form][2]/int(list_form[4]), 3)
                    ])
        # print(statistics_data)
        # set_statistics_information(information)
        set_statistics_information(statistics_data)
    
    # help_window = tk.Tk()
    statistics_window = tk.Toplevel(root)
    statistics_window.title(f'练习计算{version}统计信息')
    
    statistics_account_frame = tk.Frame(statistics_window)
    statistics_account_frame.pack()
    
    statistics_account_label = tk.Label(statistics_account_frame, text='账号:')
    statistics_account_label.pack(side=tk.LEFT)
    
    statistics_account_combobox = ttk.Combobox(statistics_account_frame, width=20)
    statistics_account_combobox['value'] = data['account_list'] # account_list # 设置下拉菜单中的值
    # statistics_account_combobox.current(0) # 设置默认值，即默认下拉框中的内容
    statistics_account_combobox.bind("<<ComboboxSelected>>",lambda event:set_statistics_information(get_statistics_information(statistics_account_combobox.get())))
    statistics_account_combobox.configure(state="readonly")#绑定事件,(下拉列表框被选中时，绑定go()函数)
    statistics_account_combobox.pack(side=tk.LEFT, fill=tk.X)
    
    show_best_button = tk.Button(statistics_account_frame, text='历史最高', command=show_best)
    show_best_button.pack(side=tk.RIGHT)
    """
    statistics_scrolledtext = tkinter.scrolledtext.ScrolledText(
        statistics_window,
        width=100,
        height=20,
        font=('宋体', 12),
        undo=True
        )  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
    # scr.place(x=50, y=50) #滚动文本框在页面的位置
    statistics_scrolledtext.pack(expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)

    # 简单的加右键菜单
    SetRightClickMenu(statistics_scrolledtext)
    """
    xscroll = ttk.Scrollbar(statistics_window, orient=tk.HORIZONTAL)
    yscroll = ttk.Scrollbar(statistics_window, orient=tk.VERTICAL)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    statistics_treeview = ttk.Treeview(
        master=statistics_window, # 父容器
        columns=statistics_columns, # 列标识符列表
        show='headings', # 隐藏
        style='Treeview', # 样式
        height=16, # 表格显示的行数
        #padding=(10,5,20,30),
        xscrollcommand=xscroll.set,     # x轴滚动条
        yscrollcommand=yscroll.set      # y轴滚动条
        )
    xscroll.config(command=statistics_treeview.xview)
    yscroll.config(command=statistics_treeview.yview)
    width = (85, 220, 45, 55, 85, 60)
    for i in range(len(statistics_columns)):
        statistics_treeview.column(column=statistics_columns[i],width=width[i],anchor=tk.CENTER, stretch=True)
        statistics_treeview.heading(column=statistics_columns[i],text=statistics_columns[i])
    statistics_treeview.pack(expand=tk.YES, fill=tk.BOTH)
    
    # set_statistics_information(get_statistics_information(data['account_list'][0]))
    show_best()
    #statistics_scrolledtext.insert(tk.INSERT, get_statistics_information(data['account_list'][0]))
    # set_statistics_information1()
    statistics_window.mainloop()

def GUI():
    read_data()
    # global account_list
    # account_list = list(data['data'].keys())
    # account_list.reverse() # 反转列表
    def start_practice():
        global question
        global question_form
        global question_number
        global now_question_number
        global right_question_number
        global order_of_units
        global now_time
        global answer
        global account_list
        # 更新账号下拉菜单中的值
        account = account_combobox.get()
        try:
            data['account_list'].remove(account)
        except:
            pass
        data['account_list'].insert(0, account)
        account_combobox['value'] = data['account_list'] # 更新下拉菜单中的值
        
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
            try:
                start_practice()
            except Exception as e:
                tkinter.messagebox.showerror('开始练习遇到错误','出错了！\n开始练习遇到错误\n请检查输入是否合法！')
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
            if round(float(your_answer), order_of_units) == answer:
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
  {round(right_question_number*100/(now_question_number-1), 1)}%'
        
        if now_question_number - 1 != question_number:
            # 下一道题
            question = generator(question_form)
            question_label['text'] = question['expression'] + '='
            answer = round(question['answer'], order_of_units)
        else:
            # 做题结束
            global spend_time
            spend_time = round(time.time() - now_time, 3) # 计算时间
            finish_practice() # 结束练习
            update_data() # 更新数据
            save_data()
            show_practice_information() # 显示练习信息
            

    
    def answer_entry_function(event):
        # print(repr(event.char))
        if event.char == '\r' or event.char == ' ' or event.char == '\n':
            next_question()
            # print('next_question')
    
    global root
    root = tk.Tk()
    root.title(f'练习计算{version}')
    root.resizable(0,0) # 禁止调节窗口大小
    
    root_frame = tk.Frame(root)
    root_frame.pack()
    
    first_frame = tk.Frame(root_frame)
    first_frame.pack()
    
    account_label = tk.Label(first_frame, text='账号:')
    account_label.pack(side=tk.LEFT)
    
    global account_combobox
    account_combobox = ttk.Combobox(first_frame, width=20)
    account_combobox['value'] = data['account_list'] # account_list # 设置下拉菜单中的值
    account_combobox.current(0) # 设置默认值，即默认下拉框中的内容
    SetRightClickMenu(account_combobox, undo=False)
    account_combobox.pack(side=tk.LEFT)

    # 简单的加右键菜单
    SetRightClickMenu(account_combobox, undo=False)
    
    show_help_button = tk.Button(first_frame, text='帮助', command=show_help)
    show_help_button.pack(side=tk.RIGHT)
    
    statistics_button = tk.Button(first_frame, text='统计', command=show_statistics_information)
    statistics_button.pack(side=tk.RIGHT)
    
    # 位数框架
    digit_frame = tk.Frame(root_frame)
    digit_frame.pack()
    
    # digit1_entry = tk.Entry(digit_frame, width=3)
    # digit1_entry.insert(tk.INSERT, '1')
    # SetRightClickMenu(digit1_entry, undo=False)
    digit1_entry = ttk.Combobox(digit_frame, width=2)
    digit1_entry['value'] = [str(i) for i in range(1, 100)]# ['1', '2','3', '4', '5', '6', '7', '8', '9', '10'] # 设置下拉菜单中的值
    digit1_entry.current(0) # 设置默认值，即默认下拉框中的内容
    SetRightClickMenu(digit1_entry, undo=False)
    digit1_entry.pack(side=tk.LEFT)
    
    digit1_label = tk.Label(digit_frame, text='位数')
    digit1_label.pack(side=tk.LEFT)
    
    mode_button = tk.Button(digit_frame, text='+', command=change_mode)
    mode_button.pack(side=tk.LEFT, padx=5)
    
    # digit2_entry = tk.Entry(digit_frame, width=3)
    # digit2_entry.insert(tk.INSERT, '1')
    # SetRightClickMenu(digit2_entry, undo=False)
    digit2_entry = ttk.Combobox(digit_frame, width=2)
    digit2_entry['value'] = [str(i) for i in range(1, 100)] # 设置下拉菜单中的值
    digit2_entry.current(0) # 设置默认值，即默认下拉框中的内容
    SetRightClickMenu(digit2_entry, undo=False)
    digit2_entry.pack(side=tk.LEFT)
    
    digit2_label = tk.Label(digit_frame, text='位数')
    digit2_label.pack(side=tk.LEFT)
    
    # 精确到小数点
    order_of_units_frame = tk.Frame(root_frame)
    order_of_units_frame.pack()
    
    order_of_units_label_1 = tk.Label(order_of_units_frame, text='小数结果时精确到小数点后')
    order_of_units_label_1.pack(side=tk.LEFT)
    
    order_of_units_combobox = ttk.Combobox(order_of_units_frame, state="readonly", width=2)
    order_of_units_combobox['value'] = [str(i) for i in range(16)] # ['0', '1', '2','3', '4', '5', '6', '7', '8', '9', '10'] # 设置下拉菜单中的值
    order_of_units_combobox.current(1) # 设置默认值，即默认下拉框中的内容
    # SetRightClickMenu(order_of_units_combobox, undo=False)
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
    SetRightClickMenu(question_number_combobox, undo=False)
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
    save_data()

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

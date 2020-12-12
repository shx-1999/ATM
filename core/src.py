# coding=utf-8
from interface import user, bank, shopping
from lib import common

user_data = {
    'name': None
    # 判断用户是否登入
}


def logout():
    '''
    退出.
    :return:
    '''
    user_data['name'] = None


def login():
    '''
    登入.
    :return:
    '''
    print('登录。。。')
    if user_data['name']:
        print('你已经登入过了')
    count = 0
    while True:
        name = input('请输入用户名>>:').strip()
        if name.lower() == 'q': break
        password = input('请输入密码>>:').strip()
        flag, msg = user.login_interface(name, password)
        if flag:
            user_data['name'] = name
            print(msg)
            break
        else:
            count += 1
            if count == 3:
                user.locked_interface(name)
                print('错误次数过多，已锁定')
            else:

                print(msg)


def register():
    '''
    注册.
    :return:
    '''
    print('注册。。。')
    if user_data['name']:
        print('你已经登入过了')
    while True:
        name = input('请输入用户名>>:').strip()
        if name.lower() == 'q': break
        password = input('请输入密码>>:').strip()
        password2 = input('再次输入密码>>:').strip()
        if password == password2:
            flag, msg = user.register_interface(name, password)
            if flag:
                print(msg)
                break
            else:
                print('用户已存在')
        else:
            print('两次密码不一致')




@common.login_auth
def check_balance():
    '''
    查看余额.
    :return:
    '''
    print('查看余额。。。')
    balance = bank.check_balance_interface(user_data['name'])
    print(balance)


@common.login_auth
def transfer():
    '''
    转账.
    :return:
    '''
    print('转账。。。')
    while True:
        to_name = input('输入转账的用户>>:').strip()
        balance = input('输入转账金额>>:').strip()
        if balance.isdigit():
            balance = int(balance)
            flag, msg = bank.transfer_interface(user_data['name'], to_name, balance)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('必须输入数字')


@common.login_auth
def repay():
    '''
    还款.
    :return:
    '''
    print('还款。。。')
    balance = input('请输入还款金额>>:').strip()
    if balance.isdigit():
        balance = int(balance)
        falg, msg = bank.repay_interface(user_data['name'], balance)
        if falg:
            print(msg)
        else:
            print(msg)
    else:
        print('必须输入数字')


@common.login_auth
def withdraw():
    '''
    取款.
    :return:
    '''
    print('取款。。。')
    balance = input('输入取款金额>>:').strip()
    if balance.isdigit():
        balance = int(balance)
        falg, msg = bank.withdraw_interface(user_data['name'], balance)
        if falg:
            print(msg)
        else:
            print(msg)
    else:
        print('必须输入数字')


@common.login_auth
def check_record():
    '''
    查看流水.
    :return:
    '''
    print('查看流水。。。')
    bankflow = bank.check_bankflow_interface(user_data['name'])
    for flow in bankflow:
        print(flow)


@common.login_auth
def shop():
    '''
    1 先循环打印出商品
    2 用户输入数字选择商品（判断是否是数字，判断输入的数字是否在范围内）
    3 取出商品名，商品价格
    4 判断用户余额是否大于商品价格
    5 余额大于商品价格时，判断此商品是否在购物车里
        5.1 在购物车里，个数加1
        5.1 不在购物车里，拼出字典放入（｛‘good’：｛‘price’：10，‘count’：1｝｝）
    6 用户余额减掉商品价格
    7 花费加上商品价格
    8 当输入 q时，购买商品
        8.1 消费为0 ，直接退出
        8.2 打印购物车
        8.3 接受用户输入，是否购买 当输入y，直接调购物接口实现购物
    :return:
    '''
    print('购物。。。')
    goods_list = [
        ['coffee', 10],
        ['chicken', 20],
        ['iphone', 8000],
        ['macPro', 15000],
        ['car', 100000]
    ]
    money = 0
    user_balance = bank.check_balance_interface(user_data['name'])
    shopping_cart = {}
    while True:
        for i, v in enumerate(goods_list):
            print(f'{i}: {v}')
        choice = input('请输入需要购买商品的编号(数字)(q退出)>>:').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice >= len(goods_list):
                print('商品不存在')
                continue
            shop_name = goods_list[choice][0]
            shop_price = goods_list[choice][1]
            if user_balance >= shop_price:
                if shop_name in shopping_cart:
                    shopping_cart[shop_name]['count'] += 1
                else:
                    shopping_cart[shop_name] = {'price': shop_price, 'count': 1}
                user_balance -= shop_price
                money += shop_price
                print(f'{shop_name}已加入购物车')
            else:
                print('余额不足')
                continue
        elif choice.lower() == 'q':
            if money == 0:
                break
            print(shopping_cart)
            user = input('是否购买Y/N>>:').strip()
            if user.lower() == 'y':
                falg, msg = shopping.shopping_interface(user_data['name'], money, shopping_cart)
                if falg:
                    print(msg)
                    break
                else:
                    print(msg)
                    break
            elif user.lower() == 'n':
                print('你什么都没有购买')
                break
            else:
                print('无选项')
                continue

        else:
            print('输入非法字符')


@common.login_auth
def check_shopping_cart():
    '''
    查看购物车.
    :return:
    '''
    print('查看购物车。。。')
    shoppingcart = shopping.check_shoppingcart(user_data['name'])
    if shoppingcart:
        print(shoppingcart)
    else:
        print('无商品')


func_dic = {
    '1': login,
    '2': register,
    '3': check_balance,
    '4': transfer,
    '5': repay,
    '6': withdraw,
    '7': check_record,
    '8': shop,
    '9': check_shopping_cart,
    '10': logout
}


def run():
    '''
    功能选择接口.
    :return:
    '''
    while True:
        print('''选择需要的功能：
1、登入
2、注册
3、查看余额
4、转账
5、还款
6、取款
7、查看流水
8、购物
9、查看购买商品
10、退出程序
''')
        choice = input('编号>>:').strip()
        if choice in func_dic:
            func_dic[choice]()

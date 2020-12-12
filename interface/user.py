from db import db_handler
from lib import common

user_logger = common.get_logger('user')


def login_interface(name, password):
    '''
    登入接口.
    :param name:用户名
    :param password: 用户密码
    :return:True,False
    '''
    user_dic = db_handler.select(name)
    if user_dic:  # {'name': 'song', 'password': '123'}
        if password == user_dic['password'] and not user_dic['locked']:
            user_logger.info('用户%s登入了账户' % name)
            return True, '登入成功'
        else:
            return False, '用户名密码错误或被锁定'
    else:
        return False, '用户不存在'


def register_interface(name, password, balance=15000):
    '''
    注册接口.
    :param name:用户名
    :param password: 密码
    :param balance: 确认密码
    :return:True,False
    '''
    user_dic = db_handler.select(name)
    if user_dic:
        return False, '用户已存在'
    else:
        user_dic = {'name': name, 'password': password, 'balance': balance,
                    'locked': False, 'bankflow': [], 'shoppingcart': {}}
        db_handler.save(user_dic)
        user_logger.info('用户%s注册成功' % name)
        return True, '注册成功'


def locked_interface(name):
    '''
    锁定接口.
    :param name:用户名
    :return:
    '''
    user_dic = db_handler.select(name)
    if user_dic:
        user_dic['locked'] = True
        db_handler.save(user_dic)


def un_locked_interface(name):
    '''
    解锁用户.
    :param name:用户名
    :return:
    '''
    user_dic = db_handler.select(name)
    if user_dic:
        user_dic['locked'] = False
        db_handler.save(user_dic)

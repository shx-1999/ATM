from db import db_handler
from interface import bank


def shopping_interface(name, money, shoppingcart):
    '''
    购物接口.
    :param name:用户名
    :param money: 消费金额
    :param shoppingcart: 购物车清单
    :return:True,False
    '''
    flag, msg = bank.consume_interface(name, money)
    if flag:
        user_dic = db_handler.select(name)
        user_dic['shoppingcart'] = shoppingcart
        db_handler.save(user_dic)
        return True, '购买成功'
    else:
        return False, '余额不足'


def check_shoppingcart(name):
    '''
    查看购物车接口.
    :param name: 用户名
    :return:user_dic['shoppingcart']
    '''
    user_dic = db_handler.select(name)

    return user_dic['shoppingcart']

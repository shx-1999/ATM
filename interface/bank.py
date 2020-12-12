from db import db_handler
from core import src
from lib import common

bank_logger = common.get_logger('bank')


def check_balance_interface(name):
    '''
    查询余额接口.
    :param name:账户名
    :return:balance
    '''
    user_dic = db_handler.select(name)
    balance = user_dic['balance']
    return balance


def transfer_interface(from_name, to_name, balance):
    '''
    转账接口.
    :param from_name:转账用户
    :param to_name: 收款用户
    :param balance: 转账金额
    :return:True,False
    '''
    if from_name == to_name:
        return False, '不能给自己转账'
    to_dic = db_handler.select(to_name)
    if to_dic:
        from_dic = db_handler.select(from_name)
        if from_dic['balance'] >= balance:
            to_dic['balance'] += balance
            from_dic['balance'] -= balance
            from_dic['bankflow'].append('你向%s转账%s元' % (to_name, balance))
            to_dic['bankflow'].append('你收到%s的转账%s元' % (from_name, balance))
            bank_logger.info('%s向%s转账%s元' % (from_name, to_name, balance))
            db_handler.save(from_dic)
            db_handler.save(to_dic)
            return True, '转账成功'
        else:
            return False, '余额不足'
    else:
        return False, '用户不存在'


def repay_interface(name, balance):
    '''
    还款接口.
    :param name: 还款用户
    :param balance: 还款金额
    :return:True,False
    '''
    user_dic = db_handler.select(name)
    if user_dic['balance'] >= balance:
        user_dic['balance'] -= balance
        user_dic['bankflow'].append('还款%s' % balance)
        bank_logger.info('%s还款了%s元' % (name, balance))
        db_handler.save(user_dic)
        return True, '还款成功'
    else:
        return False, '余额不足以还款'


def withdraw_interface(name, balance):
    '''
    取款接口.
    :param name: 取款用户
    :param balance: 取款金额
    :return:True,False
    '''
    user_dic = db_handler.select(name)
    if user_dic['balance'] >= balance * 1.05:  # 0.5%的手续费
        user_dic['balance'] -= balance * 1.05
        user_dic['bankflow'].append('取款%s,手续费%s' % (balance, balance * 0.05))
        bank_logger.info('你取款了%s元，手续费%s元' % (balance, balance * 0.05))
        db_handler.save(user_dic)
        return True, '取款成功，取出金额%s' % balance
    else:
        return False, '余额不足'


def consume_interface(name, money):
    '''
    消费接口.
    :param name: 消费用户
    :param money: 消费金额
    :return:True,False
    '''
    user_dic = db_handler.select(name)
    if user_dic['balance'] >= money:
        user_dic['balance'] -= money
        db_handler.save(user_dic)
        return True, '扣款成功'
    else:
        return False, '余额不足'


def check_bankflow_interface(name):
    '''
    银行流水.
    :param name: 账户名
    :return:user_bankflow
    '''
    user_dic = db_handler.select(name)
    user_bankflow = user_dic['bankflow']
    return user_bankflow

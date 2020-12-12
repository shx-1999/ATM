# coding=utf-8
import os
import json
from conf import setting


def save(user_dic):
    '''
    保存用户信息文件.
    :param user_dic: 用户信息
    :return:
    '''
    user_path = os.path.join(setting.BASE_DB, '%s.json' % user_dic['name'])
    with open(user_path, 'w', encoding='utf-8')as f:
        json.dump(user_dic, f)
        f.flush()


#
def select(name):
    """
   查询用户文件.
    :param name: str --> 用户名
    :return: None, user_dic
    """
    user_path = os.path.join(setting.BASE_DB, '%s.json' % name)
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf-8')as f:
            user_dic = json.load(f)
            return user_dic
    else:
        return None

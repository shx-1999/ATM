from core import src
import logging.config
from conf import setting


def login_auth(func):
    '''
    装饰器
    :param func: 函数名
    :return: wrapper
    '''

    def wrapper(*args, **kwargs):
        if not src.user_data['name']:
            src.login()
        else:
            return func(*args, **kwargs)

    return wrapper


def get_logger(name):
    '''
    盗用日志字典.
    :param name:日志名字
    :return:
    '''
    logging.config.dictConfig(setting.LOGGING_DIC)  # 使用这个日志字典
    logger = logging.getLogger('name')
    return logger


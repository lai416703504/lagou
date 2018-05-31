# -*- coding:utf-8 -*-

# 内置库
import re
import requests

# 项目内部库
from lagou.utils.util import *
from lagou.logger.LoggerHandler import Logger

# 日志中心
# logger = Logger(logger='login.py').get_logger()

# 请求对象
session = requests.session()

# 请求头信息
HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html?ts=1527748655696&serviceId=lagou&service=https%253A%252F%252Fwww.lagou.com%252F&action=login&signature=520506B19276E8AF83F8A8CE17467423',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}


def _get_password(pass_wd):
    """
    这里对密码进行了双重MD5加密 veennike 这个值是在main.html_aio_f95e644.js文件找到的
    :param pass_wd:
    :return:
    """

    pass_wd = string_to_md5(string=pass_wd)
    pass_wd = 'veenike' + pass_wd + 'veenike'
    pass_wd = string_to_md5(string=pass_wd)
    return pass_wd


def _get_token():
    forge_token = ""
    forge_code = ""
    login_page = "https://passport.lagou.com/login/login.html"
    data = session.get(login_page, headers=HEADERS)
    print(data.text)
    match_obj = re.match(r'.*X_Anti_Forge_Token = \'(.*?)\';.*X_Anti_Forge_Code = \'(\d+?)\'', data.text, re.DOTALL)
    if match_obj:
        forge_token = match_obj.group(1)
        forge_code = match_obj.group(2)
    return forge_token, forge_code


def login(user, pass_wd):
    x__anti__forge__token, x__anti__forge__code = _get_token()
    login_headers = HEADERS.copy()
    login_headers.update({
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': x__anti__forge__token,
        'X-Anti-Forge-Code': x__anti__forge__code
    })

    post_data = {
        'isValidate': 'true',
        'username': user,
        'password': _get_password(pass_wd),
        'request_form_verifyCode': '',
        'submit': '',
    }

    response = session.post('https://passport.lagou.com/login/login.json', data=post_data, headers=login_headers)
    # logger.info(response.text)


def get_cookies():
    return requests.utils.dict_from_cookiejar(session.cookies)

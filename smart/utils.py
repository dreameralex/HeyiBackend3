
import requests
import json
from django.conf import settings

def get_openid(code):
    appid = 'wx9b3b83c24c95cf33'
    app_secret = '97ab09b54a540e8d254088c6533416ad'
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={app_secret}&js_code={code}'
    try:
        response = requests.get(url)
        data = response.text
        print(data)

    except:
        raise Exception('请求失败')

    try:
        data_dict = json.loads(data)
    except:
        raise Exception('openid获取失败')
    return data_dict

from  itsdangerous import  URLSafeTimedSerializer
from  itsdangerous import  BadSignature



SECRET_KEY = 'django-insecure-tg0+wyt%egqbvers*2w$r@9n*mke8)-5p7yf@ruxzz5gmdig#6'
# //之后研究怎么从settings取
# 解密
def check_save_user_token(openid):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        token = serializer.loads(openid)
        # 加密时间
        # token = serializer.loads(token, max_age=expiration)
    except BadSignature:
        return None
    return token.get('openid')

# 加密
def generate_save_user_token(openid):
    # // 初始化序列对象
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    # // 调用dump进行加密
    data = {'openid': openid}
    token = serializer.dumps(data)
    return token

def get_access_token():
    appid = 'wx9b3b83c24c95cf33'
    app_secret = '97ab09b54a540e8d254088c6533416ad'
    # url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credentialappid='+ appid + '&secret=' + secret
    #
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={app_secret}'

    try:
        response = requests.get(url)
        data = response.text
        print(data)

    except:
        raise Exception('请求失败')

    try:
        data_dict = json.loads(data)
    except:
        raise Exception('access_token获取失败')
    return data_dict

def get_phonenumber(code,access_token):
    payload = {'code': code}
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }

    url = f'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}'

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.text
    except:
        raise Exception('wx请求失败')

    try:
        data_dict = json.loads(data)
    except:
        raise Exception('手机号获取失败')
    return data_dict


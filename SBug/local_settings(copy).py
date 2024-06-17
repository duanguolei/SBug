"""
code speace
@Time    : 2024/1/20 12:01
@Author  : 泪懿:dgl
@File    : local_settings.py
"""
import os.path

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

#短信服务
TENCENT_SMS_APP_ID="1400dsaas"
TENCENT_SMS_APP_KEY ="956d6f02bca43be7266c9cbb8"
TENCENT_SMS_SIGN="泪懿公众号"

# import django_redis
#redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "123456" # redis密码
        }
    },
    ##多个连接redis ,多台主机
    "master": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobar999ed" # redis密码
        }
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME":'django_demo',
        'USER':'root',
        "PASSWORD":'123456',
        "HOST":"127.0.0.1",
        "POST":3306,
    'CHARSET':'utf8',
    'COLLATION':'utf8_general_ci'

    }
}





# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
  # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
COS_SECRET_ID='AKIDX0MsdsdsadsadasdsRuOdhsfhg1SovoX8Wkok'
# 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
COS_SECRET_KEY='oNh4MsHZfXJzeBZpysdsdnjkdsjsfhsuidsoivqy'
COS_REGION= 'ap-chengdu'



import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#支付宝id
ALI_APPID='ifosjdfjsdijfsoiod'
ALI_GATEWAY='https://openapi-sandbox.dl.alipaydev.com/gateway.do'
AIL_PRI_KEY_PATH=os.path.join(BASE_DIR,'files/支付宝应用私钥.txt')
AIL_PUB_KEY_PATH=os.path.join(BASE_DIR,'files/支付宝应用公钥.txt')
AIL_NOTIFY_URL_PATH='http://127.0.0.1:8000/web/pay_notify/'
AIL_RETURN_URL_PATH='http://127.0.0.1:8000/web/pay_notify/'

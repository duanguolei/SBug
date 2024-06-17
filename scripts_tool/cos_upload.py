"""
code speace
@Time    : 2024/3/13 12:44
@Author  : 泪懿:dgl
@File    : cos_upload.py
"""
"""
code speace
@Time    : 2024/3/13 12:22
@Author  : 泪懿:dgl
@File    : cos_bulket.py
"""
import base
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
  # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
COS_SECRET_ID='SDSDSDSDfSDkJIOIOIIJIOmimomioohomshofepfhivlibyaibfewi'
# 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
COS_SECRET_KEY='dsDDS'
COS_REGION= 'ap-chengdu'
egion = 'ap-chengdu'      # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填



COS_CONFIG= CosConfig(Region=region, SecretId=COS_SECRET_ID, SecretKey=COS_SECRET_KEY, Token=token, Scheme=scheme)
COS_CLIENT= CosS3Client(COS_CONFIG)

response=COS_CLIENT.upload_file(
    Bucket='jiejieluoguo-1314084628',
   LocalFilePath=r"D:\Users\段国磊\Pictures\u=2970757646,2137003863&fm=253&fmt=auto&app=138&f=JPEG.jpg",
Key='p1.jpg'
)
print(response)
print(response['ETag'])
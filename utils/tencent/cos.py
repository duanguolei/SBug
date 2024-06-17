"""
code speace
@Time    : 2024/3/13 13:13
@Author  : 泪懿:dgl
@File    : cos.py
"""

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
from sts.sts import Sts
def create_bucket(buket,region=settings.COS_REGION):
    """

    :param buket:筒名称
    :param region: 筒区域
    :return:
    """
    COS_CONFIG = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY,
                      )
    COS_CLIENT = CosS3Client(COS_CONFIG)



    response = COS_CLIENT.create_bucket(
        Bucket=buket,
        ACL='public-read',
        )

    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    COS_CLIENT.put_bucket_cors(
        Bucket=buket,
        CORSConfiguration=cors_config
    )

def upload_bucket(buket,image,key,region=settings.COS_REGION):
    """

    :param buket:筒名称
    :param region: 筒区域
    :return:
    """
    COS_CONFIG = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY,
                      )
    COS_CLIENT = CosS3Client(COS_CONFIG)

    response = COS_CLIENT.upload_file_from_buffer(
        Bucket=buket,
        Body=image,
        Key=key
    )

    return f"https://{buket}.cos.{region}.myqcloud.com/{key}"

def delete_file(bucket,key,region=settings.COS_REGION,):

    COS_CONFIG = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY,
                      )
    COS_CLIENT = CosS3Client(COS_CONFIG)
    COS_CLIENT.delete_object(
        Bucket=bucket,
        Key=key
    )

def delete_file_list(bucket,key_list,region=settings.COS_REGION,):
    COS_CONFIG = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY,
                      )
    COS_CLIENT = CosS3Client(COS_CONFIG)
    ojects={
        'Quite':'true',
        'Object':key_list
    }
    COS_CLIENT.delete_objects(
        Bucket=bucket,
        Delete=ojects
    )


def create_cos_credential(bucket,region):
	# 生成一个临时凭证，并给前端返回
	# 1. 安装一个生成临时凭证python模块   pip install -U qcloud-python-sts
	# 2. 写代码

    config = {
        # 临时密钥有效时长，单位是秒（30分钟=1800秒）
        'duration_seconds': 120,
        # 固定密钥 id
        'secret_id':settings.COS_SECRET_ID,
        # 固定密钥 key
        'secret_key': settings.COS_SECRET_KEY,
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': "ap-chengdu",
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            'name/cos:PostObject',
            # 'name/cos:DeleteObject',
            # "name/cos:UploadPart",
            # "name/cos:UploadPartCopy",
            # "name/cos:CompleteMultipartUpload",
            # "name/cos:AbortMultipartUpload",
            "*",
        ],

    }

    sts = Sts(config)
    result_dict = sts.get_credential()
    return result_dict


def delete_bucket(bucket,region=settings.COS_REGION):
    COS_CONFIG = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY,
                           )
    COS_CLIENT = CosS3Client(COS_CONFIG)
    #找到同种所有文件
    while True:
        part_objects=COS_CLIENT.list_objects(bucket)
        contens=part_objects.get('Contents')
        if not contens:
            break

        ojects = {
            'Quite': 'true',
            'Object': [{'Key':item['Key']} for item in contens]
        }
        COS_CLIENT.delete_objects(
            Bucket=bucket,
            Delete=ojects
        )
        if part_objects['IsTruncated']=='false':
            break

    while True:
        part_uploads=COS_CLIENT.list_multipart_uploads(bucket)
        uploads = part_objects.get('Upload')
        if not uploads:
            break

        for item in uploads:
            COS_CLIENT.abort_multipart_upload(bucket,item['Key'],item['UploadId'])
        if part_objects['IsTruncated'] == 'false':
            break


    COS_CLIENT.delete_bucket(bucket)











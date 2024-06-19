# 轻量bug管理平台
> 平台一步一步学习项目，非原创，支持短信验证码登录注册，价格策略，支付宝沙盒，云短信，项目管理，概述，问题统计，cos文件管理,评论，wiki,邀请等功能。
>(主体大部分功能完成，小部分未完善)
> 
- 项目demo地址:http://www.mydgl.cn:8082/web, 账号 admin,密码 123456

## 部分项目简单展示
![image-20240617160859083](./images/img_0.png)
![img_1.png](./images/img_1.png)
![img_2.png](./images/img_2.png)
![img_3.png](./images/img_3.png)
![img_4.png](./images/img_4.png)
![img_5.png](./images/img_5.png)

## 运行
1.下载项目
```shell
git clone https://github.com/duanguolei/SBug.git
```

2.下载依赖
```shell
cd SBug
```
```shell
pip install -r requirements.txt
```

3.配置环境
> 见SBug/SBug/local_settings(copy).py文件，改名为local_settings.py，
> 并配置其中的数据库，支付宝，云短信，cos等信息，可上网查询相关配置

4.迁移数据库
```shell
python manage.py makemigrations

python manage.py migrate
```
5.初始化策略
```shell
python scripts_tool/create_price_policy.py

python scripts_tool/init_price_policy.py
```

6.运行
```shell
python manage.py runserver
```
访问: http://127.0.0.1:8000/web

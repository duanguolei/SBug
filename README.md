# ����bug����ƽ̨
> ƽ̨һ��һ��ѧϰ��Ŀ����ԭ����֧�ֶ�����֤���¼ע�ᣬ�۸���ԣ�֧����ɳ��֧������Ŀ��������������ͳ�ƣ�cos�ļ�����,���ۣ�wiki�ȹ���


## ������Ŀ��չʾ
![img.png](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)
![img_3.png](img_3.png)
![img_4.png](img_4.png)
![img_5.png](img_5.png)

## ����
1.������Ŀ
> git clone https://github.com/duanguolei/Sbug.git

2.��������
> cd Sbug

> pip install -r requirements.txt

3.���û���
> ��SBug/SBug/local_settings(copy).py�ļ�������Ϊlocal_settings.py��
> ���������е����ݿ⣬֧�������ƶ��ţ�cos����Ϣ����������ѯ�������

4.Ǩ�����ݿ�
> python manage.py migrate

> python manage.py makemigrations

> python manage.py migrate

5.��ʼ������
> python scripts_tool/create_price_policy.py

> python scripts_tool/init_price_policy.py

6.����


> python manage.py runserver

����: http://127.0.0.1:8000/web

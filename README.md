# acmanager-backend��װ�����̳�

###### ����  sumover@����

���̷̳�Ϊ���¼�������

1. ����Ļ���������ʹ��

2. ���⻷���Ĵ

3. ��������������ʹ��

***

### ����Ĺ�����ʹ��

�����㿴�����̵̳�ʱ��ͨ���������֪�������ȷʹ��git�Լ������ȷ�Ĺ������Ĵ����.�ڴ˲���׸��.

��������ؽ̳�:

[ʷ����ǳ���׶���Git�̳̣�](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

�������������̳�֮ǰ,��Ĭ����Ϊ�����Ѿ�����������Python���﷨֪ʶ,����pip�Ȱ������������˽�.

��������ؽ̳�:

[��ѩ���Python�̳�](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)

�ڼ����Ķ����̳�֮ǰ,���Ķ�����˵��:

�����ʹ�õ���windowsϵͳ,�ҽ�����������win10.win10�¿���ʹ��һ��linux��ϵͳ.������ѯwzhѧ��

���ʹ�õ�������ϵͳ,��ӭ��ϵ���̵̳�����   @sumover    ������������̽��

���������windows��ʹ��bash:[�����Windows 10��װ��ʹ��Linux��Bash shell](https://jingyan.baidu.com/article/e73e26c0be8b6624adb6a7ba.html)

������ļ�����ϰ�װ�����ݿ���MySQL,�ҽ������ڱ����̵� /acmanager/settings.py  ���޸����µĴ���

```python
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'acmanager',
        'USER': 'sumover',
        'PASSWORD': '2323180',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
�޸ĺ�����MySQL�д�����Ϊ acmanager   �����ݿ�

����,���еĻ�����������

***

### Python���⻷���Ĵ

�������Ǵ�PyCharm,���������ر�����һ�εĹ���,��ѡ��check   from version    control

Ȼ��ѱ�git�ֿ��URL����(�����fork���ҾͲ���˵��)

#### Python���⻷���Ĵ

������Ѿ���Ϥ��δ���һ��python�����⻷��,������

���û��,��鿴���������:

[�����pycharm�����python���⻷����](https://jingyan.baidu.com/article/48b558e3ffeb667f39c09a41.html)

####��ذ��İ�װ����

��PyCharm�д�requirement.txt Ȼ�����IDE����ʾ������ذ��İ�װ����.
�������Ҫһ��ʱ��.

***

### Django����������

��Edit configuration..

��ʱ������ûɶ�������,�Ѷ˿ںŸĳ�8008�Ϳ�����

PyCharm���Զ�ѡ�����⻷��

������,�鿴���

***

����,acmanager-backend�������Ļ����������.

~~�Ҿ�����д�Ĺ���ʽ��~~
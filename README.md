# acmanager-backend安装启动教程

###### 作者  sumover@张泽

本教程分为以下几个内容

1. 代码的基本管理与使用

2. 虚拟环境的搭建

3. 服务器的配置与使用

***

### 代码的管理与使用

相信你看到本教程的时候通常情况下是知道如何正确使用git以及如何正确的管理您的代码的.在此不多赘述.

仅给出相关教程:

[史上最浅显易懂的Git教程！](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

在您继续读本教程之前,我默认认为您是已经基本掌握了Python的语法知识,并对pip等包管理工具有所了解.

仅给出相关教程:

[廖雪峰的Python教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)

在继续阅读本教程之前,请阅读如下说明:

如果您使用的是windows系统,我建议您升级到win10.win10下可以使用一个linux子系统.详情咨询wzh学长

如果使用的是其他系统,欢迎联系本教程的作者   @sumover    进行深入灵魂的探讨

关于如何在windows下使用bash:[如何在Windows 10安装和使用Linux的Bash shell](https://jingyan.baidu.com/article/e73e26c0be8b6624adb6a7ba.html)

如果您的计算机上安装的数据库是MySQL,我建议您在本工程的 /acmanager/settings.py  中修改如下的代码

```python
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'acmanager',
        'USER': 'user name',#此处为您的用户名
        'PASSWORD': 'password',#此处为您的密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
修改后请在MySQL中创建名为 acmanager   的数据库

至此,所有的基础环境搭建完毕

***

### Python虚拟环境的搭建

首先我们打开PyCharm,如果可以请关闭您上一次的工程,并选择check   from version    control

然后把本git仓库的URL贴上(如果您fork了我就不多说了)

#### Python虚拟环境的搭建

如果您已经熟悉如何创建一个python的虚拟环境,请搭建之并跳过

如果没有,请查看下面的链接并按照链接中的步骤进行创建python虚拟环境的操作:

[如何在pycharm中添加python虚拟环境？](https://jingyan.baidu.com/article/48b558e3ffeb667f39c09a41.html)



####相关包的安装工作

在PyCharm中打开requirement.txt 然后根据IDE的提示进行相关包的安装工作.
这可能需要一段时间.

***

### Django服务器配置

在File | setting | Language & frameworks | Django 中

勾选Enable Django Support

选择Django project root: 为acmanager-backend

选择settings:为acmanager\settings.py

在安装好相关的所有包后.选择 Management script 为venv\Scripts\django-admin.py


打开Edit configuration..

这时候大概是没啥大问题的,把端口号改成8008就可以了

PyCharm会自动选择虚拟环境

点运行,查看结果

***

至此,acmanager-backend服务器的基础配置完成.

~~我觉得我写的够正式了~~
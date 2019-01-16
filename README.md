#这是一个教你怎么配ACManager的教程

######好像是sumover@zz写的

~~您配吗?您不配!~~

####然后首先是大体需要的东西

    1. 别告诉我你连pycharm都没有!!!  
        解决方案:百度:没有学校邮箱怎么注册获得Jetbrain学生认证
    2. 这个md到底是被学长放在哪个文件的我也不太清楚,为了方便我给你们地址
        https://github.com/SDUSTACM/acmanager-backend
    3. 用git然后clone一下就好,网速慢的同学可以去上个厕所
    4.clone成功之后接下一个教程

####需要的基础环境
    python3.6
    pip
    mysql(个人推荐在自己电脑上安好,学长推荐在bash下安好)
    亲学长亲情推荐:安个bash吧~

在你的电脑上创建名为ACManager的database

接下来创建虚拟环境venv

####用pycharm搭一个虚拟环境

详情见这个教程:https://jingyan.baidu.com/article/48b558e3ffeb667f39c09a41.html

File->settings...->Project:acmanager-backend->Project   interpreter

然后右上角似乎有一个齿轮的符号,点之.然后点那个add

选第一个virtualvenv environment 选择new然后选在你的工作区内.然后OK

然后你的project里似乎会出现一个venv文件夹,后面还跟着个小字 library root

然后在pycharm里打开那个requirement.txt 然后会提醒你安装些啥啥啥.

反正你乖乖听话安装就对了

***

然后我们去Edit configuration...

Host那个地方后面注明是8008

然后environment variables那个地方添加一个DJANGO_SETTINGS_MODULE   值为acmanager.settings

Python interpreter 改成你自己的那个虚拟机(就是刚才咱新添加的)

working dictionary 改成acmanager-backend

别的应该没有了

跑他丫的

~~辣鸡学弟现在去思考怎么pr去了~~
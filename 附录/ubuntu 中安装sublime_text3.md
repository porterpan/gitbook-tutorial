---
title: ubuntu 中安装sublime_text3
categories:     
    summary    
tags: [工具,sublime-text]
date: 2018-11-10 22:55:03
---
# 摘要

# <center>Porter Pan</center>

### <center>Enter "Alt+m" will show Markdown Preview</center>

>* 安装
>* 输入注册码
>* 汉化
>* 安装插件
>* 中文输入bug修复

<!-- more -->

## 1.1 安装
&emsp;&emsp;建议和我一样初学的直接安装，不要直接下载官方的离线包解压了，不然还得自己配置什么dash中显示，什么的环境配置乱七八糟的

```
1、 wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
2、 sudo apt-get install apt-transport-https
3、 echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
4、 sudo apt-get update
5、 sudo apt-get install sublime-text
```

## 1.2 输入注册码
&emsp;&emsp;在输入注册码之前先更改hosts，ubuntu中hosts位于：  vim /etc/hosts或者gedit /etc/hosts
,然后加入如下两行

```
1、 127.0.0.1       www.sublimetext.com
2、 127.0.0.1       license.sublimehq.com
```

&emsp;&emsp;然后保存，此时dash中输入sublime，找到我们安装的软件，打开后在界面菜单中选择help-->enter license，然后输入如下注册码
```
----- BEGIN LICENSE -----
sgbteam
Single User License
EA7E-1153259
8891CBB9 F1513E4F 1A3405C1 A865D53F
115F202E 7B91AB2D 0D2A40ED 352B269B
76E84F0B CD69BFC7 59F2DFEF E267328F
215652A3 E88F9D8F 4C38E3BA 5B2DAAE4
969624E7 DC9CD4D5 717FB40C 1B9738CF
20B3C4F1 E917B5B3 87C38D9C ACCE7DD8
5F7EF854 86B9743C FADC04AA FB0DA5C0
F913BE58 42FEA319 F954EFDD AE881E0B
------ END LICENSE ------
```
点击确定，然后就可以 enjoy it!
 
 在这还没结束，下面开始**汉化**
# 1.3 汉化

 &emsp;&emsp;打开软件，直接按下“shift+ctrl+p”在弹出的框内输入**ip**,然后点击"package control：install pakage",出来后输入"Chinese​Localizations"来安装**Chinese​Localizations**插件，然后重启，至此汉化结束。
# 1.4 安装markdown插件
 &emsp;&emsp;在软件界面输入“shift+ctrl+p”,然后输入“ip”，然后选择，packageinstall ，然后输入“Markdown Editing“ + ”MarkdownLivePreview”,分别安装上，然后新建md文件，在编辑界面输入“alt+m",则进入markdown preview实时显示模式。
# 1.5 解决Markdown不能输入汉字的问题
打开终端：

在终端中输入以下代码
```
git clone https://github.com/lyfeyaj/sublime-text-imfix.git
cd sublime-text-imfix && ./sublime-imfix
```
或者直接进入github的这个[仓库](https://github.com/lyfeyaj/sublime-text-imfix.git)：直接下载这个zip包，然后解压，然后在终端中cd到这个解压后的文件夹路径中，最后是在终端中输入
```
./sublime-imfix
```
此时重启sublimetext3 然后就可以进行汉字的输入了。

# 参考：

https://blog.csdn.net/qq_41590417/article/details/80461075

https://blog.csdn.net/woaidouya123/article/details/81476551

https://www.cnblogs.com/james-lee/p/6847906.html



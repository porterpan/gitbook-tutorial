---
title: ubuntu18 正确 安装ShadowSocket
date: 2018-11-10 19:26:15
categories:     
    summary
tags: [Linux,Socket5]
---

# <center> ubuntu18 正确安装shadowsocket </center>

## 摘要

为达到能够自由访问全球学习资料，我可谓是绞尽脑汁莫寻方法，目前能做到的除了付费包月的vpn代理机构的，就只能是自己动手自己干的了，但是自己搞旺旺会出很多问题，本文结合晴子实践的经验，将所遇到的问题都一一列下并解决。

![Socket5](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1541859694666&di=4157a8d46151dfea7b45b6b0e6277d61&imgtype=0&src=http%3A%2F%2Fwenwen.soso.com%2Fp%2F20120619%2F20120619102239-1814974902.jpg)

<!-- more -->

## 1、正常的安装步骤（ubuntu16版本）


```bash
* Ctrl+Alt+T打开终端，输入以下命令安装好GUI界面shadowsocks-qt5
* sudo add-apt-repository ppa:hzwhuang/ss-qt5
* sudo apt-get update
* sudo apt-get install shadowsocks-qt5
```

* 但是Ubuntu18.04在安装shadowsocks-qt5时就会出现错误

```bash
仓库 “http://ppa.launchpad.net/hzwhuang/ss-qt5/ubuntu bionic Release” 没有 Release 文件
```

# 原因：

* ppa:hzwhuang/ss-qt5 并没有18.04版本的源

# 解决方法：

### 第一步、修改sources.list.d下文件名

修改/etc/apt/sources.list.d/hzwhuang-ubuntu-ss-qt5-bionic.list文件，将bionic（18.04版本代号）改成xenial（16.04版本代号）

### 第二步、设置如下图

>> * bash 中打开 
**软件更新器** ---> **设置** ---> **其他软件** -->

>> * 编辑：http://ppa.launchpad.net/hzwhuang/ss-qt5/ubuntu

![编辑发行版](https://i.loli.net/2018/10/22/5bcdcb28d4124.png)

** 将发行版改为xenial **,如上图所示。

## 然后再执行

* sudo apt-get update
* sudo apt-get install shadowsocks-qt5 






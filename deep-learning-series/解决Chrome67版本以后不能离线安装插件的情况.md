---
title: 解决Chrome67版本以后不能离线安装插件的情况
categories:     
    summary    
tags: [工具,总结]
date: 2018-11-10 22:55:03
---

<center> Porter Pan </center>

# 摘要

通过本文安装方法可以快速，解决Chrome67版本以后不能离线安装插件的情况。

![离线插件安装失败](https://i.loli.net/2018/10/22/5bcde5483136e.png)

<!-- more -->



> 一般情况下，我们如果使用的Chrome版本为67以后的版本，安装离线插件会出现如下图信息

![离线插件安装失败](https://i.loli.net/2018/10/22/5bcde5483136e.png)

> 但是这样我们就真的没法安装离线插件了吗？特别是对想安装翻墙的插件 ***Proxy SwitchyOmega*** 的同学来说是一件噩梦。这篇文章讲会告诉读者，这个问题是可以解决的

## 解决方法如下：
* 首代开终端输入以下代码
>> /opt/google/chrome/google-chrome --enable-easy-off-store-extension-install

>> 将会打开google Chrome 浏览器，然后进入浏览器的扩展插件工具界面，如下图所示：

![扩展程序界面](https://i.loli.net/2018/10/22/5bcde7297750e.png)

* 此时请再次将离线下载的插件拖进去，看看是不是能够安装了。

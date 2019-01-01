---
title: Hexo 每次写好后deploy博客
categories:     
    summary
tags: [Hexo,Blogs]
date: 2018-11-10 22:55:03
---

<center> Porter Pan </center>

## 摘要：

github page 结合Hexo-Yelee或者Next主题,搭建个人博客主页，是很不错的一个选择，个人使用情况，感觉Yelee界面布局啥的还是很不错的。

这篇文章中我将介绍每次我们写好的md博文怎么部署到github page 上去。

----

本文主要使用的命令行如下：

* 1、直接部署到网站

```bash
hexo clean && hexo g && hexo d
```
<!-- more -->

也可以本地部署，查看浏览效果

* 2、部署到本地，查看浏览效果

```bash
hexo clean && hexo g && hexo s
```

## 我们每次写好的博文如何正确推送至github

每次我们写好了博文后，需要上传至我们的github空间中,只需要每次将我们写好的博文放到文件路径：
```C
D:\Github\smritipertor.github.io\source\_posts
```

如果之前没有安装过
** hexo-deployer-git **
的话，先执行：

```bash
npm install hexo-deployer-git --save
```

然后执行如下命令操作：

* 首先在你之前建好的博文路径：比如我的是

```bash
hexo generate

hexo s //(或者:hexo server)

hexo deploy //(或者:hexo d)
```

## 说明

* 一般我们在站点根目录中的“_config.yml”中的文件中设定我们hexo d，的部署文件到那个ID和分支中，设置内容如下：
* 
```shell
deploy:
  type: git 
  repository: https://github.com/smritipertor/smritipertor.github.io.git
  branch: master
```

> 以上内容表示，不管我们当前工作在那个分区，只要站点根目录中的“_config.yml”中branch 分区设置好，直接

```shell
hexo d
```

> 就可以发布了。

如果你执行：
```shell 
hexo generate -d 
```

## 常见错误及解决办法

### 第一种，部署出错

出现错误提示，如下：
```shell 
fatal: in unpopulated submodule '.deploy_git'                                                                           FATAL Something's wrong. Maybe you can find the solution here: http://hexo.io/docs/troubleshooting.html                 Error: fatal: in unpopulated submodule '.deploy_git'                                                                                                                                                                                                at ChildProcess.<anonymous> (D:\GitWebsite\smritipertor.github.io\node_modules\hexo-util\lib\spawn.js:37:17)            at ChildProcess.emit (events.js:182:13)                                                                                 at ChildProcess.cp.emit (D:\GitWebsite\smritipertor.github.io\node_modules\cross-spawn\lib\enoent.js:40:29)             at maybeClose (internal/child_process.js:962:16)                                                                        at Process.ChildProcess._handle.onexit (internal/child_process.js:251:5)  
```

则你可以直接执行以下命令即可：

```shell
rm -rf .deploy_git
hexo generate -d
```
即，删除地电脑本地的.deploy_git文件夹（可能是你上个版本是另一台电脑），然后再生成、部署即可。

### 至此你的网站上就有了网站数据




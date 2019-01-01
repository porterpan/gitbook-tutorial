---
title: git 推送新的文章到github其他分支上
date: 2018-11-10 19:42:28
categories:
    summary
tags:
    git
---

# <center> Porter Pan </center>

## 摘要

每次编辑博文并通过命令部署网站到github page上时，我们想每天都能将改动后的博文备份到github的一个分支上，实现本地数据同步到云仓库中。

* 实现本地博客云同步到github page其他分支上
* 实现本地博客部署到github page上的master分支上

![我的博客网站](https://s1.ax1x.com/2018/11/10/iqZ6KJ.png)

<!-- more -->

## 网站部署（建议隔段时间再部署到网站上，短时间内直接部署本地，本地浏览下就好

### 部署到网上

* 直接部署到github page的master上

```bash
1 git clone -b proworking <我的github网站仓库:proworking>
2 git pull origin proworking  #从我的工作分支更新最新的博文和站点配置文件
3 git checkout master  #将我们的本地切换到master分支
4 #此处开始加入你的博文.md到站点的：\source\_posts文件夹中
5 hexo clean && hexo g && hexo d
```

### 部署到本地

* 本地部署，本地浏览效果

```bash
1 git clone -b proworking <我的github网站仓库:proworking>
2 git checkout master  #将我们的本地切换到master分支
3 #此处开始加入你的博文.md到站点的：\source\_posts文件夹中
4 hexo clean && hexo g && hexo d
```
> 实现从github上获取我仓库中的Proworking分支数据，病拉取到我的本地

* 将本地的博文再重新push到我的云仓库（proworking)

```bash
git add .
git commit -m "添加了：file1.md\file2.md"
git push origin HEAD:proworking #一定要添加HEAD 不然会
```

-------------

## 其他注意事项

>下面贴上我遇到的问题

* [1] 若果你直接输入命令：
```bash
$ git push proworking
```
可能会出现如下的不正常信息：

```bash
Pertor@Pertor-PC MINGW64 /d/Github/smritipertor.github.io (master)
$ git push proworking

fatal: 'proworking' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.

```

正确的解决办法是，命令中输入如下代码（加HEAD)

```bash
Pertor@Pertor-PC MINGW64 /d/Github/smritipertor.github.io (master)
$ git push origin HEAD:proworking
```

此时会输出正确的提示，具体提示信息如下：

```bash
Enumerating objects: 1498, done.
Counting objects: 100% (1480/1480), done.
Delta compression using up to 4 threads
Compressing objects: 100% (1219/1219), done.
Writing objects: 100% (1461/1461), 1.17 MiB | 390.00 KiB/s, done.
Total 1461 (delta 187), reused 1300 (delta 139)
remote: Resolving deltas: 100% (187/187), completed with 10 local objects.
To https://github.com/smritipertor/smritipertor.github.io.git
   06b21dd..1ff56b7  HEAD -> proworking

```


---
title: ros and gazebo and gym_gazebo安装
localimage: image4
urlname: ros_gazabo_gym_gazabo_install
categories:      
    ROS    
tags: [ROS,Deep Learning,Algorithm]
date: 2019-4-4 22:55:03
---

# 摘要

本节笔记主要记录ROS室内仿真环景的具体演示过程和

- [x] Edit By Porter, 积水成渊,蛟龙生焉。 

<!-- more -->

## ros 安装

## gazebo安装

## gym_gazebo安装

## 安装配置中的问题

### python 环境下提示无法导入rospy

#### 报错



#### 解决

```bash
sudo pip install catkin-tools
sudo pip install rospkg
```

```bash
sudo pip3 install catkin-tools
sudo pip3 install rospkg
```

#### 效果

```shell
porter@porter-Aspire:~$ sudo pip3 install catkin-tools
[sudo] porter 的密码： 
The directory '/home/porter/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
The directory '/home/porter/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
Requirement already satisfied: catkin-tools in /usr/local/lib/python3.5/site-packages
Requirement already satisfied: osrf-pycommon>0.1.1 in /usr/local/lib/python3.5/site-packages (from catkin-tools)
Requirement already satisfied: PyYAML in /usr/local/lib/python3.5/site-packages (from catkin-tools)
Requirement already satisfied: setuptools in /usr/local/lib/python3.5/site-packages (from catkin-tools)
Requirement already satisfied: catkin-pkg>0.2.9 in /usr/local/lib/python3.5/site-packages (from catkin-tools)
Requirement already satisfied: trollius in /usr/local/lib/python3.5/site-packages (from catkin-tools)
Requirement already satisfied: docutils in /usr/local/lib/python3.5/site-packages (from catkin-pkg>0.2.9->catkin-tools)
Requirement already satisfied: pyparsing in /usr/local/lib/python3.5/site-packages (from catkin-pkg>0.2.9->catkin-tools)
Requirement already satisfied: python-dateutil in /usr/local/lib/python3.5/site-packages (from catkin-pkg>0.2.9->catkin-tools)
Requirement already satisfied: six in /usr/local/lib/python3.5/site-packages (from trollius->catkin-tools)
You are using pip version 9.0.1, however version 19.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

porter@porter-Aspire:~$ sudo pip3 install rospkg
The directory '/home/porter/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
The directory '/home/porter/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
Requirement already satisfied: rospkg in /usr/local/lib/python3.5/site-packages
Requirement already satisfied: PyYAML in /usr/local/lib/python3.5/site-packages (from rospkg)
Requirement already satisfied: catkin-pkg in /usr/local/lib/python3.5/site-packages (from rospkg)
Requirement already satisfied: python-dateutil in /usr/local/lib/python3.5/site-packages (from catkin-pkg->rospkg)
Requirement already satisfied: pyparsing in /usr/local/lib/python3.5/site-packages (from catkin-pkg->rospkg)
Requirement already satisfied: docutils in /usr/local/lib/python3.5/site-packages (from catkin-pkg->rospkg)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.5/site-packages (from python-dateutil->catkin-pkg->rospkg)
You are using pip version 9.0.1, however version 19.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

porter@porter-Aspire:~$ python3
Python 3.5.6 (default, Mar 29 2019, 21:29:42) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import rospy
>>> 
```

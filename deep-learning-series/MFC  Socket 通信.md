---
title: C++ MFC 界面实现套接字（socket) 通信
categories:
    skill
tags: [C++,Socket,GUI]
date: 2018-11-10 22:55:07
---

# 摘要

* Socket 套接字的概念
* Socket 函数功能
* MFC 介绍
* TCP 变成步骤
* TCP 上位机实现

<!-- more -->

## Socket 套接字的概念

引用[百度百科的一句话](https://baike.baidu.com/item/socket/281150?fr=aladdin)：网络上的两个程序通过一个双向的通信连接实现数据的交换，这个连接的一端称为一个socket。

* 一段形象的比喻：

>建立网络通信连接至少要一对端口号(socket)。socket本质是编程接口(API)，对TCP/IP的封装，TCP/IP也要提供可供程序员做网络开发所用的接口，这就是Socket编程接口；HTTP是轿车，提供了封装或者显示数据的具体形式；Socket是发动机，提供了网络通信的能力。

----

Socket的英文原义是“孔”或“插座”。在Internet上的主机一般运行了多个服务软件，同时提供几种服务。每种服务都打开一个Socket，并绑定到一个端口上，不同的端口对应于不同的服务。Socket正如其英文原义那样，像一个多孔插座。一台主机犹如布满各种插座的房间，每个插座有一个编号，有的插座提供220伏交流电， 有的提供110伏交流电，有的则提供有线电视节目。 客户软件将插头插到不同编号的插座，就可以得到不同的服务。

[SuperSocke,可扩展的 Socket 服务器框架](http://www.supersocket.net/)

[socket.io github 网页](https://github.com/socketio/socket.io)或者[官网](http://socket.io)

## Socket 函数功能

具体函数如下：

* socket()函数

* bind()函数

* connect()函数

* listen()函数

* accept()函数

* send()和recv()函数

* sendto()和recvfrom()函数

* close()和shutdown()函数

* getpeername()函数

* gethostname()函数

---

### socket() 函数

```C++
int socket(int domine,int type,int protocol);
```

* 参数(int domin)：

> 函数参数，即协议域，又称为协议族。协议族决定了socket的地址类型，在通信中必须采用对应的地址，如AF_INET(IPV4)、AF_INET6(IPV6)、AF_LOCAL（或称AF_UNIX，Unix域socket）、AF_ROUTE等等。通常情况下我们使用AF_INET。

> AF_INET的定义是：#define AF_INET 2，所以这里的参数都是int型的

* 参数(int type)：

> :是套接口类型，主要SOCK_STREAM(建立TCP连接)、SOCK_DGRAM（建立UDP）、SOCK_RAW；
SOCK_STREAM(建立TCP连接)：提供面向连接的可靠的数据传输服务。数据被看作是字节流，无长度限制。例如FTP协议就采用这种。
SOCK_DGRAM（建立UDP）：提供无连接的数据传输服务，不保证可靠性。

> SOCK_RAW：该接口允许对较低层次协议，如IP，ICMP直接访问。

* 参数(int protocole)：

> 指定协议。常用的协议有，IPPROTO_TCP、IPPTOTO_UDP、IPPROTO_SCTP、IPPROTO_TIPC等，它们分别对应TCP传输协议、UDP传输协议、STCP传输协议、TIPC传输协议。通常情况系设为0。

> **注意**：并不是上面的type和protocol可以随意组合的，如SOCK_STREAM不可以跟IPPROTO_UDP组合。当protocol为0时，会自动选择type类型对应的默认协议。

* 函数返回值(int):

> 成功：返回套接字描述符（套接字的索引）

> 失败：返回-1
 
### bind() 函数

一旦你有一个套接字，你可能要将套接字和机器上的一定的端口关联 起来。(如果你想用listen()来侦听一定端口的数据，这是必要一步--MUD 告 诉你说用命令 "telnet x.y.z 6969"。)如果你只想用 connect()，那么这个步 骤没有必要。但是无论如何，请继续读下去。

```C++
int bind(int sockfd, struct sockaddr *my_addr, int addrlen);
```

* 参数(int sockfd)：

> sockfd 是调用 socket 返回的文件描述符。

* 参数(struct sockaddr *my_addr)：

> my_addr 是指向数据结构 struct sockaddr 的指针，它保存你的地址(即端口和 IP 地址) 信息。

* 参数(int addrlen)：

> addrlen 设置为 sizeof(struct sockaddr)。

### connect()函数

现在我们假设你是个 telnet 程序。你的用户命令你得到套接字的文件 描述符。你听从命令调用了socket()。下一步，你的用户告诉你通过端口 23(标准 telnet 端口)连接到"132.241.5.10"。你该怎么做呢? 幸运的是，你正在阅读 connect()--如何连接到远程主机这一章。你可 不想让你的用户失望。

```C++
int connect(int sockfd, struct sockaddr *serv_addr, int addrlen);
```

* 参数(int sockfd)：

> sockfd 是系统调用 socket() 返回的套接字文件描述符。

* 参数(struct sockaddr *serv_addr)：

> serv_addr 是 保存着目的地端口和 IP 地址的数据结构 struct sockaddr。

* 参数(int addrlen)：

> addrlen 设置 为 sizeof(struct sockaddr)。

### listen()函数

是换换内容得时候了。假如你不希望与远程的一个地址相连，或者说， 仅仅是将它踢开，那你就需要等待接入请求并且用各种方法处理它们。处 理过程分两步：首先，你听--listen()，然后，你接受--accept() (请看下面的 内容)。

```C++
int listen(int sockfd, int backlog);
```

* 参数(int sockfd)：

> sockfd 是调用 socket() 返回的套接字文件描述符。

* 参数(int backlog)：

backlog 是在进入 队列中允许的连接数目。

### accept()函数


### send()和recv()函数

### sendto()和recvfrom()函数

### close()和shutdown()函数

### getpeername()函数

### gethostname()函数





本节参考了[博文](https://www.cnblogs.com/kefeiGame/p/7246942.html)

## MFC 介绍







## TCP 上位机实现


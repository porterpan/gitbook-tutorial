---
title: Module篇使用__future__
categories:      
    Python      
tags: [Module,__future__]
date: 2019-02-4 10:38:03
---

# 摘要

本节主要是学习Python 相关编程的总结及其他信息。

- [x] Edit By Porter, 不积跬步无以至千里。

<!-- more -->

[官方定义参考地址](https://docs.python.org/3/library/__future__.html)— Future statement definitions。

__future__ is a real module, and serves three purposes:

- To avoid confusing existing tools that analyze import statements and expect to find the modules they’re importing.
- To ensure that future statements run under releases prior to 2.1 at least yield runtime exceptions (the import of __future__ will fail, because there was no module of that name prior to 2.1).
- To document when incompatible changes were introduced, and when they will be — or were — made mandatory. This is a form of executable documentation, and can be inspected programmatically via importing __future__ and examining its contents.


---
title: Python 帮助文档检索方法
categories:      
    Python      
tags: [Module]
date: 2019-02-4 10:38:03
---

# 摘要

本节主要是学习Python 相关如何查找帮助文档，提升编程效率。

- [x] Edit By Porter, 不积跬步无以至千里。

<!-- more -->

Python中的Module很丰富，一段时间不用，我们就会忘记各个模块的功能作用，以及如何调用模块中的方法。所以会使用帮助文档，以及高效的使用帮助文档，将变得十分重要。

## 一、查看python中模块的所有方法

### 命令行下使用pydoc命令

```python
在命令行下运行$ pydoc modules即可查看
```

### 在python交互解释器中使用help()查看

```Python
在交互式解释器中输入>>> help("modules")即可，效果跟在命令行下输入$ pydoc modules是一样的
```

又如：

```Python
>>> help(math.sin)
Help on built-in function sin in module math:

sin(...)
    sin(x)

    Return the sine of x (measured in radians).

>>> 
```

### 查看函数信息的另一种方法print(func_name.__doc__)

如查看内建函数print用法

```Python 
>>> print(print.__doc__)
print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

Prints the values to a stream, or to sys.stdout by default.
...
>>> 
```

> __doc__前后是两个短下划线，在python中会合并为长下划线python中的help()类似unix中的man指令，熟悉后会对我们的编程带来很大帮助

### 查看模块下所有函数dir(module_name)

如我们需要列举出math模块下所有的函数名称

```Python
>>> dir(math)
['__doc__', '__loader__', '__name__',...]
>>> 
```

又如：

```
import requests,os,random
print(dir(random))

# ['BPF', 'LOG4', 'NV_MAGICCONST', 'RECIP_BPF', 'Random', 'SG_MAGICCONST', 'SystemRandom', 
#  'TWOPI', '_BuiltinMethodType', '_MethodType', '_Sequence', '_Set', '__all__', '__builtins__', 
#  '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_acos', 
#  '_ceil', '_cos', '_e', '_exp', '_inst', '_log', '_pi', '_random', '_sha512', '_sin', '_sqrt', '_test',
#  '_test_generator', '_urandom', '_warn', 'betavariate', 'choice', 'expovariate', 'gammavariate', 'gauss', 
#  'getrandbits', 'getstate', 'lognormvariate', 'normalvariate', 'paretovariate', 'randint', 'random', 'randrange', 
#  'sample', 'seed', 'setstate', 'shuffle', 'triangular', 'uniform', 'vonmisesvariate', 'weibullvariate']
```

### 在python交互是解释器下导入sys模块查看

python的sys模块也是可以用来查看模块信息的

```Python
>>> import sys
>>> sys.modules.keys()
```
### 命令行下使用pip查看

> 如果你使用的是pip来作为你的python包管理器的话，可以在命令行下直接运行$ pip freeze</code>或者<code>$ pip list来查看安装包的信息，当然其它的包管理器也有类似的功能，同时，你也可以在python交互式解释器中导入pip模块来查看包信息

```Python
import pip
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     for i in installed_packages])
print(installed_packages_list)
```

### 使用yolk来查看

> 如果你安装过yolk的话可以使用yolk命令来查看包信息，你可以使用$ pip install yolk来安装它 
yolk使用简单，只需在命令行下操作即可

```Python 
$ yolk -l    #列出所有安装模块
$ yolk -a    #列出激活的模块
$ yolk -n    #列出非激活模块
$ yolk -U [packagename]  # 通过查询pypi来查看（该）模块是否有新版本
```


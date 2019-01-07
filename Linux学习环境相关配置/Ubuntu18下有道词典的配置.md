# 有道词典解包dep，修改源码接着玩

## Ubnutu18 安装有道词典

> 本来准备安装有道云笔记的，但是我的linux是ubuntu18的Qt是5.9 用不了啊，他的Qt是哪个版本的没弄清楚，好像是5.4的，结果就是我安装不上，做这个笔记就是为了想办法重新改写他的源码看看能不能好点支持。

[文章参考来源](https://blog.csdn.net/wangxiao7474/article/details/61196238?utm_source=blogxgwz4)

----

该版本依赖于python3，需要如下依赖包：

```python
Depends: python3, python3-pyqt5, python3-requests, python3-xlib, tesseract-ocr, tesseract-ocr-eng, tesseract-ocr-chi-sim, tesseract-ocr-chi-tra, python3-pil, ttf-wqy-microhei, python3-lxml, python3-xdg, python3-pyqt5.qtmultimedia, python3-pyqt5.qtquick, python3-pyqt5.qtwebkit, gir1.2-appindicator3-0.1, python3-dbus, qtdeclarative5-controls-plugin, libqt5multimedia5-plugins,gstreamer0.10-plugins-ugly
```

* Ok， 没有条件我们开始创造条件

### 第一步、下载有道词典的dep包

进入官网，然后选择ubuntu的包下载

> 下载的是deb包，文件名为：youdao-dict_1.1.0-0-ubuntu_amd64.deb 。

### 第二步、解包

```dash 
#解压deb包到youdao-dict目录
dpkg -X youdao-dict_1.1.0-0-ubuntu_amd64.deb  youdao-dict
#解压deb包中的control信息，control中写有该软件的依赖信息
dpkg -e youdao-dict_1.1.0-0-ubuntu_amd64.deb youdao-dict/DEBIAN


```
### 第三步、修改

```dash
cd youdao-dict
cd DEBIAN
vim control
#进入解压目录，编辑control文件，删除文件中Depends：后面的gstreamer0.10-plugins-ugly，并保存
```

[v] 接着就是修改工程中的源码

[v] 接着就是保存修改

### 第四步、重新打包

```dash
cd ~/下载
#将修改后的安装文件重新打包
dpkg-deb -b youdao-dict youdao-dict_new.deb

```

第五步、重新安装

```dash 
#安装重新打包的deb包
sudo dpkg -i youdao-dict_new.deb
```

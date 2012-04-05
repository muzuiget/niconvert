*********
Niconvert
*********

简介
====

Niconvert 是一个弹幕字幕下载和转换工具，将弹幕视频网站上的评论转换成 ass 字幕。

方便在桌面播放器配合高画质视频看吐槽。

支持如下特性：

* 支持 acfun 和 bilibili 国内两大弹幕视频网站。
* 解析下载无需注册和积分。
* 支持上/下方的固定位置样式，以及颜色转换。
* 自定义字体和字体大小。
* 设置视频大小和同屏行数。
* 自定义下方字幕的底边距离。
* 自定义字幕速度。

使用 Python 语言编写，目前提供命令行、web界面和GUI界面。

网页界面
========

现成实例，直接访问 http://niconvert.appspot.com/

如果无法访问，备用地址 http://niconvert.qixinglu.com/

如果你想自己搭建，需要安装 `bottle`_ ，下载 `bottle.py`_ 到程序根目录，接着运行 ::

    ./niconvert_web.py
    
然后本地浏览器访问 http://127.0.0.1:8624/

.. _bottle: http://bottlepy.org/

.. _bottle.py: https://github.com/defnull/bottle/raw/master/bottle.py

GUI界面
=======

GTK
---

运行 ::

    ./niconvert_gtk.py

QT
--

运行 ::

    ./niconvert_qt.py

WxWidget
--------

运行 ::

    ./niconvert_wx.py

Tkinter
-------

运行 ::

    ./niconvert_tk.py

命令行
======

``niconvert.py`` 即为主程序，只使用 Python 标准库。

使用方法，默认只需要给视频地址就可以了 ::

    ./niconvert.py 视频地址

会自动在当前目录下输出 ``视频标题.ass`` 文件。


执行 ``./niconvert.py -h`` 即可看到可选选项。

许可证
======

使用 GPLv3 许可证。

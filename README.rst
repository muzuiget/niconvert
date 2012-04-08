*********
Niconvert
*********

简介
====

Niconvert 是一个弹幕字幕下载和转换工具，将弹幕视频网站上的评论转换成 ass 字幕。

方便在桌面播放器配合高画质视频看吐槽。

支持如下特性：

* 支持 acfun 和 bilibili 国内两大弹幕视频网站。
* 解析下载无需在网站上注册和积分。
* 同样支持支持上/下方的固定位置样式，以及颜色转换。
* 自定义字体和字体大小。
* 自定义视频大小和同屏行数。
* 自定义下方字幕的底边距离。
* 自定义字幕速度。

使用 Python 语言编写，目前提供命令行、web界面和桌面GUI界面。

每个界面的转换效果的都一样，运行都需要 `Python 2.7`_ 然后按下面说明按需配置。

.. _Python 2.7: http://www.python.org/getit/

命令行
======

``niconvert.py`` 即为主程序，只使用 Python 标准库。

使用方法，默认只需要给视频地址就可以了 ::

    ./niconvert.py 视频地址

会自动在当前目录下输出 ``视频标题.ass`` 文件。

执行 ``./niconvert.py -h`` 即可看到可选选项。

网页界面
========

现成实例 

* GAE http://niconvert.appspot.com/
* 备用地址 http://niconvert.qixinglu.com/

依赖 `bottle`_ ，只需要下载这个文件 `bottle.py`_ 并放到程序根目录，接着运行 ::

    ./niconvert_web.py
    
然后本地浏览器访问 http://127.0.0.1:8624/

.. _bottle: http://bottlepy.org/

.. _bottle.py: https://github.com/defnull/bottle/raw/master/bottle.py

GUI界面
=======

界面都基本一样，只是界面样式和依赖有所不同，情况如下表

+----------+-------+---------+-----+----------+
| 界面     | Linux | Windows | Mac | 额外依赖 |
+==========+=======+=========+=====+==========+
| GTK      | √     |         |     | 大       |
+----------+-------+---------+-----+----------+
| QT       | √     | √       | √   | 大       |
+----------+-------+---------+-----+----------+
| wxWdiget | √     | √       | √   | 中       |
+----------+-------+---------+-----+----------+
| Tk       | √     | √       | √   | 小       |
+----------+-------+---------+-----+----------+

GTK
---

依赖GTK3，即依赖PyGObject3。

目前PyGObject3暂无Windows运行运行环境。

运行 ::

    ./niconvert_gtk.py

QT
--

依赖 PySide_ ，非 PyQt_ 。

PySide对Linux/Windows/Mac都有良好支持，只需要安装对应的平台的 `PySide二进制包`_ 即可。

运行 ::

    ./niconvert_qt.py

.. _PySide: http://www.pyside.org/
.. _PYQt: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _PySide二进制包: http://qt-project.org/wiki/Category:LanguageBindings::PySide::Downloads

wxWidget
--------

依赖 wxPython_ 。

wxPython对Linux/Windows/Mac都有良好支持，只需要安装对应的平台的 `wxPython二进制包`_ 即可。

运行 ::

    ./niconvert_wx.py

.. _wxPython: http://www.wxpython.org/
.. _wxPython二进制包: http://www.wxpython.org/download.php

Tk
--

依赖Tkinter。

Tkinter是Python标准库组件，无需再安装额外依赖，只是界面比较简陋。

运行 ::

    ./niconvert_tk.py

选项说明
========

提供一些自定义选项方便调整字幕样式

字体(-f/-s)
    设置默认使用的字体，不包括样式（即粗体和斜体）。字体大小即为原弹幕中的默认中号字体，大号和小号字体和会按此大小作相应的增减。

分辨率(-r)
    视频的分辨率，非网站Flash播放器上的视频 ，而是你挂在转换出来的ass字幕来播放的视频。因为ass字幕各种位置参数（如字体大小，字幕边距等）都按此分辨率（或这叫坐标）为准。如果和视频实际分辨率不一致，播放器会进行字幕缩放操作。

同屏行数(-l)
    也就是把滚动字幕限制在画面上方几行，以免遮挡大部分画面。

底边距离(-b)
    设置下方字幕的底边距离，也就是Flash播放里正下方的字幕，考虑视频本身的对白字幕也在正下方，为了避免遮挡对白字幕，设置这个参数让下方字幕比对白字幕高一点或者低一点。

调整秒数(-t)
   如果对字幕滚动得过快或者过慢，可以调整此参数，正数为减慢，负数为加快。

FAQ
===

Q：为什么看起来和Flash播放器上样式不一致？

A：实现技术不同，不可能一致，ass算是各种字幕标准中提供能提高最高级的功能了。

Q：字幕太多时会重叠起来，有所谓的碰撞检测吗？

A：暂时没有，实现一个完美的弹幕算法还是要不少精力啊。

Q：视频的分辨率很低，字体怎么调整都不舒服，调小了，看不清，调大，遮挡画面。

A：有两个方法：1，在播放器上修改字幕的渲染方式，例如smplayer的视频滤镜有「软件缩放」功能，启用后字幕会变得清晰锐利，不像默认的「内嵌」在视频中，而是像浮动在视频上方。2，加黑边，例如smplayer的视频滤镜有「加黑边」功能，会让字幕现实在黑边上，但注意加黑边后分辨率实际上已经改变了，字幕可能被播放器缩放。

Q：视频被分段怎么办，有合并功能吗，不同步怎么办？

A：暂时没有合并功能，目前只有转换功能，同步字幕还是用专业的字幕修改工具吧，推荐用 gaupol_

Q：有些视频需要登录权限，怎么下载？

A：同样支持根据评论地址转换，在浏览器上安装 `Niconvert - Commnet Link`_ 这个脚本，会在视频页面显示出评论地址的链接，复制评论地址并粘贴到输入框即可。

.. _gaupol: http://home.gna.org/gaupol/
.. _Niconvert - Commnet Link: http://userscripts.org/scripts/show/130401

许可证
======

使用 GPLv3 许可证。

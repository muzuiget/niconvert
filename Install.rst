########
安装说明
########

Linux/Mac
=========

需要 Python 2.7。

niconvert.py 文件就是命令行界面，使用 ``-h`` 参数运行查看详细帮助。

其余文件都是命令行的 GUI 前端，安装对应的依赖包即可。

web 版本依赖的是 `bottle`_ 默认地址是 http://127.0.0.1:8624/

.. _bottle: http://bottlepy.org/

Windows
=======

安装 Python
-----------

如果你还没有安装过 Python 请先下载安装。

打开 http://python.org/getit/ 需要版本是 2.7.x，目前最新是 2.7.3。

* 32 位系统下载「Python 2.7.3 Windows Installer」这个文件

* 64 位系统则是「Python 2.7.3 Windows X86-64 Installer」这个。

双击运行过安装到随便一个目录即可，然后就不用管了。

运行 niconvert
--------------

解压下载到的 zip 压缩包。双击 niconvert_tk.py 这个文件就看到界面了。

如果你嫌那个 cmd 黑框碍眼的话，只需要把 niconvert_tk.py 重命名成 niconvert_tk.pyw，这样重新运行就不会出现了。

实际运行就只需要 niconvert.py 和 niconvert_tk.py 这两个文件，其余文件都是用于不同系统的 GUI 界面而已，嫌碍眼的话，可以无视和删掉。

卸载和更新
----------

就是所谓的绿色软件了，卸载就是直接删掉解压缩后的目录即可，更新就是重新下载覆盖掉。

没有版本号，每次下载的就是最新版本。

查看 `更新日志 <https://github.com/muzuiget/niconvert/commits/master>`_

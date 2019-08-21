安装说明
========

[文档目录](./README.md)

使用 Python 3 编写，仅依赖标准库。

* 支持最小版本号为 Python 3.4.4。
* 编写此文档时最新版本是 [Python 3.7.1](https://www.python.org/downloads/release/python-370/)。

安装依赖
--------

### Windows

下载安装包 [python-3.7.1-amd64.exe](https://www.python.org/ftp/python/3.7.1/python-3.7.1-amd64.exe)，根据向导安装，安装后默认自动关联 .py 和 .pyw 文件，无需特别配置。

**注：** 最后支持 XP 版本为 Python 3.4.4，安装包 [python-3.4.4.msi](https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi)。

### MacOS

下载安装包 [python-3.7.1-macosx10.9.pkg](https://www.python.org/ftp/python/3.7.1/python-3.7.1-macosx10.9.pkg)，双击运行安装包，根据向导安装。

### Linux

一般发行版都自带最新的 Python 3 了，如果要使用图形界面，则需要先安装 `python3-tkinter` 包。

运行
----

执行文件只有程序根目录下的 main.pyw，会自动根据当前环境判断使用命令行还是图形界面。

* 如果双击打开，则使用图形界面。
* 如果在终端调用，则使用命令行界面。
* 如果在终端以 ``main.pyw tk`` 参数调用，则使用图形界面。

或者你可以软链一份到 /usr/local/bin/ 里，以便在 `$PATH` 里使用。

```
$ sudo ln -s /path/to/main.pyw /usr/local/bin/niconvert
$ niconvert -h
usage: niconvert [-h] -o FILENAME [-f FILE] [-t] [-b] [-g] [+r WIDTHxHEIGHT]
                 [+f NAME] [+s SIZE] [+l COUNT] [+a NAME] [+t SECONDS]
                 [+d SECONDS] [+b HEIGHT] [+c LENGTH] [+h FILE]
                 FILENAME
```

卸载和更新
----------

卸载直接删掉程序根目录即可，更新就是重新下载覆盖根目录。

小软件就不特别弄版本号了，每次打包下载主干仓库就是最新版本，每次提交就是更新日志。

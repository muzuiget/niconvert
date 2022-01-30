安装说明
========

[文档目录](./README.md)

使用 Python 3 编写，仅依赖标准库。

* 编写此文档时最新版本是 Python 3.10.2。
* 支持最小版本号为 Python 3.4.4。

安装依赖
--------

### Windows

**方法一：通过 Microsoft Store**

这是 Windows 10 用户推荐方法，一键安装和卸载，干净无残留。

打开 Microsoft Store 程序，搜索 `Python 3.10`，进入应用页面安装。

* 确保发布者名字为 `Python Software Foundation`。
* 如果提示登录 Microsoft 账号，可以选择跳过。

**方法二：通过安装程序**

1. 打开 [Python Windows 下载页面](https://www.python.org/downloads/windows/)。
2. 选择一个稳定版本号，例如 `Python 3.10.2 - Jan. 14, 2022`，点击 `Download Windows installer (64-bit)` 链接下载。
3. 下载 python-3.10.2-amd64.exe 文件后，双击运行，并根据向导安装。

*备注：最后支持 Windows XP 版本为 Python 3.4.4。*

### macOS

1. 打开 [Python macOS 下载页面](https://www.python.org/downloads/macos/)。
2. 选择一个稳定版本号，例如 `Python 3.10.2 - Jan. 14, 2022`，点击 `Download macOS 64-bit universal2 installer` 链接下载。
3. 下载 python-3.10.2-macos11.pkg 文件后，双击运行，并根据向导安装。

### Linux

一般发行版都自带最新的 Python 3 了，如果要使用图形界面，则需要先安装 `python3-tkinter` 包。

运行
----

安装 Python 后，操作系统默认自动关联 .py 和 .pyw 文件，这两种文件可以直接双击运行。

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

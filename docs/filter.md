过滤器文件格式定义
==================

[文档目录](./README.md)

过滤器文件支持两种格式：

* 纯文本格式，以 `.txt` 为扩展名
* Pyhton 格式，以 `.py` 为扩展名

**注：** 过滤器执行顺序：

1. 游客过滤器
2. 顶部过滤器
3. 底部过滤器
4. 自定义过滤器

纯文本格式
----------

每行一条正则被表达式，例如：

```
最后
结局
^剧透
是凶手$
```

表达式使用部分匹配，简单的关键词直接打上即可。

如果要使用完全匹配，可以和 ``^`` 或 ``$`` 配搭使用。

具体参考 Python 的[正则文档][re]。

[re]: https://docs.python.org/3/library/re.html

Python 格式
-----------

如果你会 Python，可以编写一个小脚本来做复杂过滤，接口非常简单，.py 文件里有一个 `do_filter()` 函数即可。

```python
# 过滤字数小于 5 个字的弹幕
def do_filter(danmakus):
    keep = []
    for danmaku in danmakus:
        if len(danmaku.content) < 5:
            continue
        keep.append(danmaku)
    return keep
```

`do_filter()` 中的参数 `danmakus` 是一个 Python 数组，每个元素是一个 Danmaku 实例，有以下属性：

* `start` 出现时间，浮点数类型，单位是秒。
* `style` 位置，字符串类型，滚动、顶部、底部、忽略分别是 `scroll`、`top`、`bottom`、`none`。
* `color` 颜色，数字类型，十六进制的 RGB 字符串所表示的整数值。
* `commenter` 评论者ID，字符串类型。
* `content` 弹幕内容，字符串类型。
* `is_guest` 是否游客弹幕，布尔类型。

`do_filter()` 函数返回一个数组，表示过滤后输出到 ass 里的弹幕。

如果你想修改弹幕的各种属性，直接修改弹幕实例对象即可，例如想把所有颜色强制转成白色：

```python
# 把所有弹幕转成白色
def do_filter(danmakus):
    for danmaku in danmakus:
        danmaku.color = 0xffffff
    return danmakus
```

以下是一些用法示例：

### 示例：实现关键词过滤

类似纯文本格式的，使用正则表达式过滤

```python
import re

block_words = [
    '最后',
    '结局',
    '^剧透',
    '是凶手$',
]
block_words = list(map(re.compile, block_words))

def match_regexp(regexps, danmaku):
    for regexp in regexps:
        if regexp.search(danmaku.content):
            return True
    return False

def do_filter(danmakus):
    keep = []
    for danmaku in danmakus:
        if match_regexp(block_words, danmaku):
            continue
        keep.append(danmaku)
    return keep
```

### 示例：屏蔽某些评论者

屏蔽某些评论者所有弹幕

```python
import re

block_users = [
    'aaaa',
    'bbbb',
    'cccc',
]

def do_filter(danmakus):
    keep = []
    for danmaku in danmakus:
        if danmakus.commenter in block_users:
            continue
        keep.append(danmaku)
    return keep
```

### 示例：按关键词屏蔽评论者

综合上面两种代码，对于发了某些关键词的评论者，直接屏蔽其所有弹幕

```python
import re

# 一般屏蔽词
normal_words = [
    '最后',
    '结局',
    '^剧透',
    '是凶手$',
]
normal_words = list(map(re.compile, normal_words))

# 特殊屏蔽词，例如粗口，屏蔽该评论者所有弹幕
bad_words = [
    '傻逼',
    '我操',
    '妈的',
]
bad_words = list(map(re.compile, bad_words))

# 存放屏蔽评论者 ID
block_users = []

def match_regexp(regexps, danmaku):
    for regexp in regexps:
        if regexp.search(danmaku.content):
            return True
    return False

def do_filter(danmakus):
    # 第一次按关键词过滤
    keep1 = []
    for danmaku in danmakus:
        # 符合特殊屏蔽词，记下该评论者 ID 
        if match_regexp(bad_words, danmaku):
            block_users.append(danmaku.commenter)
            continue

        # 过滤一般屏蔽词
        if match_regexp(normal_words, danmaku):
            continue

        keep1.append(danmaku)

    # 第二次按评论者 ID 过滤
    keep2 = []
    for danmaku in keep1:
        if danmaku.commenter in block_users:
            continue
        keep2.append(danmaku)
    return keep2
```

JSON 文件格式定义
=================

[文档目录](./README.md)

如果你有其它来源的弹幕格式，想用 Niconvert 转换成 ass 文件，无需费劲转成B站的 xml 格式，直接转成 json 即可。

Niconvert 的 json 格式示例如下：

```json
[
    {
        "start": 0,
        "style": "scroll",
        "color": "ffffff",
        "commenter": "aaa",
        "content": "滚动弹幕内容",
        "is_guest": false
    },
    {
        "start": 1.0,
        "style": "top",
        "color": "ffffff",
        "commenter": "bbb",
        "content": "顶部弹幕内容",
        "is_guest": false
    },
    {
        "start": 2.0,
        "style": "bottom",
        "color": "ffffff",
        "commenter": "ccc",
        "content": "底部弹幕内容",
        "is_guest": false
    }
]
```

最顶层是一个数组，每个数组的元素一条弹幕，每个属性如下

* `start` 出现时间，数字类型，单位是秒，可以是否浮点数。
* `style` 位置，字符串类型，滚动、顶部、底部、忽略分别是 `scroll`、`top`、`bottom`、`none`。
* `color` 颜色，字符串类型，十六进制的 RGB 字符串。
* `commenter` 评论者ID，字符串类型。
* `content` 弹幕内容，字符串类型。
* `is_guest` 是否游客弹幕，布尔类型。

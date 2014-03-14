from .const import NOT_SUPPORT


class BaseDanmaku(object):
    ''' 弹幕基类 '''

    def __init__(self):

        # 开始时间
        self.start = 0

        # 位置样式
        self.style = NOT_SUPPORT

        # 颜色
        self.color = 0xFFFFFF

        # 评论者
        self.commenter = ''

        # 评论正文
        self.content = ''

        # 字体缩放比例
        self.size_ratio = 1

        # 是否游客弹幕
        self.is_guest = False

        # 是否歌词或神弹幕
        self.is_applaud = False

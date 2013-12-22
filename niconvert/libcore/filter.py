import re
from .const import BOTTOM


class BaseFilter(object):
    ''' 过滤器基类 '''

    def match(self, danmaku):
        return False


class GuestFilter(BaseFilter):
    ''' 游客过滤器 '''

    def match(self, danmaku):
        return danmaku.is_guest


class BottomFilter(BaseFilter):
    ''' 底部样式过滤器 '''

    def match(self, danmaku):
        return danmaku.style == BOTTOM


class CustomFilter(BaseFilter):
    ''' 自定义过滤器 '''

    def __init__(self, lines):
        self.lines = lines
        self.regexps = self._regexps()

    def _regexps(self):
        lines = filter(lambda l: l.strip(), self.lines)
        lines = filter(lambda l: l != '', lines)
        return list(map(re.compile, lines))

    def match(self, danmaku):
        for regexp in self.regexps:
            if regexp.search(danmaku.content):
                return True
        return False

guest_filter = GuestFilter()
bottom_filter = BottomFilter()

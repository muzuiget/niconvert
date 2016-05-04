import re
from .const import TOP, BOTTOM


class BaseFilter(object):
    ''' 过滤器基类 '''

    def match(self, danmaku):
        return False


class GuestFilter(BaseFilter):
    ''' 游客过滤器 '''

    def match(self, danmaku):
        return danmaku.is_guest


class TopFilter(BaseFilter):
    ''' 顶部样式过滤器 '''

    def match(self, danmaku):
        if danmaku.is_applaud:
            return False
        return danmaku.style == TOP


class BottomFilter(BaseFilter):
    ''' 底部样式过滤器 '''

    def match(self, danmaku):
        if danmaku.is_applaud:
            return False
        return danmaku.style == BOTTOM


class CustomFilter(BaseFilter):
    ''' 自定义过滤器 '''

    def __init__(self, lines):
        self.lines = lines
        self.regexps = self._regexps()

    def _regexps(self):
        return list(map(re.compile, self.lines))

    def match(self, danmaku):
        for regexp in self.regexps:
            if regexp.search(danmaku.content):
                return True
        return False

guest_filter = GuestFilter()
top_filter = TopFilter()
bottom_filter = BottomFilter()

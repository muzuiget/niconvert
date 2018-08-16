import os
import re
import importlib.util
from niconvert.libcore.const import TOP, BOTTOM

class BaseFilter:
    ''' 过滤器基类 '''

    def filter_danmakus(self, danmakus):
        return danmakus

class GuestFilter(BaseFilter):
    ''' 游客过滤器 '''

    def filter_danmakus(self, danmakus):
        return list(filter(lambda d: not d.is_guest, danmakus))

class TopFilter(BaseFilter):
    ''' 顶部样式过滤器 '''

    def filter_danmakus(self, danmakus):
        keep = []
        for danmaku in danmakus:
            if danmaku.is_applaud:
                keep.append(danmaku)
                continue
            if danmaku.style == TOP:
                continue
            keep.append(danmaku)
        return keep

class BottomFilter(BaseFilter):
    ''' 底部样式过滤器 '''

    def filter_danmakus(self, danmakus):
        keep = []
        for danmaku in danmakus:
            if danmaku.is_applaud:
                keep.append(danmaku)
                continue
            if danmaku.style == BOTTOM:
                continue
            keep.append(danmaku)
        return keep


class CustomSimpleFilter(BaseFilter):
    ''' 自定义过滤器(纯文本) '''

    def __init__(self, filename):
        self.filename = filename
        self.lines = self._lines()
        self.regexps = self._regexps()

    def _lines(self):
        with open(self.filename) as file:
            text = file.read().strip() + '\n'
            lines = map(lambda l: l.strip(), text.split('\n'))
            lines = list(filter(lambda l: l != '', lines))
        return lines

    def _regexps(self):
        return list(map(re.compile, self.lines))

    def match(self, danmaku):
        for regexp in self.regexps:
            if regexp.search(danmaku.content):
                return True
        return False

    def filter_danmakus(self, danmakus):
        keep = []
        for danmaku in danmakus:
            if self.match(danmaku):
                continue
            keep.append(danmaku)
        return keep

class CustomPythonFilter(BaseFilter):
    ''' 自定义过滤器(Python) '''

    def __init__(self, filename):
        self.filename = filename
        self.module = self._module()

    def _module(self):
        module_name = 'filter_module'
        file_path = os.path.abspath(self.filename)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, 'filter_danmakus'):
            raise ValueError('过滤文件不存在 filter_danmakus() 函数')
        return module

    def filter_danmakus(self, danmakus):
        return self.module.filter_danmakus(danmakus)

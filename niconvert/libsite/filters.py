import os
import re
import importlib.util

class BaseFilter:
    ''' 过滤器基类 '''

    def do_filter(self, danmakus):
        raise NotImplementedError

class GuestFilter(BaseFilter):
    ''' 游客过滤器 '''

    def do_filter(self, danmakus):
        keep = []
        for danmaku in danmakus:
            if danmaku.is_guest:
                continue
            keep.append(danmaku)
        return keep

class TopFilter(BaseFilter):
    ''' 顶部样式过滤器 '''

    def do_filter(self, danmakus):
        keep = []
        for danmaku in danmakus:
            if danmaku.style == 'top':
                continue
            keep.append(danmaku)
        return keep

class BottomFilter(BaseFilter):
    ''' 底部样式过滤器 '''

    def do_filter(self, danmakus):
        keep = []
        for danmaku in danmakus:
            if danmaku.style == 'bottom':
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
        with open(self.filename, 'r', encoding='utf-8') as file:
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

    def do_filter(self, danmakus):
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

        if not hasattr(module, 'do_filter'):
            raise ValueError('过滤文件不存在 do_filter() 函数')
        return module

    def do_filter(self, danmakus):
        return self.module.do_filter(danmakus)

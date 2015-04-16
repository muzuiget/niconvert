import os
import sys
from ..libcore.utils import xhms2s


class Config(object):
    ''' 本模块的配置对象 '''

    def __init__(self, args):
        self.args = args

        (self.screen_width,
         self.screen_height) = self._screen_size()
        self.font_name = self._font_name()
        self.base_font_size = self._base_font_size()
        self.line_count = self._line_count()
        self.layout_algorithm = self._layout_algorithm()
        self.tune_duration = self._tune_duration()
        self.drop_offset = self._drop_offset()
        self.bottom_margin = self._bottom_margin()
        self.custom_offset = self._custom_offset()
        self.header_template = self._header_template()

    def _screen_size(self):
        return map(int, self.args['play_resolution'].split('x'))

    def _font_name(self):
        if self.args['font_name']:
            return self.args['font_name']

        if sys.platform.startswith('win'):
            return '微软雅黑'
        else:
            return 'WenQuanYi Micro Hei'

    def _base_font_size(self):
        return self.args['font_size']

    def _line_count(self):
        if self.args['line_count'] == 0:
            return self.screen_height // self.base_font_size
        else:
            return self.args['line_count']

    def _layout_algorithm(self):
        return self.args['layout_algorithm']

    def _tune_duration(self):
        return self.args['tune_duration']

    def _drop_offset(self):
        return self.args['drop_offset']

    def _bottom_margin(self):
        return self.args['bottom_margin']

    def _custom_offset(self):
        return xhms2s(self.args['custom_offset'])

    def _header_template(self):
        if not self.args['header_file']:
            tpl_file = '/header.txt'
            filename = (os.path.dirname(__file__) + tpl_file)
        else:
            filename = self.args['header_file']
        with open(filename) as file:
            lines = file.read().strip().split('\n')
            lines = map(lambda l: l.strip(), lines)
            header = '\n'.join(lines) + '\n'
        return header

from ..libcore.const import SCROLL
from ..libcore.utils import s2hms, int2bgr, is_dark, correct_typos

DIALOGUE_TPL = '''
Dialogue: %(layer)s,%(start)s,%(end)s,Danmaku,,0000,0000,0000,,%(content)s
'''.strip()


class Subtitle(object):
    ''' 字幕 '''

    def __init__(self, danmaku, display, offset=0):
        self.danmaku = danmaku
        self.display = display
        self.offset = offset

        self.start = self._start()
        self.end = self._end()
        self.color = self._color()
        self.position = self._position()
        self.start_markup = self._start_markup()
        self.end_markup = self._end_markup()
        self.color_markup = self._color_markup()
        self.border_markup = self._border_markup()
        self.font_size_markup = self._font_size_markup()
        self.style_markup = self._style_markup()
        self.layer_markup = self._layer_markup()
        self.content_markup = self._content_markup()
        self.text = self._text()

    def _start(self):
        return self.danmaku.start + self.offset

    def _end(self):
        return self.start + self.display.duration

    def _color(self):
        return int2bgr(self.danmaku.color)

    def _position(self):
        x1, x2 = self.display.horizontal
        y1, y2 = self.display.vertical
        return dict(x1=x1, y1=y1, x2=x2, y2=y2)

    def _start_markup(self):
        return s2hms(self.start)

    def _end_markup(self):
        return s2hms(self.end)

    def _color_markup(self):
        # 白色不需要加特别标记
        if self.color == 'FFFFFF':
            return ''
        else:
            return '\\c&H%s' % self.color

    def _border_markup(self):
        # 暗色加个亮色边框，方便阅读
        if is_dark(self.danmaku.color):
            return '\\3c&HFFFFFF'
        else:
            return ''

    def _font_size_markup(self):
        if self.display.is_scaled:
            return '\\fs%d' % self.display.font_size
        else:
            return ''

    def _style_markup(self):
        if self.danmaku.style == SCROLL:
            return '\\move(%(x1)d, %(y1)d, %(x2)d, %(y2)d)' % self.position
        else:
            return '\\a6\\pos(%(x1)d, %(y1)d)' % self.position

    def _layer_markup(self):
        if self.danmaku.style != SCROLL:
            return '-2'
        else:
            return '-3'

    def _content_markup(self):
        markup = ''.join([
            self.style_markup,
            self.color_markup,
            self.border_markup,
            self.font_size_markup
        ])
        content = correct_typos(self.danmaku.content)
        return '{%s}%s' % (markup, content)

    def _text(self):
        return DIALOGUE_TPL % dict(
            layer=self.layer_markup,
            start=self.start_markup,
            end=self.end_markup,
            content=self.content_markup)

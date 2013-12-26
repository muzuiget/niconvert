from ..libcore.const import SCROLL
from ..libcore.utils import s2hms, int2bgr, is_dark, correct_typos

DIALOGUE_TPL = '''
Dialogue: {layer},{start},{end},Danmaku,,0000,0000,0000,,{content}
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
            return '\\c&H' + self.color

    def _border_markup(self):
        # 暗色加个亮色边框，方便阅读
        if is_dark(self.danmaku.color):
            return '\\3c&HFFFFFF'
        else:
            return ''

    def _font_size_markup(self):
        if self.display.is_scaled:
            return '\\fs' + str(self.display.font_size)
        else:
            return ''

    def _style_markup(self):
        if self.danmaku.style == SCROLL:
            return '\\move({x1}, {y1}, {x2}, {y2})'.format(**self.position)
        else:
            return '\\a6\\pos({x1}, {y1})'.format(**self.position)

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
        return '{' + markup + '}' + content

    def _text(self):
        return DIALOGUE_TPL.format(
            layer=self.layer_markup,
            start=self.start_markup,
            end=self.end_markup,
            content=self.content_markup)

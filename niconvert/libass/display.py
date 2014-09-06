from ..libcore.const import SCROLL, TOP, BOTTOM
from ..libcore.utils import intceil, display_length


class Display(object):
    ''' 显示方式 '''

    def __init__(self, config, danmaku):
        self.config = config
        self.danmaku = danmaku
        self.line_index = 0

        self.font_size = self._font_size()
        self.is_scaled = self._is_scaled()
        self.max_length = self._max_length()
        self.width = self._width()
        self.height = self._height()

        self.horizontal = self._horizontal()
        self.vertical = self._vertical()

        self.duration = self._duration()
        self.leave = self._leave()

    def _font_size(self):
        ''' 字体大小 '''
        # 按用户自定义的字体大小来缩放
        return intceil(self.config.base_font_size * self.danmaku.size_ratio)

    def _is_scaled(self):
        ''' 字体是否被缩放过 '''
        return self.danmaku.size_ratio != 1

    def _max_length(self):
        ''' 最长的行字符数 '''
        return max(map(display_length, self.danmaku.content.split('\n')))

    def _width(self):
        ''' 整条字幕宽度 '''
        char_count = self.max_length / 2
        return intceil(self.font_size * char_count)

    def _height(self):
        ''' 整条字幕高度 '''
        line_count = len(self.danmaku.content.split('\n'))
        return line_count * self.font_size

    def _horizontal(self):
        ''' 出现和消失的水平坐标位置 '''
        # 默认在屏幕中间
        x = self.config.screen_width // 2
        x1, x2 = x, x
        return x1, x2

    def _vertical(self):
        ''' 出现和消失的垂直坐标位置 '''
        # 默认在屏幕中间
        y = self.config.screen_height // 2
        y1, y2 = y, y
        return y1, y2

    def _duration(self):
        ''' 整条字幕的显示时间 '''

        base = 3 + self.config.tune_duration
        if base <= 0:
            base = 0
        char_count = self.max_length / 2

        if char_count < 6:
            value = base + 1
        elif char_count < 12:
            value = base + 2
        else:
            value = base + 3

        return value

    def _leave(self):
        ''' 离开碰撞时间 '''
        return self.danmaku.start + self.duration

    def relayout(self, line_index):
        ''' 按照新的行号重新布局 '''
        self.line_index = line_index
        self.horizontal = self._horizontal()
        self.vertical = self._vertical()


class TopDisplay(Display):
    ''' 顶部 '''

    def _vertical(self):
        # 这里 y 坐标为 0 就是最顶行了
        y = self.line_index * self.config.base_font_size
        y1, y2 = y, y
        return y1, y2


class BottomDisplay(Display):
    ''' 底部 '''

    def _vertical(self):
        # 要让字幕不超出底部，减去高度
        y = self.config.screen_height \
            - (self.line_index * self.config.base_font_size) - self.height

        # 再减去自定义的底部边距
        y -= self.config.bottom_margin
        y1, y2 = y, y
        return y1, y2


class ScrollDisplay(Display):
    ''' 滚动 '''

    def __init__(self, config, danmaku):
        self.config = config
        self.danmaku = danmaku
        self.line_index = 0

        self.font_size = self._font_size()
        self.is_scaled = self._is_scaled()
        self.max_length = self._max_length()
        self.width = self._width()
        self.height = self._height()

        self.horizontal = self._horizontal()
        self.vertical = self._vertical()

        self.distance = self._distance()
        self.speed = self._speed()

        self.duration = self._duration()
        self.leave = self._leave()

    def _horizontal(self):
        # ASS 的水平位置参考点是整条字幕文本的中点
        x1 = self.config.screen_width + self.width // 2
        x2 = -self.width // 2
        return x1, x2

    def _vertical(self):
        base_font_size = self.config.base_font_size

        # 垂直位置，按基准字体大小算每一行的高度
        y = (self.line_index + 1) * base_font_size

        # 个别弹幕可能字体比基准要大，所以最上的一行还要避免挤出顶部屏幕
        # 坐标不能小于字体大小
        if y < self.font_size:
            y = self.font_size

        y1, y2 = y, y
        return y1, y2

    def _distance(self):
        ''' 字幕坐标点的移动距离 '''
        x1, x2 = self.horizontal
        return x1 - x2

    def _speed(self):
        ''' 字幕每个字的移动的速度 '''
        # 基准时间，就是每个字的移动时间
        # 12 秒加上用户自定义的微调
        base = 12 + self.config.tune_duration
        if base <= 0:
            base = 0
        return intceil(self.config.screen_width / base)

    def _sync_duration(self):
        ''' 计算每条弹幕的显示时长，同步方式

        每个弹幕的滚动速度都一样，辨认度好，适合观看剧集类视频。
        '''
        return self.distance / self.speed

    def _async_duration(self):
        ''' 计算每条弹幕的显示时长，异步方式

        每个弹幕的滚动速度都不一样，动态调整，辨认度低，适合观看 MTV 类视频。
        '''

        base = 6 + self.config.tune_duration
        if base <= 0:
            base = 0
        char_count = self.max_length / 2

        if char_count < 6:
            value = base + char_count
        elif char_count < 12:
            value = base + (char_count / 2)
        elif char_count < 24:
            value = base + (char_count / 3)
        else:
            value = base + 10

        return value

    def _duration(self):
        ''' 整条字幕的移动时间 '''
        func_name = '_' + self.config.layout_algorithm + '_duration'
        func = getattr(self, func_name)
        return func()

    def _leave(self):
        ''' 离开碰撞时间 '''

        # 对于滚动样式弹幕来说，就是最后一个字符离开最右边缘的时间
        # 坐标是字幕中点，在屏幕外和内各有半个字幕宽度
        # 也就是跑过一个字幕宽度的路程
        duration = self.width / self.speed
        return self.danmaku.start + duration


def display_factory(config, danmaku):
    ''' 根据弹幕样式自动创建对应的 Display 类 '''
    mapping = {
        SCROLL: ScrollDisplay,
        TOP: TopDisplay,
        BOTTOM: BottomDisplay,
    }
    class_type = mapping[danmaku.style]
    return class_type(config, danmaku)

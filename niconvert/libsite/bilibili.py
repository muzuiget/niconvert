import re

class Danmaku:

    def __init__(self, text):
        self.text = text
        self.raw = self._raw()
        self.start = self._start()
        self.style = self._style()
        self.color = self._color()
        self.commenter = self._commenter()
        self.content = self._content()
        self.size_ratio = self._size_ratio()
        self.is_guest = self._is_guest()

    def _raw(self):
        reg = re.compile('<d p="(.+?)">(.*?)</d>')
        attr_string, content_string = reg.findall(self.text)[0]
        attrs = attr_string.split(',')
        props = {
            'start': float(attrs[0]),
            'style': int(attrs[1]),
            'size': int(attrs[2]),
            'color': int(attrs[3]),
            'publish': int(attrs[4]),
            'pool': int(attrs[5]),  # 弹幕池
            'commenter': attrs[6],
            'uid': attrs[7],  # 此弹幕的唯一识别符
            'content': content_string
        }
        return props

    def _start(self):
        return self.raw['start']

    def _style(self):
        MAPPING = {
            1: 'scroll',
            2: 'scroll',  # 似乎也是滚动弹幕
            3: 'scroll',  # 同上
            4: 'bottom',
            5: 'top',
            6: 'scroll',  # 逆向滚动弹幕，还是当滚动处理
            7: 'none',  # 精准定位，暂时不要考虑
            8: 'none',  # 高级弹幕，暂时不要考虑
        }
        return MAPPING.get(self.raw['style'], 'none')

    def _color(self):
        return self.raw['color']

    def _commenter(self):
        return self.raw['commenter']

    def _content(self):
        return self.raw['content']

    def _size_ratio(self):
        FLASH_PLAYER_FONT_SIZE = 25
        return self.raw['size'] / FLASH_PLAYER_FONT_SIZE

    def _is_guest(self):
        # 以 D 开头都是游客评论
        return self.raw['commenter'].startswith('D')

def loads(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.replace('<d p="', '\n<d p="')
    reg = re.compile('<d .*</d>')
    comments = reg.findall(text)
    danmakus = list(map(Danmaku, comments))
    danmakus.sort(key=lambda x: x.start)
    return danmakus

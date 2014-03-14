import re
from ..libcore.const import NOT_SUPPORT, SCROLL, TOP, BOTTOM
from ..libcore.utils import extract_params
from ..libcore.fetcher import fetch
from ..libcore.danmaku import BaseDanmaku
from ..libcore.video import BaseVideo


class Danmaku(BaseDanmaku):

    def __init__(self, text):
        self.text = text
        self.raw = self._raw()
        # 父类接口
        self.start = self._start()
        self.style = self._style()
        self.color = self._color()
        self.commenter = self._commenter()
        self.content = self._content()
        self.size_ratio = self._size_ratio()
        self.is_guest = self._is_guest()
        self.is_applaud = self._is_applaud()

    def _raw(self):
        reg = re.compile("<d p='(.+?)'><!\[CDATA\[(.*?)\]\]></d>")
        attr_string, content_string = reg.findall(self.text)[0]
        attrs = attr_string.split(',')
        props = {
            'start': float(attrs[0]),
            'style': int(attrs[1]),
            'size': int(attrs[2]),
            'color': int(attrs[3]),
            'publish': int(attrs[4]),
            'content': content_string
        }
        return props

    # 父类接口 #

    def _start(self):
        return self.raw['start']

    def _style(self):
        MAPPING = {
            1: SCROLL,
            2: SCROLL,
            3: SCROLL,
            4: BOTTOM,
            5: TOP,
            6: SCROLL,
            7: NOT_SUPPORT,
            8: NOT_SUPPORT,
        }
        return MAPPING.get(self.raw['style'], NOT_SUPPORT)

    def _color(self):
        return self.raw['color']

    def _commenter(self):
        # 没有可以判断的依据
        return 'blank'

    def _content(self):
        return self.raw['content']

    def _size_ratio(self):
        FLASH_PLAYER_FONT_SIZE = 25
        return self.raw['size'] / FLASH_PLAYER_FONT_SIZE

    def _is_guest(self):
        # 没有可以判断的依据
        return False

    def _is_applaud(self):
        return False


class Video(BaseVideo):

    def __init__(self, config, meta):
        self.config = config
        self.meta = meta
        self.aid = self._aid()
        self.pid = self._pid()
        #print('信息：' + str(self.meta))
        #print('信息：' + str(dict(aid=self.aid, pid=self.pid)))
        # 父类接口
        self.uid = 'pid:' + self.pid
        self.h1 = self._h1()
        self.h2 = self._h2()
        self.title = self._title()
        self.filter = self._filter()
        (self.play_length,
         self.play_urls) = self._play_info()
        self.danmakus = self._danmakus()
        self.feature_start = self._feature_start()

    def _aid(self):
        value = self.meta.get('aid')
        if value is not None:
            return value

        raise Exception('无法获取 aid，请用辅助参数指定')

    def _pid(self):
        return '11-' + self.aid + '-1-0'

    # 父类接口 #

    def _h1(self):
        return self.meta.get('h1', '')

    def _h2(self):
        return self.meta.get('h2', '')

    def _title(self):
        if not self.h1:
            return '未知标题'
        if self.h2:
            return self.h1 + ' - ' + self.h2
        else:
            return self.h1

    def _filter(self):
        # 不做了
        return None

    def _play_info(self):
        # 不做了
        return (0, [])

    def _danmakus(self):
        tpl = 'http://www.tucao.cc/index.php?' + \
              'm=mukio&c=index&a=init&playerID={}&r=205'
        url = tpl.format(self.pid)
        text = fetch(url)
        reg = re.compile('<d .*</d>')
        matches = reg.findall(text)
        orignal_danmakus = map(Danmaku, matches)
        ordered_danmakus = sorted(orignal_danmakus, key=lambda d: d.start)
        return ordered_danmakus

    def _feature_start(self):
        # 不做了
        return 0


class Page(object):

    def __init__(self, url):
        self.url = url
        self.video_class = Video
        self.params = self._params()

    def _params(self):
        abbr_prefix = 'c://'
        normal_prefix = 'http://www.tucao.cc/play/'

        url = self.url
        params = {}

        if url.startswith(abbr_prefix):
            argv = url[len(abbr_prefix):]
            params = extract_params(argv)

        elif url.startswith(normal_prefix):
            params = self.extract_params_from_normal_page(url)

        return params

    def extract_params_from_normal_page(self, url):
        aid_reg = re.compile('/play/h([0-9]+)/')
        h1_reg = re.compile("add_favorite\('(.+?)'\);")
        text = fetch(url)

        params = {}
        params['aid'] = aid_reg.findall(url)[0]
        params['h1'] = h1_reg.findall(text)[0]
        return params

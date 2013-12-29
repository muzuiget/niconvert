import re
import json
from ..libcore.const import NOT_SUPPORT, SCROLL, TOP, BOTTOM
from ..libcore.utils import extract_params
from ..libcore.fetcher import fetch
from ..libcore.danmaku import BaseDanmaku
from ..libcore.video import BaseVideo


class Danmaku(BaseDanmaku):

    def __init__(self, entry):
        self.entry = entry
        self.raw = self._raw()
        # 父类接口
        self.start = self._start()
        self.style = self._style()
        self.color = self._color()
        self.commenter = self._commenter()
        self.content = self._content()
        self.size_ratio = self._size_ratio()
        self.is_guest = self._is_guest()

    def _raw(self):
        attr_string = self.entry['c']
        content_string = self.entry['m']
        attrs = attr_string.split(',')
        props = {
            'start': float(attrs[0]),
            'color': int(attrs[1]),
            'style': int(attrs[2]),
            'size': int(attrs[3]),
            'commenter': attrs[4],
            'publish': int(attrs[5]),
            'content': content_string
        }
        return props

    # 父类接口 #

    def _start(self):
        return self.raw['start']

    def _style(self):
        MAPPING = {
            1: SCROLL,
            2: NOT_SUPPORT,  # 没搜到明确定义
            3: NOT_SUPPORT,  # 同上
            4: BOTTOM,
            5: TOP,
            6: NOT_SUPPORT,  # 没搜到明确定义
            7: NOT_SUPPORT,  # 高级弹幕，暂时不要考虑
            8: NOT_SUPPORT,  # 没搜到明确定义
        }
        return MAPPING.get(self.raw['style'], NOT_SUPPORT)

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
        # 似乎 14 个字符长，还包含英文字母的就是游客
        return len(self.raw['commenter']) == 14


class Video(BaseVideo):

    def __init__(self, config, meta):
        self.config = config
        self.meta = meta
        self.vid = self._vid()
        self.cid = self._cid()
        #print('信息：' + str(self.meta))
        #print('信息：' + str(dict(vid=self.vid, cid=self.cid)))
        # 父类接口
        self.uid = 'vid:{}+cid:{}'.format(self.vid, self.cid)
        self.h1 = self._h1()
        self.h2 = self._h2()
        self.title = self._title()
        self.filter = self._filter()
        (self.play_length,
         self.play_urls) = self._play_info()
        self.danmakus = self._danmakus()
        self.feature_start = self._feature_start()

    def _vid(self):
        value = self.meta.get('vid')
        if value is not None:
            return value
        raise Exception('无法获取 vid，请用辅助参数指定')

    def _cid(self):
        value = self.meta.get('cid')
        if value is not None:
            return value

        url = 'http://www.acfun.tv/api/getVideoByID.aspx?vid=' + self.vid
        text = fetch(url)
        value = json.loads(text).get('cid')
        if value:
            return value

        raise Exception('无法获取 cid，请用辅助参数指定')

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
        tpl = 'http://comment.acfun.tv/{}.json'
        url = tpl.format(self.cid)
        text = fetch(url)
        orignal_danmakus = map(Danmaku, json.loads(text))
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
        abbr_prefix = 'a://'
        normal_prefix = 'http://www.acfun.tv/v/ac'
        comment_prefix = 'http://comment.acfun.tv/'

        url = self.url
        params = {}

        if url.startswith(abbr_prefix):
            argv = url[len(abbr_prefix):]
            params = extract_params(argv)

        elif url.startswith(normal_prefix):
            if '_' not in url:
                url += '_1'
            params = self.extract_params_from_normal_page(url)

        elif url.startswith(comment_prefix):
            vid = ''
            cid = url[len(comment_prefix):-5]
            params = dict(vid=vid, cid=cid)

        return params

    def extract_params_from_normal_page(self, url):
        aid_reg = re.compile('/ac([0-9]+)')
        vid_reg = re.compile('\[video\](.+?)\[/video\]', re.IGNORECASE)
        h1_reg = re.compile('system.title = "(.+?)";')
        text = fetch(url)

        params = {}
        params['aid'] = aid_reg.findall(url)[0]
        params['vid'] = vid_reg.findall(text)[0]
        params['h1'] = h1_reg.findall(text)[0]
        return params

import os
import re
import json
from ..libcore.const import NOT_SUPPORT, SCROLL, TOP, BOTTOM
from ..libcore.utils import extract_params, play_url_fix
from ..libcore.fetcher import fetch
from ..libcore.filter import BaseFilter
from ..libcore.danmaku import BaseDanmaku
from ..libcore.video import BaseVideo


class Filter(BaseFilter):

    def __init__(self, text):
        self.text = text
        (self.keywords,
         self.users) = self._rules()

    def _rules(self):
        struct = json.loads(self.text)['up']
        return struct['keyword'], struct['user']

    def match(self, danmaku):
        if danmaku.commenter in self.users:
            return True
        for keyword in self.keywords:
            if keyword in danmaku.content:
                return True
        return False


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

    # 父类接口 #

    def _start(self):
        return self.raw['start']

    def _style(self):
        MAPPING = {
            1: SCROLL,
            2: SCROLL,  # 似乎也是滚动弹幕
            3: SCROLL,  # 同上
            4: BOTTOM,
            5: TOP,
            6: SCROLL,  # 逆向滚动弹幕，还是当滚动处理
            7: NOT_SUPPORT,  # 精准定位，暂时不要考虑
            8: NOT_SUPPORT,  # 高级弹幕，暂时不要考虑
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
        # 以 D 开头都是游客评论
        return self.raw['commenter'].startswith('D')

    def _is_applaud(self):
        # 不是 0 就是特殊池
        return self.raw['pool'] != 0


class Video(BaseVideo):

    def __init__(self, config, meta):
        self.config = config
        self.meta = meta
        self.cid = self._cid()
        self.aid = self._aid()
        #print('信息：' + str(self.meta))
        #print('信息：' + str(dict(cid=self.cid, aid=self.aid)))
        # 父类接口
        self.uid = 'cid:' + self.cid
        self.h1 = self._h1()
        self.h2 = self._h2()
        self.title = self._title()
        self.filter = self._filter()
        (self.play_length,
         self.play_urls) = self._play_info()
        self.danmakus = self._danmakus()
        self.feature_start = self._feature_start()

    def _cid(self):
        value = self.meta.get('cid')
        if value is not None:
            return value

        ids = []
        for key, value in self.meta.items():
            if key.endswith('id') and key != 'aid':
                ids.append(value)

        reg = re.compile('<chatid>(.+?)</chatid>')
        for id in ids:
            url = 'http://interface.bilibili.com/player?id=' + id
            text = fetch(url)
            matches = reg.findall(text)
            if matches:
                return matches[0]

        raise Exception('无法获取 cid，请用辅助参数指定')

    def _aid(self):
        value = self.meta.get('aid')
        if value is not None:
            return value
        url = 'http://interface.bilibili.com/player?id=cid:' + self.cid
        text = fetch(url)
        reg = re.compile('<aid>(.+?)</aid>')
        matches = reg.findall(text)
        if matches:
            return matches[0]
        else:
            return None

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
        if self.config.disable_video_filter:
            return None
        if not self.aid:
            return None
        tpl = 'http://comment.bilibili.com/cloud/filter/{}.json'
        url = tpl.format(self.aid)
        text = fetch(url)
        return Filter(text)

    def _play_info(self):
        tpl = 'http://interface.bilibili.com/playurl?cid={}'
        url = tpl.format(self.cid)
        text = fetch(url)

        # 有时可能获取不了视频元数据，多重试几次
        tried = 0
        while True:
            if '视频隐藏' not in text or tried >= 5:
                break
            text = fetch(url, True)
            tried += 1

        reg = re.compile('<timelength>(.+?)</timelength>')
        matches = reg.findall(text)
        if matches:
            play_length = int(float(matches[0])) // 1000
        else:
            play_length = 0

        reg = re.compile('<url><!\[CDATA\[(.+?)\]\]></url>')
        matches = reg.findall(text)
        if matches:
            play_urls = map(play_url_fix, matches)
        else:
            play_urls = []
        return play_length, play_urls

    def _danmakus(self):
        tpl = 'http://comment.bilibili.com/{}.xml'
        url = tpl.format(self.cid)
        text = fetch(url)
        reg = re.compile('<d .*</d>')
        matches = reg.findall(text)
        orignal_danmakus = map(Danmaku, matches)
        ordered_danmakus = sorted(orignal_danmakus, key=lambda d: d.start)
        return ordered_danmakus

    def _feature_start(self):
        # 特殊池中，并且是高级弹幕，而且是最前的 10 条弹幕
        reg = re.compile('Player.seek\(([0-9]+?)\);')
        for danmaku in self.danmakus[:10]:
            if not (danmaku.raw['pool'] == 2 and danmaku.raw['style'] == 8):
                continue
            matches = reg.findall(danmaku.content)
            if matches:
                return int(matches[0]) / 1000
        return 0


class Page(object):

    def __init__(self, url):
        self.url = url
        self.video_class = Video
        self.params = self._params()

    def _params(self):
        abbr_prefix = 'b://'
        secure_prefix = 'https://secure.bilibili.com/secure,'
        normal_prefix = 'http://www.bilibili.com/video/av'
        normal1_prefix = 'http://bilibili.kankanews.com/video/av'
        comment_prefix = 'http://comment.bilibili.com/'

        url = self.url
        params = {}

        if url.startswith(abbr_prefix):
            argv = url[len(abbr_prefix):]
            params = extract_params(argv)

        elif url.startswith(secure_prefix):
            argv = url[len(secure_prefix):].replace('&', ',')
            params = extract_params(argv)

        elif url.startswith(normal_prefix) or url.startswith(normal1_prefix):
            if url.endswith('/'):
                url += 'index_1.html'
            params = self.extract_params_from_normal_page(url)

        elif url.startswith(comment_prefix):
            aid = ''
            cid = url[len(comment_prefix):-4]
            params = dict(aid=aid, cid=cid)

        return params

    def extract_params_from_normal_page(self, url):
        aid_reg = re.compile('/av([0-9]+)/')
        cid_reg = re.compile("cid=([0-9]+)|cid:'(.+?)'")
        h1_reg = re.compile('<h2 title="(.+?)">')
        text = fetch(url)

        params = {}
        params['aid'] = aid_reg.findall(url)[0]
        try:
            cid_matches = cid_reg.findall(text)[0]
            params['cid'] = cid_matches[0] or cid_matches[1]
            params['h1'] = h1_reg.findall(text)[0]
        except IndexError:
            print('警告：无法获取 cid，此页面可能需要登录')
        return params


class Part(object):

    def __init__(self, url):
        self.url = url
        self.pages = self._pages()

    def _pages(self):
        text = fetch(self.url)
        reg = re.compile("<option value='(.+?)'(?: selected)?>(.+?)</option>")
        matches = reg.findall(text)
        if not matches:
            raise Exception('此页面没有找到多个分段')

        pages = []
        for link in matches:
            url = self.full_urlify(link[0])
            page = Page(url)
            pages.append(page)
        return pages

    def full_urlify(self, fuzzy_url):
        url = fuzzy_url
        if url.startswith('/'):
            url = 'http://www.bilibili.com' + url
        if fuzzy_url.endswith('/'):
            url += 'index_1.html'
        return url


class LocalVideo(object):

    def __init__(self, config, meta):
        self.config = config
        self.meta = meta
        self.title = self._title()
        self.uid = '0'
        self.danmakus = self._danmakus()
        self.play_length = 0
        self.feature_start = 0
        self.filter = None
        self.play_urls = []

    def _title(self):
        title = os.path.basename(self.meta['path'])
        if '.' in title:
            title = title.split('.')[0]
        return title

    def _danmakus(self):
        path = self.meta['path']
        text = open(path).read()
        reg = re.compile('<d .*</d>')
        matches = reg.findall(text)
        orignal_danmakus = map(Danmaku, matches)
        ordered_danmakus = sorted(orignal_danmakus, key=lambda d: d.start)
        return ordered_danmakus


class LocalPage(object):

    def __init__(self, url):
        self.url = url
        self.video_class = LocalVideo
        self.params = {'path': self.url}

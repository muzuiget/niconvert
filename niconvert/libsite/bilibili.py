import os
import re
import json
from ..libcore.const import NOT_SUPPORT, SCROLL, TOP, BOTTOM
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

    def filter_danmakus(self, danmakus):
        return list(filter(lambda d: not self.match(d), danmakus))


class Danmaku(BaseDanmaku):

    def __init__(self, item):
        self.start = item['start']
        self.style = item['style']
        self.color = int('0x%s' % item['color'], 0)
        self.commenter = item['commenter']
        self.content = item['content']
        self.size_ratio = item.get('size_ratio', 1)
        self.is_guest = item.get('is_guest', False)
        self.is_applaud = item.get('is_applaud', False)

class LocalVideo(object):

    def __init__(self, config, meta):
        self.config = config
        self.meta = meta
        self.title = self._title()
        self.uid = '0'
        self.danmakus = self._danmakus()
        self.play_length = 0
        self.filter = None
        self.play_urls = []

    def _title(self):
        title = os.path.basename(self.meta['path'])
        if '.' in title:
            title = title.split('.')[0]
        return title

    def _danmakus(self):
        path = self.meta['path']
        with open(path) as file:
            text = file.read()
        matches = json.loads(text)
        orignal_danmakus = map(Danmaku, matches)
        ordered_danmakus = sorted(orignal_danmakus, key=lambda d: d.start)
        return ordered_danmakus


class LocalPage(object):

    def __init__(self, url):
        self.url = url
        self.video_class = LocalVideo
        self.params = {'path': self.url}

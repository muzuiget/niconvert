import json
from niconvert.libcore.filter import BaseFilter

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


class Danmaku:

    def __init__(self, item):
        self.start = item['start']
        self.style = item['style']
        self.color = int('0x%s' % item['color'], 0)
        self.commenter = item['commenter']
        self.content = item['content']
        self.size_ratio = item.get('size_ratio', 1)
        self.is_guest = item.get('is_guest', False)

class LocalVideo:

    def __init__(self, input_filename):
        self.input_filename = input_filename
        self.danmakus = self._danmakus()

    def _danmakus(self):
        with open(self.input_filename) as file:
            text = file.read()
        matches = json.loads(text)
        orignal_danmakus = map(Danmaku, matches)
        ordered_danmakus = sorted(orignal_danmakus, key=lambda d: d.start)
        return ordered_danmakus

class LocalPage:

    def __init__(self, url):
        self.url = url
        self.video_class = LocalVideo
        self.params = {'path': self.url}

import json

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

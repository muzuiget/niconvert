import json
from niconvert.libsite.config import Config

class Danmaku:

    def __init__(self, item):
        self.start = item['start']
        self.style = item['style']
        self.color = int('0x%s' % item['color'], 0)
        self.commenter = item['commenter']
        self.content = item['content']
        self.size_ratio = item.get('size_ratio', 1)
        self.is_guest = item.get('is_guest', False)

class Producer:

    def __init__(self, args, input_filename):
        self.config = Config(args)
        self.input_filename = input_filename

    def start_handle(self):
        self.load_json_danmakus()
        self.init_filter_danmakus()

    def load_json_danmakus(self):
        with open(self.input_filename) as file:
            text = file.read()
        items = json.loads(text)
        self.all_danmakus = list(map(Danmaku, items))

    def init_filter_danmakus(self):
        filter_detail = dict(
            bottom=0,
            custom=0,
            guest=0,
            top=0,
        )

        danmakus = self.all_danmakus
        orders = ['guest', 'top', 'bottom', 'custom']
        for name in orders:
            filter_obj = getattr(self.config, 'get_%s_filter' % name)()
            if filter_obj is not None:
                count = len(danmakus)
                danmakus = filter_obj.filter_danmakus(danmakus)
                filter_detail[name] = count - len(danmakus)

        self.keeped_danmakus = danmakus
        self.filter_detail = filter_detail
        self.blocked_count = sum(filter_detail.values())
        self.passed_count = len(danmakus)
        self.total_count = self.blocked_count + self.passed_count

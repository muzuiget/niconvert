import json
from niconvert.libsite import filters, bilibili

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

    def __init__(self, config, input_filename):
        self.config = config
        self.input_filename = input_filename

    def start_handle(self):
        self.load_input_file()
        self.load_filter_objs()
        self.apply_filter_objs()

    def load_input_file(self):
        path = self.input_filename
        if path.endswith('.xml'):
            self.all_danmakus = bilibili.loads(path)
            return
        self.load_json_file()

    def load_json_file(self):
        with open(self.input_filename, 'r', encoding='utf-8') as file:
            text = file.read()
        items = json.loads(text)
        self.all_danmakus = list(map(Danmaku, items))

    def load_filter_objs(self):
        config = self.config
        objs = {}

        if config.get('guest_filter', False):
            objs['guest'] = filters.GuestFilter()
        if config.get('top_filter', False):
            objs['top'] = filters.TopFilter()
        if config.get('bottom_filter', False):
            objs['bottom'] = filters.BottomFilter()

        path = config.get('custom_filter')
        if path is not None:
            if path.endswith('.py'):
                obj = filters.CustomPythonFilter(path)
            else:
                obj = filters.CustomSimpleFilter(path)
            objs['custom'] = obj
        self.filter_objs = objs

    def apply_filter_objs(self):
        filter_detail = dict(
            bottom=0,
            custom=0,
            guest=0,
            top=0,
        )

        danmakus = self.all_danmakus
        orders = ['guest', 'top', 'bottom', 'custom']
        for name in orders:
            filter_obj = self.filter_objs.get(name)
            if filter_obj is not None:
                count = len(danmakus)
                danmakus = filter_obj.do_filter(danmakus)
                filter_detail[name] = count - len(danmakus)

        self.keeped_danmakus = danmakus
        self.filter_detail = filter_detail

    def report(self):
        blocked_count = sum(self.filter_detail.values())
        passed_count = len(self.keeped_danmakus)
        total_count = blocked_count + passed_count
        ret = {
            'blocked': blocked_count,
            'passed': passed_count,
            'total': total_count,
        }
        ret.update(self.filter_detail)
        return ret

from .config import Config
from .bilibili import (LocalPage as BilibiliLocalPage)

def make_video(page, input_filename):
    return page.video_class(input_filename)

class Producer:

    def __init__(self, args, input_filename):
        self.config = Config(args)
        self.input_filename = input_filename
        self.page = None
        self.video = None

    def start_download(self):
        self.page = BilibiliLocalPage(self.input_filename)
        self.video = make_video(self.page, self.input_filename)

    def start_handle(self):
        self.init_filter_danmakus()

    def init_filter_danmakus(self):
        filter_detail = dict(
            custom=0,
            guest=0,
            video=0,
            top=0,
            bottom=0,
        )

        custom_filter = self.config.get_custom_filter()
        guest_filter = self.config.get_guest_filter()
        top_filter = self.config.get_top_filter()
        bottom_filter = self.config.get_bottom_filter()
        video_filter = self.video.filter
        danmakus = self.video.danmakus

        if custom_filter is not None:
            count = len(danmakus)
            danmakus = custom_filter.filter_danmakus(danmakus)
            filter_detail['custom'] = count - len(danmakus)

        if guest_filter is not None:
            count = len(danmakus)
            danmakus = guest_filter.filter_danmakus(danmakus)
            filter_detail['guest'] = count - len(danmakus)

        if video_filter is not None:
            count = len(danmakus)
            danmakus = video_filter.filter_danmakus(danmakus)
            filter_detail['video'] = count - len(danmakus)

        if top_filter is not None:
            count = len(danmakus)
            danmakus = top_filter.filter_danmakus(danmakus)
            filter_detail['top'] = count - len(danmakus)

        if bottom_filter is not None:
            count = len(danmakus)
            danmakus = bottom_filter.filter_danmakus(danmakus)
            filter_detail['bottom'] = count - len(danmakus)

        self.keeped_danmakus = danmakus
        self.filter_detail = filter_detail
        self.blocked_count = sum(filter_detail.values())
        self.passed_count = len(danmakus)
        self.total_count = self.blocked_count + self.passed_count

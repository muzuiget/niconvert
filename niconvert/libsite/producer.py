from .config import Config
from .bilibili import (LocalPage as BilibiliLocalPage)


def make_local_page(url):
    page = None
    if 'json' in url:
        page = BilibiliLocalPage(url)
    if page is None:
        raise Exception('不支持的文件')
    return page


def make_page(url):
    return make_local_page(url)


def make_video(config, page):
    meta = page.params.copy()
    return page.video_class(config, meta)


class Producer:

    def __init__(self, args, bootstrap_url):
        self.config = Config(args)
        self.bootstrap_url = bootstrap_url
        self.page = None
        self.video = None
        self.title = '未知标题'

    def start_download(self):
        self.page = make_page(self.bootstrap_url)
        self.video = make_video(self.config, self.page)
        self.title = self.video.title

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

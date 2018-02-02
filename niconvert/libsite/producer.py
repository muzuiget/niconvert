import os
from .config import Config
from .bilibili import (Page as BilibiliPage, LocalPage as BilibiliLocalPage)


def make_normal_page(url):
    page = None
    if 'bilibili' in url:
        page = BilibiliPage(url)
    if page is None:
        raise Exception('不支持的网址')
    return page


def make_local_page(url):
    page = None
    if 'xml' in url:
        page = BilibiliLocalPage(url)
    if page is None:
        raise Exception('不支持的文件')
    return page


def make_page(url):
    if os.path.exists(url):
        return make_local_page(url)
    return make_normal_page(url)


def make_video(config, page):
    meta = page.params.copy()
    return page.video_class(config, meta)


class ProxyDanmaku(object):
    ''' 代理弹幕类

    解决补丁这种蛋疼情况
    '''

    def __init__(self, danmaku, offset):
        self.danmaku = danmaku
        self.offset = offset
        self.start = self._start()

    def _start(self):
        return self.danmaku.start + self.offset

    def __getattr__(self, name):
        return getattr(self.danmaku, name)


class Producer(object):

    def __init__(self, args, bootstrap_url):
        self.config = Config(args)
        self.bootstrap_url = bootstrap_url

        self.title = '未知标题'
        self.pages = []
        self.videos = []

    def start_download(self):
        self.pages = [make_page(self.bootstrap_url)]

        self.videos = []
        for page in self.pages:
            video = make_video(self.config, page)
            self.videos.append(video)

        video = self.videos[0]
        self.title = video.title

    def start_handle(self):
        self.init_filter_danmakus()

    def init_filter_danmakus(self):
        keeped_danmakus = []
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

        for video in self.videos:
            video_filter = video.filter
            danmakus = video.danmakus

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

            keeped_danmakus.extend(danmakus)

        self.keeped_danmakus = keeped_danmakus
        self.filter_detail = filter_detail
        self.blocked_count = sum(filter_detail.values())
        self.passed_count = len(keeped_danmakus)
        self.total_count = self.blocked_count + self.passed_count

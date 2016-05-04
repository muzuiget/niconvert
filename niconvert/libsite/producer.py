import os
from ..libcore.filter import guest_filter, top_filter, bottom_filter
from .config import Config
from .bilibili import (
    Page as BilibiliPage, LocalPage as BilibiliLocalPage,
    Part as BilibiliPart)
from .acfun import Page as AcfunPage, LocalPage as AcfunLocalPage


def make_normal_page(url):
    page = None
    if url.startswith('b://') or 'bilibili' in url:
        page = BilibiliPage(url)
    elif url.startswith('a://') or 'acfun' in url:
        page = AcfunPage(url)
    if page is None:
        raise Exception('不支持的网址')
    return page


def make_local_page(url):
    page = None
    if 'xml' in url:
        page = BilibiliLocalPage(url)
    if 'json' in url:
        page = AcfunLocalPage(url)
    if page is None:
        raise Exception('不支持的文件')
    return page


def make_page(url):
    if os.path.exists(url):
        return make_local_page(url)
    else:
        return make_normal_page(url)


def make_part_pages(url):
    prefixes = ['http://www.bilibili.com/video/av',
                'http://bilibili.kankanews.com/video/av']
    for prefix in prefixes:
        if url.startswith(prefix):
            return BilibiliPart(url).pages
    raise Exception('此网址不支持自动合并分段')


def make_video(config, page):
    meta = page.params.copy()
    meta.update(config.assist_params)
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
        if self.config.merge_parts:
            self.pages = make_part_pages(self.bootstrap_url)
        else:
            self.pages = [make_page(self.bootstrap_url)]

        self.videos = []
        for page in self.pages:
            video = make_video(self.config, page)
            self.videos.append(video)

        video = self.videos[0]
        if self.config.merge_parts:
            self.title = video.h1
        else:
            self.title = video.title

    def start_handle(self):
        self.init_filter_danmakus()

    def init_filter_danmakus(self):
        keeped_danmakus = []
        filter_detail = dict(
            top=0,
            bottom=0,
            guest=0,
            video=0,
            custom=0
        )

        custom_filter = self.config.custom_filter
        part_offset = 0
        for i, video in enumerate(self.videos):

            # 处理偏移 #
            offset = 0

            # 合并分段
            if self.config.merge_parts:
                if i != 0:
                    prev_video = self.videos[i - 1]
                    part_offset += prev_video.play_length
                    offset = part_offset

            # 跳过补丁
            if self.config.skip_patch:
                offset -= video.feature_start

            # 处理过滤 #

            for danmaku in video.danmakus:

                if not self.config.disable_guest_filter:
                    if guest_filter.match(danmaku):
                        filter_detail['guest'] += 1
                        continue
                if not self.config.disable_top_filter:
                    if top_filter.match(danmaku):
                        filter_detail['top'] += 1
                        continue
                if not self.config.disable_bottom_filter:
                    if bottom_filter.match(danmaku):
                        filter_detail['bottom'] += 1
                        continue
                if not self.config.disable_video_filter:
                    if video.filter and video.filter.match(danmaku):
                        filter_detail['video'] += 1
                        continue
                if custom_filter:
                    if custom_filter.match(danmaku):
                        filter_detail['custom'] += 1
                        continue

                # 算上偏移加入保留列表中
                danmaku = ProxyDanmaku(danmaku, offset)
                keeped_danmakus.append(danmaku)

        self.keeped_danmakus = keeped_danmakus
        self.filter_detail = filter_detail
        self.blocked_count = sum(filter_detail.values())
        self.passed_count = len(keeped_danmakus)
        self.total_count = self.blocked_count + self.passed_count

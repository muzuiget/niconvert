import sys
from os.path import join, isdir, basename
from .config import Config
from .creater import Creater


class Studio(object):
    ''' 字幕工程类 '''

    def __init__(self, args, producer):
        self.config = Config(args)
        self.producer = producer

    def start_handle(self):
        self.ass_danmakus = self._ass_danmakus()
        self.creater = self._creater()
        self.keeped_count = self._keep_count()
        self.droped_count = self._droped_count()
        self.play_urls = self._play_urls()

    def _ass_danmakus(self):
        ''' 创建输出 ass 的弹幕列表 '''
        return self.producer.keeped_danmakus

    def _creater(self):
        ''' ass 创建器 '''
        return Creater(self.config, self.ass_danmakus)

    def _keep_count(self):
        ''' 保留条数 '''
        return len(self.creater.subtitles)

    def _droped_count(self):
        ''' 丢弃条数 '''
        return len(self.ass_danmakus) - self.keeped_count

    def create_ass_file(self, filename):
        ''' 创建 ass 字幕 '''
        default_filename = self.default_filename('.ass')
        if filename is None:
            filename = default_filename
        elif isdir(filename):
            filename = join(filename, default_filename)
        elif not filename.endswith('.ass'):
            filename += '.ass'

        self.create_file(filename, self.creater.text)
        return basename(filename)

    def _play_urls(self):
        ''' 播放地址 '''
        urls = []
        for video in self.producer.videos:
            urls.extend(video.play_urls)
        return urls

    def create_m3u_file(self, filename):
        ''' 创建 m3u 播放列表 '''
        default_filename = self.default_filename('.m3u')
        if filename is None:
            filename = default_filename
        elif isdir(filename):
            filename = join(filename, default_filename)
        else:
            if filename.endswith('.ass'):
                filename = filename[:-4] + '.m3u'
            else:
                filename += '.m3u'

        if not self.play_urls:
            return ''

        text = '\n'.join(self.play_urls)
        self.create_file(filename, text)
        return basename(filename)

    def default_filename(self, suffix):
        ''' 创建文件全名 '''
        video_title = self.producer.title.replace('/', ' ')
        filename = video_title + suffix
        return filename

    def create_file(self, filename, text):
        with open(filename, 'wb') as file:
            if sys.platform.startswith('win'):
                text = text.replace('\n', '\r\n')
            text = text.encode('utf-8')
            file.write(text)

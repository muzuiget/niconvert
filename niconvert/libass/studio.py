import sys
from niconvert.libass.config import Config
from niconvert.libass.creater import Creater

class Studio:
    ''' 字幕工程类 '''

    def __init__(self, args, producer):
        self.config = Config(args)
        self.producer = producer

    def start_handle(self):
        self.ass_danmakus = self._ass_danmakus()
        self.creater = self._creater()
        self.keeped_count = self._keep_count()
        self.droped_count = self._droped_count()

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
        self.create_file(filename, self.creater.text)

    def create_file(self, filename, text):
        with open(filename, 'wb') as file:
            if sys.platform.startswith('win'):
                text = text.replace('\n', '\r\n')
            text = text.encode('utf-8')
            file.write(text)

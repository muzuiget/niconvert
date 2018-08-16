from niconvert.libass.config import Config
from niconvert.libass.creater import Creater

class Studio:
    ''' 字幕工程类 '''

    def __init__(self, args, danmakus):
        self.config = Config(args)
        self.danmakus = danmakus

    def start_handle(self):
        self.creater = self._creater()
        self.keeped_count = self._keep_count()
        self.droped_count = self._droped_count()

    def _creater(self):
        ''' ass 创建器 '''
        return Creater(self.config, self.danmakus)

    def _keep_count(self):
        ''' 保留条数 '''
        return len(self.creater.subtitles)

    def _droped_count(self):
        ''' 丢弃条数 '''
        return len(self.danmakus) - self.keeped_count

    def create_ass_file(self, filename):
        ''' 创建 ass 字幕 '''
        self.create_file(filename, self.creater.text)

    def create_file(self, filename, text):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)

    def report(self):
        return {
            'total': len(self.danmakus),
            'droped': self.droped_count,
            'keeped': self.keeped_count,
        }

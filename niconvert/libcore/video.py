class BaseVideo(object):
    ''' 视频基类 '''

    def __init__(self):

        # 唯一识别符号
        self.uid = ''

        # 视频标题
        self.h1 = ''
        self.h2 = ''
        self.title = '未知标题'

        # 过滤器
        self.filter = None

        # 视频长度
        self.play_length = 0

        # 视频地址
        self.play_urls = []

        # 弹幕列表
        self.danmakus = []

        # 正片位置
        self.feature_start = 0


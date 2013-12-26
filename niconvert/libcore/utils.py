import re
import colorsys
from math import ceil
from urllib.parse import unquote
from unicodedata import east_asian_width


def intceil(number):
    ''' 向上取整 '''
    return int(ceil(number))


def display_length(text):
    ''' 字符长度，1 个汉字当 2 个英文 '''
    width = 0
    for char in text:
        width += east_asian_width(char) == 'Na' and 1 or 2
    return width


def correct_typos(text):
    ''' 修正一些评论者的拼写错误 '''

    # 错误的换行转义
    text = text.replace('/n', '\\N')
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')

    return text


def s2hms(seconds):
    ''' 秒数转 时:分:秒 格式 '''
    if seconds < 0:
        return '0:00:00.00'

    i, d = divmod(seconds, 1)
    m, s = divmod(i, 60)
    h, m = divmod(m, 60)
    (h, m, s, d) = map(int, (h, m, s, d * 100))
    return '{:d}:{:02d}:{:02d}.{:02d}'.format(h, m, s, d)


def hms2s(hms):
    ''' 时:分:秒 格式转 秒数 '''

    nums = hms.split(':')
    seconds = 0
    for i in range(len(nums)):
        seconds += int(nums[-i - 1]) * (60 ** i)
    return seconds


def xhms2s(xhms):
    ''' 同上，不过可以用 +/- 符号来连接多个

    即 3:00-2:30 相当于 30 秒
    '''

    args = xhms.replace('+', ' +').replace('-', ' -').split(' ')
    result = 0
    for hms in args:
        seconds = hms2s(hms)
        result += seconds
    return result


def int2rgb(integer):
    ''' 颜色值，整型转 RGB '''
    return hex(integer).upper()[2:].zfill(6)


def int2bgr(integer):
    ''' 颜色值，整型转 BGR '''
    rgb = int2rgb(integer)
    bgr = rgb[4:6] + rgb[2:4] + rgb[0:2]
    return bgr


def int2hls(integer):
    ''' 颜色值，整型转 HLS '''
    rgb = int2rgb(integer)
    rgb_decimals = map(lambda x: int(x, 16), (rgb[0:2], rgb[2:4], rgb[4:6]))
    rgb_coordinates = map(lambda x: x // 255, rgb_decimals)
    hls_corrdinates = colorsys.rgb_to_hls(*rgb_coordinates)
    hls = (
        hls_corrdinates[0] * 360,
        hls_corrdinates[1] * 100,
        hls_corrdinates[2] * 100
    )
    return hls


def is_dark(integer):
    ''' 是否属于暗色 '''
    if integer == 0:
        return True

    hls = int2hls(integer)
    hue, lightness = hls[0:2]

    # HSL 色轮见
    # http://zh.wikipedia.org/zh-cn/HSL和HSV色彩空间
    # 以下的数值都是我的主观判断认为是暗色
    if (hue > 30 and hue < 210) and lightness < 33:
        return True
    if (hue < 30 or hue > 210) and lightness < 66:
        return True

    return False


def extract_params(argv):
    ''' 转换网址参数字符串为字典对象 '''
    argv = unquote(argv)
    params = {}
    for arg in argv.split(','):
        key, value = arg.split('=')
        params[key] = value
    return params


def play_url_fix(url):
    ''' 视频地址修复 '''
    # 不知道为毛我不能解析 videoctfs.tc.qq.com 这个域名，即是用电信的 DNS 也是，
    # 但是通过抓包分析，Flash 播放器获取时就变成 IP 了，
    # 似乎是硬编码直接替换过的。
    if url.startswith('http://videoctfs.tc.qq.com/'):
        return url.replace('http://videoctfs.tc.qq.com/',
                           'http://183.60.73.103/', 1)

    # 默认这个会返回 403
    if url.startswith('http://vhot2.qqvideo.tc.qq.com/'):
        key_part = re.findall(
            'http://vhot2.qqvideo.tc.qq.com/(.+?)\?.*', url)[0]
        url = 'http://vsrc.store.qq.com/{}?'.format(key_part)
        url += 'channel=vhot2&sdtfrom=v2&r=256&rfc=v10'
        return url

    return url

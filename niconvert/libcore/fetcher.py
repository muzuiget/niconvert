import gzip
import zlib
from urllib import request
from io import BytesIO


USER_AGENT = \
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'


class Fetcher(object):

    def __init__(self):
        self.opener = self._opener()
        self.cache = {}

    def _opener(self):
        opener = request.build_opener()
        opener.addheaders = [
            ('User-Agent', USER_AGENT),
            ('Accept-Encoding', 'gzip')
        ]
        return opener

    def decompression(self, content, encoding):
        if encoding == 'gzip':
            return gzip.GzipFile(fileobj=BytesIO(content), mode='rb').read()
        elif encoding == 'deflate':
            return zlib.decompressobj(-zlib.MAX_WBITS).decompress(content)
        else:
            return content

    def download(self, url, data):
        if data:
            resp = self.opener.open(url, data.encode('utf-8'))
        else:
            resp = self.opener.open(url)
        content = resp.read()
        encoding = resp.headers.get('content-encoding', None)
        return self.decompression(content, encoding).decode('UTF-8')

    def open(self, url, force=False, data=None):
        text = self.cache.get(url)
        if force or text is None:
            print('下载：' + str(url))
            text = self.download(url, data)
            self.cache[url] = text
        else:
            print('重用：' + str(url))
        return text


fetch = Fetcher().open

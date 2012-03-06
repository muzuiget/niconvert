#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time

from bottle import get, post, run, request, template, response
from niconvert import create_website

with open('niconvert_web.html') as htmlfile:
    page_template = htmlfile.read().decode('UTF-8')

class Cache:

    def __init__(self, size=1000, expire=3600):
        self.size = size
        self.expire = expire

        self.objects = {}
        self.timestamps = {}
        self.keys = []

    def set(self, key, value):
        if len(self.timestamps) >= self.size:
            key = self.keys[0]
            self.delete(key)

        self.objects[key] = value
        self.timestamps[key] = time()
        self.keys.append(key)

    def get(self, key):
        if key not in self.timestamps:
            return None

        timestamp = self.timestamps[key]
        if time() - timestamp > self.expire:
            return None
        
        return self.objects[key]

    def delete(self, key):
        if key in self.objects:
            del self.objects[key]
        if key in self.timestamps:
            del self.timestamps[key]
        if key in self.keys:
            self.keys.remove(key)

cache = Cache()

def create_website_with_cache(url): 
    website = cache.get(url)
    if website is not None:
        return website

    try:
        website = create_website(url)
    except:
        raise StandardError(u"解析失败，可能是视频地址或服务器错误")

    if website is None:
        raise StandardError(u"不支持的网站")
    else:
        cache.set(url, website)
    return website

@get('/')
def setting():
    url = request.params.get('url', '')
    if url == "":
        return template(page_template)

    try:
        website = create_website_with_cache(url)
    except StandardError as error:
        message = error.message
        return template(page_template, message=message)
    
    user_agent = request.headers.get('User-Agent', '')
    if user_agent.find('Linux') != -1:
        default_font_name = "WenQuanYi Micro Hei"
    else:
        default_font_name = "微软雅黑"

    return template(page_template, 
                    url=url,
                    video_title=website.downloader.title,
                    default_font_name=default_font_name,
                    comment_url=website.downloader.comment_url)

@post('/')
def download():
    url = request.forms.get('url')
    font_name = request.forms.get('font_name').strip().decode("UTF-8")

    try:
        font_size = int(request.forms.get('font_size'))
        video_width = int(request.forms.get('video_width'))
        video_height = int(request.forms.get('video_height'))
        line_count = int(request.forms.get('line_count'))
    except ValueError:
        message = '除字体名称外，其它选项必须为数字'
        return template(page_template, message=message)

    try:
        website = create_website_with_cache(url)
    except StandardError as error:
        message = error.message
        return template(page_template, message=message)

    user_agent = request.headers.get('User-Agent', '')
    if user_agent.find('Windows') != -1:
        filename = website.downloader.title.encode("GBK") + '.ass'
    else:
        filename = website.downloader.title.encode("UTF-8") + '.ass'

    response.set_header('Content-Disposition', 'attachment; filename="%s"' % filename)
    response.set_header('Content-Type', 'text/plain; charset=utf-8')

    return website.ass_subtitles_text(
            font_name=font_name,
            font_size=font_size, 
            resolution="%d:%d" % (video_width, video_height),
            line_count=line_count
    )

def main():
    run(host='127.0.0.1', port=8624)

if __name__ == '__main__':
    main()

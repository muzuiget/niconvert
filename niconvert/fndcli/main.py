from ..libsite.producer import Producer
from ..libass.studio import Studio
from .argpaser import argpaser


def parseargs():
    namespace = argpaser.parse_args()

    io_keys = ('path', 'output_filename')
    danmaku_keys = (
        'custom_filter',
        'disable_top_filter', 'disable_bottom_filter',
        'disable_guest_filter',
    )
    subtitle_keys = (
        'play_resolution', 'font_name', 'font_size',
        'line_count', 'layout_algorithm', 'tune_duration',
        'drop_offset', 'bottom_margin', 'custom_offset', 'header_file'
    )

    create_args = lambda keys: {k: getattr(namespace, k) for k in keys}
    io_args = create_args(io_keys)
    danmaku_args = create_args(danmaku_keys)
    subtitle_args = create_args(subtitle_keys)
    return io_args, danmaku_args, subtitle_args


def convert(io_args, danmaku_args, subtitle_args):
    path = io_args['path']
    output_filename = io_args['output_filename']

    producer = Producer(danmaku_args, path)

    producer.start_download()
    print()

    producer.start_handle()
    print('屏蔽条数：顶部({top}) + 底部({bottom}) + '
          '游客({guest}) + 云屏蔽({video}) + 自定义({custom}) = {}'
          .format(producer.blocked_count, **producer.filter_detail))
    print('通过条数：总共({0.total_count}) - 屏蔽({0.blocked_count}) = '
          '{0.passed_count}'.format(producer))

    studio = Studio(subtitle_args, producer)
    studio.start_handle()

    print('字幕条数：总共({0}) - 丢弃({1.droped_count}) = '
          '{1.keeped_count}'
          .format(len(studio.ass_danmakus), studio))
    print('字幕文件：' + studio.create_ass_file(output_filename))
    print()


def main():
    convert(*parseargs())

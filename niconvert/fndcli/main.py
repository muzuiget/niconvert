import os
from niconvert.fndcli.argpaser import argpaser
from niconvert.libsite.producer import Producer
from niconvert.libass.studio import Studio

def parse_args():
    io_keys = (
        'input_filename',
        'output_filename',
    )
    danmaku_keys = (
        'custom_filter',
        'disable_bottom_filter',
        'disable_guest_filter',
        'disable_top_filter',
    )
    subtitle_keys = (
        'bottom_margin',
        'custom_offset',
        'drop_offset',
        'font_name',
        'font_size',
        'header_file',
        'layout_algorithm',
        'line_count',
        'play_resolution',
        'tune_duration',
    )

    namespace = argpaser.parse_args()
    create_args = lambda v: {k: getattr(namespace, k) for k in v}
    io_args = create_args(io_keys)
    danmaku_args = create_args(danmaku_keys)
    subtitle_args = create_args(subtitle_keys)
    return io_args, danmaku_args, subtitle_args

def convert(io_args, danmaku_args, subtitle_args):
    input_filename = io_args['input_filename']
    output_filename = io_args['output_filename']

    producer = Producer(danmaku_args, input_filename)
    producer.start_handle()
    print('屏蔽条数：顶部({top}) + 底部({bottom}) + '
          '游客({guest}) + 自定义({custom}) = {}'
          .format(producer.blocked_count, **producer.filter_detail))
    print('通过条数：总共({0.total_count}) - 屏蔽({0.blocked_count}) = '
          '{0.passed_count}'.format(producer))

    studio = Studio(subtitle_args, producer)
    studio.start_handle()

    print('字幕条数：总共({0}) - 丢弃({1.droped_count}) = '
          '{1.keeped_count}'
          .format(len(studio.ass_danmakus), studio))

    studio.create_ass_file(output_filename)
    print('字幕文件：' + os.path.basename(output_filename))
    print()

def main():
    convert(*parse_args())

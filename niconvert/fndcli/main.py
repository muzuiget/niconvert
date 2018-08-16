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
        'bottom_filter',
        'guest_filter',
        'top_filter',
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

    # 弹幕预处理
    producer = Producer(danmaku_args, input_filename)
    producer.start_handle()
    print('屏蔽条数：游客(%(guest)d) + 顶部(%(top)d) + '
          '底部(%(bottom)d) + 自定义(%(custom)d) = %(blocked)d\n'
          '通过条数：总共(%(total)d) - 屏蔽(%(blocked)d) = %(passed)d'
          % producer.report())

    # 字幕生成
    danmakus = producer.keeped_danmakus
    studio = Studio(subtitle_args, danmakus)
    studio.start_handle()
    studio.create_ass_file(output_filename)
    print('字幕条数：总共(%(total)d) - 丢弃(%(droped)d) = %(keeped)d' %
          studio.report())
    print('字幕文件：%s' % os.path.basename(output_filename))

def main():
    convert(*parse_args())

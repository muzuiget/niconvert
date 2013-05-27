# -*- coding: utf-8 -*-
from niconvert import *

#Convert from xml string and return an ass string.
def convert(input,resolution,font_name,font_size,line_count,bottom_margin,shift):
    XML_NODE_RE = re.compile('<d p="([^"]*)">([^<]*)</d>')
    nico_subtitles = []
    nico_subtitle_lines = XML_NODE_RE.findall(input)
    for line in nico_subtitle_lines:
        attributes = line[0].split(',')

        nico_subtitle = NicoSubtitle()
        nico_subtitle.start_seconds = float(attributes[0])
        nico_subtitle.style = NicoSubtitle.to_style(int(attributes[1]))
        nico_subtitle.font_size = int(attributes[2])
        nico_subtitle.font_color = NicoSubtitle.to_bgr(int(attributes[3]))
        nico_subtitle.white_border = NicoSubtitle.need_white_border(int(attributes[3]))
		#nico_subtitle.text = line[1].decode('UTF-8').replace('/n', '\\N')
        nico_subtitle.text = line[1].replace('/n', '\\N')

        if nico_subtitle.style != NicoSubtitle.NOT_SUPPORT:
            nico_subtitles.append(nico_subtitle)
    nico_subtitles.sort(key=lambda x: x.start_seconds)

    for i, nico_subtitle in enumerate(nico_subtitles):
        nico_subtitle.index = i


    video_width, video_height = map(int, resolution.split(':'))

    ass_subtitles = []
    for nico_subtitle in nico_subtitles:
        ass_subtitle = AssSubtitle(nico_subtitle,
                                    video_width, video_height,
                                    font_size, line_count,
                                    bottom_margin, shift)
        ass_subtitles.append(ass_subtitle)

    ass_lines = []
    for ass_subtitle in ass_subtitles:
        ass_lines.append(ass_subtitle.ass_line)

    ass_header = ASS_HEADER_TPL % dict(video_width=video_width,
                                        video_height=video_height,
                                        font_name=font_name,
                                        font_size=font_size)
    text = ass_header + '\n'.join(ass_lines)

    return text
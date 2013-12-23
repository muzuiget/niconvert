import os
import sys
from .tkmodules import tk, ttk, tku


class SubtitleFrame(ttk.LabelFrame):

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='字幕选项', padding=2)
        self.pack(fill=tk.BOTH)
        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.init_play_resolution_widgets()
        self.init_font_name_widgets()
        self.init_font_size_widgets()
        self.init_line_count_widgets()
        self.init_layout_algorithm_widgets()
        self.init_tune_duration_widgets()
        self.init_drop_offset_widgets()
        self.init_bottom_margin_widgets()
        self.init_custom_offset_widgets()
        self.init_header_file_widgets()
        tku.add_border_space(self, 1, 1)

    def init_play_resolution_widgets(self):
        label = ttk.Label(self, text='分辨率：')
        box = ResolutionBox(self)
        label1 = ttk.Label(self, text='像素')

        label.grid(row=0, column=0, sticky=tk.E)
        box.grid(row=0, column=1, sticky=tk.EW)
        label1.grid(row=0, column=2, sticky=tk.W)

        box.set('1920x1080')
        self.play_resolution_box = box

    def init_font_name_widgets(self):
        fonts = list(tk.font.families(self))
        fonts = list(set(fonts))
        fonts.sort()

        strvar = tk.StringVar()
        label = ttk.Label(self, text='字体名称：')
        combobox = ttk.Combobox(self, textvariable=strvar, values=fonts)

        label.grid(row=1, column=0, sticky=tk.E)
        combobox.grid(row=1, column=1, sticky=tk.EW, columnspan=2)

        if sys.platform == 'linux':
            strvar.set('WenQuanYi Micro Hei')
        else:
            strvar.set('微软雅黑')

        self.font_name_strvar = strvar

    def init_font_size_widgets(self):
        label = ttk.Label(self, text='字体大小：')
        spinbox = tk.Spinbox(self, justify=tk.RIGHT, from_=1, to=100)
        label1 = ttk.Label(self, text='像素')

        label.grid(row=2, column=0, sticky=tk.E)
        spinbox.grid(row=2, column=1, sticky=tk.EW)
        label1.grid(row=2, column=2, sticky=tk.W)

        spinbox.delete(0, tk.END)
        spinbox.insert(0, 32)
        self.font_size_spinbox = spinbox

    def init_line_count_widgets(self):
        label = ttk.Label(self, text='限制行数：')
        spinbox = tk.Spinbox(self, justify=tk.RIGHT, from_=0, to=100)
        label1 = ttk.Label(self, text='行')

        label.grid(row=3, column=0, sticky=tk.E)
        spinbox.grid(row=3, column=1, sticky=tk.EW)
        label1.grid(row=3, column=2, sticky=tk.W)

        spinbox.delete(0, tk.END)
        spinbox.insert(0, 4)
        self.line_count_spinbox = spinbox

    def init_layout_algorithm_widgets(self):
        label = ttk.Label(self, text='布局算法：')
        box = AlgorithmBox(self)

        label.grid(row=4, column=0, sticky=tk.E)
        box.grid(row=4, column=1, sticky=tk.EW, columnspan=2)

        box.set('sync')
        self.layout_algorithm_box = box

    def init_tune_duration_widgets(self):
        label = ttk.Label(self, text='微调时长：')
        spinbox = tk.Spinbox(self, justify=tk.RIGHT, from_=-10, to=100)
        label1 = ttk.Label(self, text='秒')

        label.grid(row=5, column=0, sticky=tk.E)
        spinbox.grid(row=5, column=1, sticky=tk.EW)
        label1.grid(row=5, column=2, sticky=tk.W)

        spinbox.delete(0, tk.END)
        spinbox.insert(0, 0)
        self.tune_duration_spinbox = spinbox

    def init_drop_offset_widgets(self):
        label = ttk.Label(self, text='丢弃偏移：')
        spinbox = tk.Spinbox(self, justify=tk.RIGHT, from_=0, to=100)
        label1 = ttk.Label(self, text='秒')

        label.grid(row=6, column=0, sticky=tk.E)
        spinbox.grid(row=6, column=1, sticky=tk.EW)
        label1.grid(row=6, column=2, sticky=tk.W)

        spinbox.delete(0, tk.END)
        spinbox.insert(0, 5)
        self.drop_offset_spinbox = spinbox

    def init_bottom_margin_widgets(self):
        label = ttk.Label(self, text='底部边距：')
        spinbox = tk.Spinbox(self, justify=tk.RIGHT, from_=0, to=100)
        label1 = ttk.Label(self, text='像素')

        label.grid(row=7, column=0, sticky=tk.E)
        spinbox.grid(row=7, column=1, sticky=tk.EW)
        label1.grid(row=7, column=2, sticky=tk.W)

        spinbox.delete(0, tk.END)
        spinbox.insert(0, 0)
        self.bottom_margin_spinbox = spinbox

    def init_custom_offset_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='自定偏移：')
        entry = ttk.Entry(self, textvariable=strvar, justify=tk.RIGHT)
        label1 = ttk.Label(self, text='秒')

        label.grid(row=8, column=0, sticky=tk.E)
        entry.grid(row=8, column=1, sticky=tk.EW)
        label1.grid(row=8, column=2, sticky=tk.W)

        strvar.set('0')
        self.custom_offset_strvar = strvar

    def init_header_file_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='样式模板：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=9, column=0, sticky=tk.E)
        entry.grid(row=9, column=1, sticky=tk.EW)
        button.grid(row=9, column=2, sticky=tk.W)

        button['command'] = self.on_header_file_button_clicked
        self.header_file_strvar = strvar

    def on_header_file_button_clicked(self):
        current_path = self.header_file_strvar.get().strip()
        if current_path == '':
            foldername, filename = os.getcwd(), ''
        else:
            foldername, filename = os.path.split(current_path)

        selected_path = tk.filedialog.askopenfilename(
            parent=self,
            title='打开文件',
            initialdir=foldername,
            initialfile=filename
        )

        if selected_path is None:
            return

        self.header_file_strvar.set(selected_path)

    def values(self):
        return dict(
            play_resolution=self.play_resolution_box.get().strip(),
            font_name=self.font_name_strvar.get().strip(),
            font_size=int(self.font_size_spinbox.get()),
            line_count=int(self.line_count_spinbox.get()),
            layout_algorithm=self.layout_algorithm_box.get(),
            tune_duration=int(self.tune_duration_spinbox.get()),
            drop_offset=int(self.drop_offset_spinbox.get()),
            bottom_margin=int(self.bottom_margin_spinbox.get()),
            custom_offset=self.custom_offset_strvar.get().strip(),
            header_file=self.header_file_strvar.get().strip(),
        )


class ResolutionBox(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.init_widgets()

    def init_widgets(self):
        width_spinbox = tk.Spinbox(
            self, justify=tk.RIGHT, width=16, from_=1, to=9999)
        label = ttk.Label(self, text='x')
        height_spinbox = tk.Spinbox(
            self, justify=tk.RIGHT, width=16, from_=1, to=9999)

        width_spinbox.pack(side=tk.LEFT, fill=tk.BOTH)
        label.pack(side=tk.LEFT)
        height_spinbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.width_spinbox = width_spinbox
        self.height_spinbox = height_spinbox

    def get(self):
        width = self.width_spinbox.get()
        height = self.height_spinbox.get()
        return width + 'x' + height

    def set(self, value):
        width, height = value.split('x')
        self.width_spinbox.delete(0, tk.END)
        self.width_spinbox.insert(0, width)
        self.height_spinbox.delete(0, tk.END)
        self.height_spinbox.insert(0, height)


class AlgorithmBox(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.init_widgets()

    def init_widgets(self):
        strvar = tk.StringVar()
        sync_radiobutton = ttk.Radiobutton(
            self, text='速度同步', variable=strvar, value='sync')
        async_radiobutton = ttk.Radiobutton(
            self, text='速度异步', variable=strvar, value='async')

        sync_radiobutton.pack(side=tk.LEFT)
        async_radiobutton.pack(side=tk.LEFT)
        self.strvar = strvar

    def get(self):
        return self.strvar.get()

    def set(self, value):
        self.strvar.set(value)

import os
from .tkmodules import tk, ttk, tku


class DanmakuFrame(ttk.LabelFrame):

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='弹幕选项', padding=2)
        self.pack(fill=tk.BOTH)
        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.init_assist_params_widgets()
        self.init_custom_filter_widgets()
        self.init_disable_top_filter_widgets()
        self.init_disable_bottom_filter_widgets()
        self.init_disable_guest_filter_widgets()
        self.init_disable_video_filter_widgets()
        self.init_skip_patch_widgets()
        self.init_merge_parts_widgets()
        tku.add_border_space(self, 1, 1)

    def init_assist_params_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='辅助参数：')
        entry = ttk.Entry(self, textvariable=strvar)

        label.grid(row=0, column=0, sticky=tk.E)
        entry.grid(row=0, column=1, sticky=tk.EW, columnspan=2)

        self.assist_params_strvar = strvar

    def init_custom_filter_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='过滤文件：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=1, column=0, sticky=tk.E)
        entry.grid(row=1, column=1, sticky=tk.EW)
        button.grid(row=1, column=2, sticky=tk.W)

        button['command'] = self.on_custom_filter_button_clicked
        self.custom_filter_strvar = strvar

    def init_disable_top_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='不要过滤顶部弹幕', variable=intvar)

        checkbutton.grid(row=2, column=0, sticky=tk.W, columnspan=3)

        self.disable_top_filter_intvar = intvar

    def init_disable_bottom_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='不要过滤底部弹幕', variable=intvar)

        checkbutton.grid(row=3, column=0, sticky=tk.W, columnspan=3)

        self.disable_bottom_filter_intvar = intvar

    def init_disable_guest_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='不要过滤游客弹幕', variable=intvar)

        checkbutton.grid(row=4, column=0, sticky=tk.W, columnspan=3)

        self.disable_guest_filter_intvar = intvar

    def init_disable_video_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='不要过滤云屏蔽弹幕', variable=intvar)

        checkbutton.grid(row=5, column=0, sticky=tk.W, columnspan=3)

        self.disable_video_filter_intvar = intvar

    def init_skip_patch_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(self, text='跳过补丁', variable=intvar)

        checkbutton.grid(row=6, column=0, sticky=tk.W, columnspan=3)

        self.skip_patch_intvar = intvar

    def init_merge_parts_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(self, text='合并分段', variable=intvar)

        checkbutton.grid(row=7, column=0, sticky=tk.W, columnspan=3)

        self.merge_parts_intvar = intvar

    def on_custom_filter_button_clicked(self):
        current_path = self.custom_filter_strvar.get().strip()
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

        self.custom_filter_strvar.set(selected_path)

    def values(self):
        return dict(
            assist_params=self.assist_params_strvar.get().strip(),
            custom_filter=self.custom_filter_strvar.get().strip(),
            disable_top_filter=self.disable_top_filter_intvar.get() == 1,
            disable_bottom_filter=self.disable_bottom_filter_intvar.get() == 1,
            disable_guest_filter=self.disable_guest_filter_intvar.get() == 1,
            disable_video_filter=self.disable_video_filter_intvar.get() == 1,
            skip_patch=self.skip_patch_intvar.get() == 1,
            merge_parts=self.merge_parts_intvar.get() == 1,
        )

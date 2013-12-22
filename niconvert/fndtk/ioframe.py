import os
from .tkmodules import tk, ttk, tku


class IoFrame(ttk.LabelFrame):

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='输入输出', padding=2)
        self.pack(fill=tk.BOTH)
        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.init_url_widgets()
        self.init_output_filename_widgets()
        self.init_create_playlist_widgets()
        self.init_convert_widgets()
        tku.add_border_space(self, 1, 1)

    def init_url_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='视频地址：')
        entry = ttk.Entry(self, textvariable=strvar)

        label.grid(row=0, column=0, sticky=tk.E)
        entry.grid(row=0, column=1, sticky=tk.EW, columnspan=2)

        self.url_strvar = strvar

    def init_output_filename_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='输出文件：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=1, column=0, sticky=tk.E)
        entry.grid(row=1, column=1, sticky=tk.EW)
        button.grid(row=1, column=2, sticky=tk.W)

        strvar.set(os.getcwd())
        button['command'] = self.on_output_filename_button_clicked
        self.output_filename_strvar = strvar

    def init_create_playlist_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='同时输出播放列表', variable=intvar)
        checkbutton.grid(row=3, column=0, sticky=tk.W, columnspan=3)

        self.create_playlist_intvar = intvar

    def init_convert_widgets(self):
        button = ttk.Button(self, text='转换', width=6)

        button.grid(row=3, column=2, sticky=tk.W)

        button['command'] = self.on_convert_button_clicked
        self.convert_button = button

    def on_output_filename_button_clicked(self):
        current_path = self.output_filename_strvar.get().strip()
        if current_path == '':
            foldername, filename = os.getcwd(), ''
        elif os.path.isdir(current_path):
            foldername, filename = current_path, ''
        else:
            foldername, filename = os.path.split(current_path)

        selected_path = tk.filedialog.asksaveasfilename(
            parent=self,
            title='保存文件',
            initialdir=foldername,
            initialfile=filename
        )

        if selected_path is None:
            return

        if selected_path == '':
            selected_path = os.getcwd()
        self.output_filename_strvar.set(selected_path)

    def on_convert_button_clicked(self):
        self.event_generate('<<ConvertButtonClicked>>')

    def values(self):
        return dict(
            url=self.url_strvar.get().strip(),
            output_filename=self.output_filename_strvar.get().strip(),
            create_playlist=self.create_playlist_intvar.get() == 1,
        )

    def enable_convert_button(self):
        self.convert_button['state'] = tk.NORMAL

    def disable_convert_button(self):
        self.convert_button['state'] = tk.DISABLED

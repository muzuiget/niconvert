from pathlib import Path
from niconvert.fndtk.tkmodules import tk, ttk, tku

class IoFrame(ttk.LabelFrame):

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='输入输出', padding=2)
        self.pack(fill=tk.BOTH)
        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.init_input_filename_widgets()
        self.init_output_filename_widgets()
        self.init_convert_widgets()
        tku.add_border_space(self, 1, 1)

    def init_input_filename_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='输入文件：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=0, column=0, sticky=tk.E)
        entry.grid(row=0, column=1, sticky=tk.EW)
        button.grid(row=0, column=2, sticky=tk.W)

        strvar.set('')
        button['command'] = self.on_input_filename_button_clicked

        self.input_filename_strvar = strvar

    def init_output_filename_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='输出文件：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=1, column=0, sticky=tk.E)
        entry.grid(row=1, column=1, sticky=tk.EW)
        button.grid(row=1, column=2, sticky=tk.W)

        strvar.set('')
        button['command'] = self.on_output_filename_button_clicked
        self.output_filename_strvar = strvar

    def init_convert_widgets(self):
        button = ttk.Button(self, text='转换', width=6)

        button.grid(row=3, column=2, sticky=tk.W)

        button['command'] = self.on_convert_button_clicked
        self.convert_button = button

    def on_input_filename_button_clicked(self):
        strvar = self.input_filename_strvar
        filetypes = [
            ('XML 文件', '*.xml'),
            ('JSON 文件', '*.json'),
        ]
        tku.on_filedialog(self, strvar=strvar, method='load',
                          defaultextension='.xml',
                          filetypes=filetypes)()

        # 自动设置输出文件名
        input_filename = strvar.get().strip()
        if input_filename == '':
            return
        output_filename = self.output_filename_strvar.get().strip()
        if output_filename.endswith('.ass'):
            return
        path = str(Path(input_filename).with_suffix('.ass'))
        self.output_filename_strvar.set(path)

    def on_output_filename_button_clicked(self):
        strvar = self.output_filename_strvar
        filetypes = [('ASS 文件', '*.ass')]
        tku.on_filedialog(self, strvar=strvar, method='save',
                          defaultextension='.ass',
                          filetypes=filetypes)()

    def on_convert_button_clicked(self):
        self.event_generate('<<ConvertButtonClicked>>')

    def values(self):
        return dict(
            input_filename=self.input_filename_strvar.get().strip(),
            output_filename=self.output_filename_strvar.get().strip(),
        )

    def enable_convert_button(self):
        self.convert_button['state'] = tk.NORMAL

    def disable_convert_button(self):
        self.convert_button['state'] = tk.DISABLED

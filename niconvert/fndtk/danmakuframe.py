import os
from niconvert.fndtk.tkmodules import tk, ttk, tku

class DanmakuFrame(ttk.LabelFrame):

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='弹幕选项', padding=2)
        self.pack(fill=tk.BOTH)
        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.init_custom_filter_widgets()
        self.init_top_filter_widgets()
        self.init_bottom_filter_widgets()
        self.init_guest_filter_widgets()
        tku.add_border_space(self, 1, 1)

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

    def init_top_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='过滤顶部弹幕', variable=intvar)

        checkbutton.grid(row=2, column=0, sticky=tk.W, columnspan=3)

        self.top_filter_intvar = intvar

    def init_bottom_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='过滤底部弹幕', variable=intvar)

        checkbutton.grid(row=3, column=0, sticky=tk.W, columnspan=3)

        self.bottom_filter_intvar = intvar

    def init_guest_filter_widgets(self):
        intvar = tk.IntVar()
        checkbutton = ttk.Checkbutton(
            self, text='过滤游客弹幕', variable=intvar)

        checkbutton.grid(row=4, column=0, sticky=tk.W, columnspan=3)

        self.guest_filter_intvar = intvar

    def on_custom_filter_button_clicked(self):
        strvar = self.custom_filter_strvar
        filetypes = [
            ('文本文件', '*.txt'),
            ('Python 文件', '*.py'),
        ]
        tku.on_filedialog(self, strvar=strvar, method='load',
                          defaultextension='.txt',
                          filetypes=filetypes)()

    def values(self):
        custom_filter = self.custom_filter_strvar.get().strip()
        if custom_filter == '':
            custom_filter = None
        return dict(
            custom_filter=custom_filter,
            top_filter=self.top_filter_intvar.get() == 1,
            bottom_filter=self.bottom_filter_intvar.get() == 1,
            guest_filter=self.guest_filter_intvar.get() == 1,
        )

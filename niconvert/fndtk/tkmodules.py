from os.path import join, dirname
import tkinter
import tkinter.ttk
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext

tk = tkinter
ttk = tkinter.ttk

# MonkeyPatch 来让 ScrolledText 用上 ttk 的组件
tk.scrolledtext.Frame = ttk.Frame
tk.scrolledtext.Scrollbar = ttk.Scrollbar
ttk.ScrolledText = tk.scrolledtext.ScrolledText


class tku(object):

    @staticmethod
    def add_border_space(widget, padx, pady, recursive=True):
        ''' 给每个 widget 增加指定像素的距离 '''
        widget.pack_configure(padx=padx, pady=pady)
        if recursive:
            for subwidget in widget.pack_slaves():
                subwidget.pack_configure(padx=padx, pady=pady)
            for subwidget in widget.grid_slaves():
                subwidget.grid_configure(padx=padx, pady=pady)

    @staticmethod
    def move_to_screen_center(win):
        ''' 把窗口移动到屏幕中间 '''
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        window_size = win.geometry().split('+')[0]
        window_width, window_height = map(int, window_size.split('x'))
        x = screen_width / 2 - window_width / 2 - 8
        y = screen_height / 2 - window_height / 2 - 40
        win.geometry('%dx%d+%d+%d' %
                    (window_width, window_height, x, y))

    @staticmethod
    def asset_path(name):
        return join(dirname(dirname(__file__)), 'assets', name)

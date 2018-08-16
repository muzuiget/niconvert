import sys
import webbrowser
from io import StringIO
from pprint import pprint
from niconvert.fndcli.main import convert
from niconvert.fndtk.utils import toisotime, redirect_stdio
from niconvert.fndtk.tkmodules import tk, ttk, tku
from niconvert.fndtk.menubar import MenuBar
from niconvert.fndtk.ioframe import IoFrame
from niconvert.fndtk.danmakuframe import DanmakuFrame
from niconvert.fndtk.loggingframe import LoggingFrame
from niconvert.fndtk.subtitleframe import SubtitleFrame

class Application(ttk.Frame):

    def __init__(self):
        ttk.Frame.__init__(self, None, border=2)
        self.pack(fill=tk.BOTH, expand=True)
        self.init_widgets()

    def init_widgets(self):
        self.init_topwin()
        self.init_menubar()
        self.init_rootpane()
        self.init_left_frame()
        self.init_right_frame()
        tku.add_border_space(self, 2, 2)

        # Windows 下让窗口居中
        # 有个问题，窗口实例初始化后，出现在默认位置，
        # 如果马上修改窗口位置，窗口还是会在默认位置闪现一下，
        # 因此先隐藏起来，位置更新后再显示出来
        if sys.platform.startswith('win'):
            self.topwin.withdraw()
            tku.move_to_screen_center(self.topwin)
            self.topwin.deiconify()

    def init_topwin(self):
        self.topwin = self.winfo_toplevel()
        self.topwin.title('Niconvert')
        if sys.platform.startswith('win'):
            icon_path = tku.asset_path('logo.ico')
            self.topwin.iconbitmap(default=icon_path)
        else:
            icon_path = tku.asset_path('logo.gif')
            self.topwin.iconphoto(self.topwin, tk.PhotoImage(file=icon_path))
        self.topwin.protocol('WM_DELETE_WINDOW', self.quit)

    def init_menubar(self):
        events = {
            '<<QuitMenuitemClicked>>': self.on_quit_menuitem_clicked,
            '<<HelpMenuitemClicked>>': self.on_help_menuitem_clicked,
            '<<AboutMenuitemClicked>>': self.on_about_menuitem_clicked,
        }
        menubar = MenuBar(self)
        for name, func in events.items():
            menubar.bind(name, func)

        self.topwin.config(menu=menubar)

    def init_rootpane(self):
        self.rootpane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.rootpane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def init_left_frame(self):
        frame = ttk.Frame(self)
        self.io_frame = IoFrame(frame)
        self.danmaku_frame = DanmakuFrame(frame)
        self.subtitle_frame = SubtitleFrame(frame)
        self.io_frame.bind('<<ConvertButtonClicked>>',
                           self.on_convert_button_clicked)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.rootpane.add(frame)

    def init_right_frame(self):
        frame = ttk.Frame(self)
        self.logging_frame = LoggingFrame(frame)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.rootpane.add(frame)

    def get_convert_args_list(self):
        io_args = self.io_frame.values()
        danmaku_args = self.danmaku_frame.values()
        subtitle_args = self.subtitle_frame.values()
        if sys.stdout:
            pprint(io_args)
            pprint(danmaku_args)
            pprint(subtitle_args)
        return (io_args, danmaku_args, subtitle_args)

    def on_convert_button_clicked(self, event): # pylint: disable=unused-argument
        args_list = self.get_convert_args_list()
        io_args = args_list[0]
        if io_args['input_filename'] == '':
            return
        if io_args['output_filename'] == '':
            return

        self.io_frame.disable_convert_button()

        stream = StringIO()
        with redirect_stdio(stream):
            print('[%s] 开始转换 ...' % toisotime())
            convert(*args_list)
        self.logging_frame.write(stream.getvalue() + '\n')

        self.io_frame.enable_convert_button()

    def on_quit_menuitem_clicked(self):
        self.quit()

    def on_help_menuitem_clicked(self):
        url = 'https://github.com/muzuiget/niconvert/tree/master/docs'
        webbrowser.open(url)

    def on_about_menuitem_clicked(self):
        url = 'https://github.com/muzuiget/niconvert#readme'
        webbrowser.open(url)

def main():
    app = Application()
    app.mainloop()

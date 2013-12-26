import sys
import webbrowser
import traceback
from pprint import pprint
from ..fndcli.main import convert
from .tkmodules import tk, ttk, tku
from .menubar import MenuBar
from .ioframe import IoFrame
from .danmakuframe import DanmakuFrame
from .loggingframe import LoggingFrame
from .subtitleframe import SubtitleFrame


class Application(ttk.Frame):

    def __init__(self):
        ttk.Frame.__init__(self, None, border=2)
        self.pack(fill=tk.BOTH, expand=True)
        self.init_widgets()

    def init_widgets(self):
        self.init_topwin()
        self.init_menubar()
        self.init_left_frame()
        self.init_right_frame()
        tku.add_border_space(self, 2, 2)

        # Windows 下有个问题，窗口实例初始化后，出现在默认位置，
        # 如果马上修改窗口位置，窗口还是会在默认位置闪现一下，
        # 因此先隐藏起来，位置更新后再显示出来
        if sys.platform.startswith('win'):
            self.topwin.withdraw()
            tku.move_to_screen_center(self.topwin)
            self.topwin.deiconify()
        else:
            tku.move_to_screen_center(self.topwin)

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
        # XXX Python 3.3 在 Windows XP/7 里都不能收到 bind 过的函数
        # 原因不明，不想给 MenuBar 传入外部依赖 ，暂时用 MonkeyPatch 处理
        if sys.platform.startswith('win'):
            MenuBar.on_quit_menuitem_clicked = \
                lambda s: self.on_quit_menuitem_clicked(None)
            MenuBar.on_help_menuitem_clicked = \
                lambda s: self.on_help_menuitem_clicked(None)
            MenuBar.on_about_menuitem_clicked = \
                lambda s: self.on_about_menuitem_clicked(None)

        events = {
            '<<QuitMenuitemClicked>>': self.on_quit_menuitem_clicked,
            '<<HelpMenuitemClicked>>': self.on_help_menuitem_clicked,
            '<<AboutMenuitemClicked>>': self.on_about_menuitem_clicked,
        }
        menubar = MenuBar(self)
        for name, func in events.items():
            menubar.bind(name, func)

        self.topwin.config(menu=menubar)

    def init_left_frame(self):
        frame = ttk.Frame(self)
        self.io_frame = IoFrame(frame)
        self.danmaku_frame = DanmakuFrame(frame)
        self.subtitle_frame = SubtitleFrame(frame)
        self.io_frame.bind('<<ConvertButtonClicked>>',
                           self.on_convert_button_clicked)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)

    def init_right_frame(self):
        frame = ttk.Frame(self)
        self.logging_frame = LoggingFrame(frame)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_convert_args_list(self):
        io_args = self.io_frame.values()
        danmaku_args = self.danmaku_frame.values()
        subtitle_args = self.subtitle_frame.values()
        if sys.stdout:
            pprint(io_args)
            pprint(danmaku_args)
            pprint(subtitle_args)
        return (io_args, danmaku_args, subtitle_args)

    def on_convert_button_clicked(self, event):
        args_list = self.get_convert_args_list()
        if args_list[0]['url'] == '':
            return

        # TODO 使用线程
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr

        self.io_frame.disable_convert_button()
        sys.stdout = self.logging_frame
        try:
            print('========')
            print('开始转换')
            print('========')
            print()
            convert(*args_list)
        except:
            print(traceback.format_exc())
        self.io_frame.enable_convert_button()

        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    def on_quit_menuitem_clicked(self, event):
        self.quit()

    def on_help_menuitem_clicked(self, event):
        webbrowser.open('https://github.com/muzuiget/niconvert/wiki')

    def on_about_menuitem_clicked(self, event):
        webbrowser.open('https://github.com/muzuiget/niconvert#readme')


def main():
    app = Application()
    app.mainloop()

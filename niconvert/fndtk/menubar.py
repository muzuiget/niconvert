from niconvert.fndtk.tkmodules import tk

class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.event_funcs = {}
        self.init_widgets()

    def init_widgets(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(
            label='退出(Q)', underline=3,
            command=self.on_quit_menuitem_clicked)

        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(
            label='帮助(O)', underline=3,
            command=self.on_help_menuitem_clicked)
        help_menu.add_command(
            label='关于(A)', underline=3,
            command=self.on_about_menuitem_clicked)

        self.add_cascade(label='文件(F)', menu=file_menu, underline=3)
        self.add_cascade(label='帮助(H)', menu=help_menu, underline=3)

    def on_quit_menuitem_clicked(self):
        func = self.event_funcs['<<QuitMenuitemClicked>>']
        func()

    def on_help_menuitem_clicked(self):
        func = self.event_funcs['<<HelpMenuitemClicked>>']
        func()

    def on_about_menuitem_clicked(self):
        func = self.event_funcs['<<AboutMenuitemClicked>>']
        func()

    def bind(self, name, func):
        # pylint: disable=arguments-differ
        self.event_funcs[name] = func

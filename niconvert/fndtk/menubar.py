from .tkmodules import tk


class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
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
        self.event_generate('<<QuitMenuitemClicked>>')

    def on_help_menuitem_clicked(self):
        self.event_generate('<<HelpMenuitemClicked>>')

    def on_about_menuitem_clicked(self):
        self.event_generate('<<AboutMenuitemClicked>>')

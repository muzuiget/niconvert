#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser
import Tkinter as tk
import tkMessageBox
import tkFileDialog
import tkFont
from niconvert import create_website

class FontDialog(tk.Toplevel):

    def __init__(self, parent, init_font_name=None, init_font_size=24):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.font_name = init_font_name
        self.font_size = init_font_size
        self.transient(parent)
        self.do_layout()
        self.bind_event()

    def do_layout(self):

        def create_font_list_widget():
            frame = tk.Frame(self)
            frame.pack(fill=tk.BOTH)

            self.font_listbox = tk.Listbox(
                frame, takefocus=tk.FALSE, exportselection=tk.FALSE)

            font_scrollbar= tk.Scrollbar(frame)

            fonts = list(tkFont.families(self))
            fonts = list(set(fonts))
            fonts.sort()
            for font in fonts:
                self.font_listbox.insert(tk.END, font)
            if self.font_name in fonts:
                activate_index = fonts.index(self.font_name)
            else:
                activate_index = 0
            self.font_listbox.selection_set(activate_index)
            self.font_listbox.see(activate_index)

            font_scrollbar.config(command=self.font_listbox.yview)
            self.font_listbox.config(yscrollcommand=font_scrollbar.set)

            tk.Label(frame, text=u'字体：', anchor=tk.N).pack(
                side=tk.LEFT, fill=tk.Y)
            self.font_listbox.pack(side=tk.LEFT)
            font_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        def create_font_size_widget():
            frame = tk.Frame(self)
            frame.pack(fill=tk.BOTH)

            self.font_size_spinbox = tk.Spinbox(
                frame, justify=tk.RIGHT, from_=6, to=72)
            self.font_size_spinbox.delete(0, tk.END)
            self.font_size_spinbox.insert(0, self.font_size)

            tk.Label(frame, text=u'大小：').pack(side=tk.LEFT)
            self.font_size_spinbox.pack(side=tk.LEFT, fill=tk.BOTH)
            tk.Label(frame, text=u'像素').pack(side=tk.LEFT)

        def create_response_widget():
            frame = tk.Frame(self)
            frame.pack(fill=tk.BOTH)

            self.ok_button = tk.Button(self, text="确定")
            self.cancel_button = tk.Button(self, text="取消")

            self.ok_button.pack(side=tk.RIGHT)
            self.cancel_button.pack(side=tk.RIGHT)

        def add_space_for_each_widgets():
            for widget in self.slaves():
                widget.pack_configure(padx=2, pady=2)
                for subwidget in widget.pack_slaves():
                    subwidget.pack_configure(padx=2, pady=2)

        create_font_list_widget()
        create_font_size_widget()
        create_response_widget()
        add_space_for_each_widgets()

    def bind_event(self):
        self.protocol("WM_DELETE_WINDOW", self.cancel_command)
        self.ok_button['command'] = self.ok_command
        self.cancel_button['command'] = self.cancel_command

    def show(self):
        self.grab_set()
        self.wait_window()

    def close(self):
        self.parent.focus_set()
        self.destroy()

    @staticmethod
    def run(parent, init_font_name=None, init_font_size=24):
        dialog = FontDialog(parent, init_font_name, init_font_size)
        dialog.show()
        if dialog.response == tkMessageBox.OK:
            return dialog.font_name, dialog.font_size
        else:
            return None

    def ok_command(self):
        index = int(self.font_listbox.curselection()[0])
        self.font_name = self.font_listbox.get(index)
        try:
            self.font_size = int(self.font_size_spinbox.get())
        except ValueError:
            tkMessageBox.showerror('', '字体大小必须为整数')
            return
        self.response = tkMessageBox.OK
        self.close()

    def cancel_command(self):
        self.response = tkMessageBox.CANCEL
        self.close()

class NiconvertTk:

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Niconvert')
        self.main_frame = tk.Frame(self.main_window, border=2)
        self.do_layout()
        self.bind_event()

        self.website = None

    def do_layout(self):

        def create_menubar():
            menubar = tk.Menu(self.main_window)

            self.quit_menuitem = dict(
                    label=u"退出(Q)", underline=3,
                    command=self.quit_menuitem_command)
            self.about_menuitem = dict(
                    label=u"关于(A)", underline=3,
                    command=self.about_menuitem_command)

            file_menu = tk.Menu(menubar, tearoff=0)
            help_menu = tk.Menu(menubar, tearoff=0)

            file_menu.add_command(**self.quit_menuitem)
            help_menu.add_command(**self.about_menuitem)
            menubar.add_cascade(label=u"文件(F)", menu=file_menu, underline=3)
            menubar.add_cascade(label=u"帮助(H)", menu=help_menu, underline=3)

            self.main_window.config(menu=menubar)

        def create_analyse_widget():
            frame = tk.LabelFrame(self.main_frame, text=u"分析")
            frame.pack(fill=tk.BOTH)

            self.url_entry = tk.Entry(frame)
            self.fetch_button = tk.Button(frame, text=u'抓取')

            tk.Label(frame, text=u'视频地址:').pack(side=tk.LEFT)
            self.url_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.fetch_button.pack(side=tk.LEFT)

        def create_summary_widget():
            frame = tk.LabelFrame(self.main_frame, text=u"摘要")
            frame.pack(fill=tk.BOTH)

            self.video_title_label = tk.Label(frame, text='', anchor=tk.W)
            self.comment_url_label = tk.Label(
                frame, text='', anchor=tk.W, fg='#0000FF')

            tk.Label(frame, text=u'视频标题:').grid(row=0, column=0)
            self.video_title_label.grid(row=0, column=1, sticky=tk.EW)
            tk.Label(frame, text=u'评论地址:').grid(row=1, column=0)
            self.comment_url_label.grid(row=1, column=1, sticky=tk.EW)

        def create_options_widget():

            def set_default_value(spinbox, value):
                spinbox.delete(0, tk.END)
                spinbox.insert(0, value)

            frame = tk.LabelFrame(self.main_frame, text=u"选项")
            frame.pack(fill=tk.BOTH)

            video_frame = tk.Frame(frame)

            if sys.platform == 'win32':
                font_label = u"微软雅黑 | 24"
            else:
                font_label = 'WenQuanYi Micro Hei | 24'
            self.font_button = tk.Button(frame, text=font_label)
            self.video_width_spinbox = tk.Spinbox(
                video_frame, justify=tk.RIGHT, from_=1, to=9999)
            self.video_height_spinbox = tk.Spinbox(
                video_frame, justify=tk.RIGHT, from_=1, to=9999)
            self.line_count_spinbox = tk.Spinbox(
                frame, justify=tk.RIGHT, from_=1, to=100)
            self.bottom_margin_spinbox = tk.Spinbox(
                frame, justify=tk.RIGHT, from_=1, to=9999)
            self.tune_seconds_spinbox = tk.Spinbox(
                frame, justify=tk.RIGHT, from_=-100, to=100)
            self.output_entry = tk.Entry(frame)
            self.output_button = tk.Button(frame, text=u'浏览')

            set_default_value(self.video_width_spinbox, 1280)
            set_default_value(self.video_height_spinbox, 768)
            set_default_value(self.line_count_spinbox, 5)
            set_default_value(self.bottom_margin_spinbox, 50)
            set_default_value(self.tune_seconds_spinbox, 0)

            self.video_width_spinbox.pack(side=tk.LEFT)
            tk.Label(video_frame, text='x').pack(side=tk.LEFT)
            self.video_height_spinbox.pack(side=tk.LEFT)

            tk.Label(frame, text=u'字体:').grid(
                row=0, column=0, sticky=tk.E)
            self.font_button.grid(row=0, column=1, columnspan=2, sticky=tk.EW)

            tk.Label(frame, text=u'分辨率:').grid(
                row=1, column=0, sticky=tk.E)
            video_frame.grid(row=1, column=1, sticky=tk.EW)
            tk.Label(frame, text=u'像素').grid(row=1, column=2, sticky=tk.W)

            tk.Label(frame, text=u'同屏行数:').grid(
                row=2, column=0, sticky=tk.E)
            self.line_count_spinbox.grid(row=2, column=1, sticky=tk.EW)
            tk.Label(frame, text=u'像素').grid(row=2, column=2, sticky=tk.W)

            tk.Label(frame, text=u'底边距离:').grid(
                row=3, column=0, sticky=tk.E)
            self.bottom_margin_spinbox.grid(row=3, column=1, sticky=tk.EW)
            tk.Label(frame, text=u'像素').grid(row=3, column=2, sticky=tk.W)

            tk.Label(frame, text=u'调整秒数:').grid(
                row=4, column=0, sticky=tk.E)
            self.tune_seconds_spinbox.grid(row=4, column=1, sticky=tk.EW)
            tk.Label(frame, text=u'像素').grid(row=4, column=2, sticky=tk.W)

            tk.Label(frame, text=u'输出文件:').grid(
                row=5, column=0, sticky=tk.E)
            self.output_entry.grid(row=5, column=1, sticky=tk.EW)
            self.output_button.grid(row=5, column=2, sticky=tk.W)

        def create_convert_widget():
            frame = tk.Frame(self.main_frame)
            frame.pack(fill=tk.BOTH)

            self.convert_button = tk.Button(frame, text=u"转换")
            self.convert_button.pack(side=tk.RIGHT)

        def add_space_for_each_widgets():
            for widget in self.main_frame.slaves():
                widget.pack_configure(padx=2, pady=2)
                for subwidget in widget.pack_slaves():
                    subwidget.pack_configure(padx=2, pady=2)
                for subwidget in widget.grid_slaves():
                    subwidget.grid_configure(padx=2, pady=2)

        self.main_frame.pack(fill=tk.BOTH)
        create_menubar()
        create_analyse_widget()
        create_summary_widget()
        create_options_widget()
        create_convert_widget()
        add_space_for_each_widgets()

    def bind_event(self):
        self.main_window.protocol(
            "WM_DELETE_WINDOW", self.quit_menuitem_command)
        self.comment_url_label.bind(
            "<Button-1>", self.comment_url_label_event_handler)
        self.output_entry.bind(
            '<FocusOut>', self.output_entry_event_handler)
        self.fetch_button['command'] = self.fetch_button_command
        self.font_button['command'] = self.font_button_command
        self.output_button['command'] = self.output_button_command
        self.convert_button['command'] = self.convert_button_command

    def alert(self, message_type, message_text):
        show_func = getattr(tkMessageBox, 'show%s' % message_type.lower())
        show_func('', message_text)

    def comment_url_label_event_handler(self, event):
        webbrowser.open(self.comment_url_label['text'])

    def output_entry_event_handler(self, event):
        text = self.output_entry.get().strip()
        if text != '' and not text.endswith('.ass'):
            text += '.ass'
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, text)

    def font_button_command(self):
        font_name, font_size =  self.font_button['text'].split(' | ')
        font_size = int(font_size)
        result = FontDialog.run(self.main_window, font_name, font_size)
        if result is not None:
            font_label = "%s | %d" % result
            self.font_button['text'] = font_label

    def fetch_button_command(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http://"):
            return

        try:
            self.website = create_website(url)
        except StandardError as error:
            self.video_title_label['text'] = ''
            self.comment_url_label['text'] = ''
            self.comment_url_label['cursor'] = ''
            self.website = None
            self.alert(tkMessageBox.ERROR, error)
            return

        if self.website is None:
            self.alert(tkMessageBox.ERROR, u"不支持的网站")
            return

        title = self.website.downloader.title
        url = self.website.downloader.comment_url

        self.video_title_label['text'] = title
        self.comment_url_label['text'] = url
        self.comment_url_label['cursor'] = 'hand1'
        if self.output_entry.get().strip() == '':
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, title + '.ass')

    def output_button_command(self):
        filename = 'output.ass'
        output = self.output_entry.get().strip()
        if output == '':
            if self.website is not None:
                filename = self.website.downloader.title + '.ass'
            foldername = os.getcwd()
        else:
            foldername, filename = os.path.split(output)

        output = tkFileDialog.asksaveasfilename(parent=self.main_window,
            title=u"请选择一个文件", initialdir=foldername,
            initialfile=filename
        )

        if output != '':
            if not output.endswith('.ass'):
                output += '.ass'
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output)

    def convert_button_command(self):
        font_name, font_size =  self.font_button['text'].split(' | ')
        font_size = int(font_size)
        video_width = self.video_width_spinbox.get()
        video_height = self.video_height_spinbox.get()
        line_count = self.line_count_spinbox.get()
        bottom_margin = self.bottom_margin_spinbox.get()
        tune_seconds = self.tune_seconds_spinbox.get()

        output = self.output_entry.get().strip()
        errors = []
        if self.website is None:
            errors.append(u"未抓取源字幕")
        if output == '':
            errors.append(u"未选择输出路径")
        options = {
            u'视频宽度' : video_width,
            u'视频高度' : video_height,
            u'同屏行数' : line_count,
            u'底部边距' : bottom_margin,
            u'调整秒数' : tune_seconds
        }
        for key, value in options.iteritems():
            try:
                int(value)
            except ValueError:
                errors.append(u'%s需要为整数' % key)

        if len(errors) != 0:
            self.alert(tkMessageBox.ERROR, '\n'.join(errors))
            return

        video_width = int(video_width)
        video_height = int(video_height)
        line_count = int(line_count)
        bottom_margin = int(bottom_margin)
        tune_seconds = int(tune_seconds)

        text = self.website.ass_subtitles_text(
            font_name=font_name,
            font_size=font_size,
            resolution="%d:%d" % (video_width, video_height),
            line_count=line_count,
            bottom_margin=bottom_margin,
            tune_seconds=tune_seconds
        )

        output = os.path.abspath(output)
        try:
            outfile = open(output, 'w')
            outfile.write(text.encode("UTF-8"))
            outfile.flush()
            outfile.close()
        except StandardError as error:
            self.alert(tkMessageBox.ERROR, error)
            return

        message = u"转换成功，文件保存到\n %s" % output
        self.alert(tkMessageBox.INFO, message)

    def quit_menuitem_command(self):
        self.main_window.quit()

    def about_menuitem_command(self):
        webbrowser.open('https://github.com/muzuiget/niconvert#readme')

def main():
    niconvert_tk = NiconvertTk()
    niconvert_tk.main_window.mainloop()
    niconvert_tk.main_window.destroy()

if __name__ == '__main__':
    main()

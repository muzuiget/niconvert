#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser
from gi.repository import Gtk
from niconvert import create_website

__folder__ = os.path.dirname(os.path.abspath(__file__))

class NiconvertGtk:

    def __init__(self):
        glade_file_path = os.path.join(__folder__, 'niconvert_gtk.glade')
        builder = Gtk.Builder()
        builder.add_from_file(glade_file_path)
        builder.connect_signals(self)
        for widget in builder.get_objects():
            if isinstance(widget, Gtk.Buildable):
                name = Gtk.Buildable.get_name(widget)
                setattr(self, name, widget)

        self.init_widgets_status()
        self.website = None

    def init_widgets_status(self):
        if sys.platform == 'win32':
            self.font_fontbutton.set_font_name(u'微软雅黑 24')
        else:
            self.font_fontbutton.set_font_name('WenQuanYi Micro Hei 24')

    def alert(self, message_type, message_text):
        dialog = Gtk.MessageDialog(
                self.main_window, 0, message_type,
                Gtk.ButtonsType.OK, message_text)
        dialog.run()
        dialog.destroy()

    def on_fetch_button_clicked(self, widget):
        url = self.url_entry.get_text().strip()
        if not url.startswith("http://"):
            return

        try:
            self.website = create_website(url)
        except StandardError as error:
            self.video_title_label.set_text('')
            self.comment_url_label.set_text('')
            self.website = None
            self.alert(Gtk.MessageType.ERROR, error)
            return

        if self.website is None:
            self.alert(Gtk.MessageType.ERROR, u'不支持的网站')
            return

        title = self.website.downloader.title
        url = self.website.downloader.comment_url
        markup = '<a href="%s">%s</a>' % (url, url)

        self.video_title_label.set_text(title)
        self.comment_url_label.set_markup(markup)
        if self.output_entry.get_text().strip() == '':
            self.output_entry.set_text(title + '.ass')

    def on_output_entry_changed(self, widget, event):
        text = self.output_entry.get_text().strip()
        if text != '' and not text.endswith('.ass'):
            text += '.ass'
        self.output_entry.set_text(text)

    def on_output_button_clicked(self, widget):
        filename = 'output.ass'
        output = self.output_entry.get_text().strip()
        if output == '':
            if self.website is not None:
                filename = self.website.downloader.title + '.ass'
            filepath = os.path.join(os.getcwd(), filename)
        else:
            filepath = output

        dialog = Gtk.FileChooserDialog(
            u"请选择一个文件", self.main_window, Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )

        dialog.set_current_name(filename)
        dialog.set_filename(filepath)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            output = dialog.get_filename()
            if not output.endswith('.ass'):
                output += '.ass'
            self.output_entry.set_text(output)
        dialog.destroy()

    def on_convert_button_clicked(self, widget):
        font_name =  self.font_fontbutton.get_font_family().get_name()
        font_size = self.font_fontbutton.get_font_size()
        video_width = self.video_width_spinbutton.get_value_as_int()
        video_height = self.video_height_spinbutton.get_value_as_int()
        line_count = self.line_count_spinbutton.get_value_as_int()
        bottom_margin = self.bottom_margin_spinbutton.get_value_as_int()
        tune_seconds = self.tune_seconds_spinbutton.get_value_as_int()

        output = self.output_entry.get_text().strip()
        errors = []
        if self.website is None:
            errors.append(u"未抓取源字幕")
        if output == '':
            errors.append(u"未选择输出路径")

        if len(errors) != 0:
            self.alert(Gtk.MessageType.ERROR, '\n'.join(errors))
            return

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
            self.alert(Gtk.MessageType.ERROR, error)
            return

        message = u'转换成功，文件保存到\n %s' % output.decode("UTF-8")
        self.alert(Gtk.MessageType.INFO, message)

    def on_quit_imagemenuitem_activate(self, widget):
        Gtk.main_quit()

    def on_about_imagemenuitem_activate(self, widget):
        webbrowser.open('https://github.com/muzuiget/niconvert#readme')

    def on_main_window_desotry(self, widget):
        Gtk.main_quit()

def main():
    NiconvertGtk().main_window.show()
    Gtk.main()

if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser

from PySide.QtCore import QObject
from PySide.QtGui import (QApplication, QDesktopWidget, QMessageBox,
                          QFileDialog, QFontDialog, QFont)
from PySide.QtUiTools import QUiLoader

from niconvert import create_website

__folder__ = os.path.dirname(os.path.abspath(__file__))

class NiconvertQt:

    def __init__(self):
        ui_file_path = os.path.join(__folder__, 'niconvert_qt.ui')
        self.main_window = QUiLoader().load(ui_file_path)
        for widget in self.main_window.findChildren(QObject):
            name = widget.objectName()
            if name == '' or name.startswith('qt_') or name.startswith('_'):
                continue
            setattr(self, name, widget)

        self.init_widgets_status()
        self.bind_signals()

        self.website = None

    def init_widgets_status(self):
        if sys.platform == 'win32':
            self.font_pushButton.setText(u'微软雅黑 | 36')
        else:
            self.font_pushButton.setText('WenQuanYi Micro Hei | 36')
        self.move_to_screen_center()
        self.main_window.resize(480, 0)

    def move_to_screen_center(self):
        cp = QDesktopWidget().availableGeometry().center()
        qr = self.main_window.frameGeometry()
        qr.moveCenter(cp)
        self.main_window.move(qr.topLeft())

    def bind_signals(self):
        self.quit_menuitem.triggered.connect(
            self.quit_menuitem_triggered_slot)
        self.about_menuitem.triggered.connect(
            self.about_menuitem_triggered_slot)
        self.fetch_pushButton.clicked.connect(
            self.fetch_pushButton_clicked_slot)
        self.font_pushButton.clicked.connect(
            self.font_pushButton_clicked_slot)
        self.output_lineEdit.editingFinished.connect(
            self.output_lineEdit_editingFinished_slot)
        self.output_pushButton.clicked.connect(
            self.output_pushButton_clicked_slot)
        self.convert_pushButton.clicked.connect(
            self.convert_pushButton_clicked_slot)

    def alert(self, message_type, message_text):
        dialog = QMessageBox()
        dialog.setIcon(message_type)
        dialog.setText('%s' % message_text)
        dialog.exec_()

    def fetch_pushButton_clicked_slot(self):
        url = self.url_lineEdit.text().strip()
        if not url.startswith('http://'):
            return

        try:
            self.website = create_website(url)
        except StandardError as error:
            self.video_title_label.setText('')
            self.comment_url_label.setText('')
            self.website = None
            self.alert(QMessageBox.Critical, error)
            return

        if self.website is None:
            self.alert(QMessageBox.Critical, u'不支持的网站')
            return

        title = self.website.downloader.title
        url = self.website.downloader.comment_url
        markup = '<a href="%s">%s</a>' % (url, url)

        self.video_title_label.setText(title)
        self.comment_url_label.setText(markup)
        if self.output_lineEdit.text().strip() == '':
            self.output_lineEdit.setText(title + '.ass')

    def font_pushButton_clicked_slot(self):
        font_name, font_size =  self.font_pushButton.text().split(' | ')
        font_size = int(font_size)
        font, respose = QFontDialog.getFont(
            QFont(font_name, font_size), self.main_window)

        if respose:
            font_label = '%s | %d' % (
                font.family(), font.pointSize())
            self.font_pushButton.setText(font_label)

    def output_lineEdit_editingFinished_slot(self):
        text = self.output_lineEdit.text().strip()
        if text != '' and not text.endswith('.ass'):
            text += '.ass'
        self.output_lineEdit.setText(text)

    def output_pushButton_clicked_slot(self):
        filename = 'output.ass'
        output = self.output_lineEdit.text().strip()
        if output == '':
            if self.website is not None:
                filename = self.website.downloader.title + '.ass'
            filepath = os.path.join(os.getcwd(), filename)
        else:
            filepath = output

        output = QFileDialog.getSaveFileName(
            self.main_window, u'请选择一个文件', filepath)[0]

        if output != '':
            if not output.endswith('.ass'):
                output += '.ass'
            self.output_lineEdit.setText(output)

    def convert_pushButton_clicked_slot(self):
        font_name, font_size =  self.font_pushButton.text().split(' | ')
        font_size = int(font_size)
        video_width = self.video_width_spinBox.value()
        video_height = self.video_height_spinBox.value()
        line_count = self.line_count_spinBox.value()
        bottom_margin = self.bottom_margin_spinBox.value()
        tune_seconds = self.tune_seconds_spinBox.value()

        output = self.output_lineEdit.text().strip()
        errors = []
        if self.website is None:
            errors.append(u'未抓取源字幕')
        if output == '':
            errors.append(u'未选择输出路径')

        if len(errors) != 0:
            self.alert(QMessageBox.Critical, '\n'.join(errors))
            return

        text = self.website.ass_subtitles_text(
            font_name=font_name,
            font_size=font_size,
            resolution='%d:%d' % (video_width, video_height),
            line_count=line_count,
            bottom_margin=bottom_margin,
            tune_seconds=tune_seconds
        )

        output = os.path.abspath(output)
        try:
            outfile = open(output, 'w')
            outfile.write(text.encode('UTF-8'))
            outfile.flush()
            outfile.close()
        except StandardError as error:
            self.alert(QMessageBox.Critical, error)
            return

        message = u'转换成功，文件保存到\n %s' % output
        self.alert(QMessageBox.Information, message)

    def quit_menuitem_triggered_slot(self):
        self.main_window.close()

    def about_menuitem_triggered_slot(self):
        webbrowser.open('https://github.com/muzuiget/niconvert#readme')

def main():
    app = QApplication(sys.argv)
    niconvert_qt = NiconvertQt()
    niconvert_qt.main_window.show()
    app.exec_()

if __name__ == '__main__':
    main()

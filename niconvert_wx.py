#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser
import wx
import wx.lib.agw.hyperlink as hl
from niconvert import create_website

class NiconvertWx():

    def __init__(self):
        self.main_window = wx.Frame(None, title='Niconvert')
        self.main_panel = wx.Panel(self.main_window)
        self.do_layout()
        self.bind_event()

        self.website = None

    def do_layout(self):

        def create_menubar():
            file_menu = wx.Menu()
            file_menu.Append(wx.ID_EXIT, u"退出(&Q)")
            help_menu = wx.Menu()
            help_menu.Append(wx.ID_ABOUT, u"关于(&A)")
            menuBar = wx.MenuBar()
            menuBar.Append(file_menu, u"文件(&F)")
            menuBar.Append(help_menu, u"帮助(&H)")
            self.main_window.SetMenuBar(menuBar)

        def create_analyse_widget():
            self.url_textcrtl = wx.TextCtrl(self.main_panel)
            self.fetch_button = wx.Button(self.main_panel, label=u"抓取")

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"视频地址："),
                0, wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                self.url_textcrtl, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer.Add(
                self.fetch_button, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)

            upsizer = wx.StaticBoxSizer(
                wx.StaticBox(self.main_panel, label=u"分析"),
                wx.VERTICAL)
            upsizer.Add(sizer, 0, wx.EXPAND)
            return upsizer

        def create_summary_widget():
            self.video_title_statictext = wx.StaticText(self.main_panel)
            self.comment_url_hyperlinkctrl = hl.HyperLinkCtrl(self.main_panel)

            sizer = wx.FlexGridSizer(2, 2, 4, 4)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"视频标题："),
                0, wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self.video_title_statictext, 1, wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"评论地址："),
                0, wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                self.comment_url_hyperlinkctrl, 1, wx.ALIGN_CENTER_VERTICAL)

            upsizer = wx.StaticBoxSizer(
                wx.StaticBox(self.main_panel, label=u"摘要"),
                wx.VERTICAL)
            upsizer.Add(sizer, 0, wx.EXPAND)
            return upsizer

        def create_options_widget():

            if sys.platform == 'win32':
                font_label = u"微软雅黑 | 24"
            else:
                font_label = 'WenQuanYi Micro Hei | 24'
            self.font_button = wx.Button(self.main_panel, label=font_label)
            self.video_width_spinbutton = wx.SpinCtrl(self.main_panel)
            self.video_height_spinbutton = wx.SpinCtrl(self.main_panel)
            self.line_count_spinbutton = wx.SpinCtrl(self.main_panel)
            self.bottom_margin_spinbutton = wx.SpinCtrl(self.main_panel)
            self.tune_seconds_spinbutton = wx.SpinCtrl(self.main_panel)
            self.output_textcrtl = wx.TextCtrl(self.main_panel)
            self.output_button = wx.Button(self.main_panel, label=u"浏览")

            self.video_width_spinbutton.SetRange(1, 9999)
            self.video_width_spinbutton.SetValue(1280)
            self.video_height_spinbutton.SetRange(1, 9999)
            self.video_height_spinbutton.SetValue(768)
            self.line_count_spinbutton.SetRange(1, 100)
            self.line_count_spinbutton.SetValue(5)
            self.bottom_margin_spinbutton.SetRange(1, 9999)
            self.bottom_margin_spinbutton.SetValue(50)
            self.tune_seconds_spinbutton.SetRange(-100, 100)
            self.tune_seconds_spinbutton.SetValue(0)

            video_subsizer = wx.BoxSizer(wx.HORIZONTAL)
            video_subsizer.Add(
                self.video_width_spinbutton, 1, wx.ALIGN_CENTER_VERTICAL)
            video_subsizer.Add(
                wx.StaticText(self.main_panel, label='x'),
                0, wx.ALIGN_CENTER_VERTICAL)
            video_subsizer.Add(
                self.video_height_spinbutton, 1, wx.ALIGN_CENTER_VERTICAL)

            sizer = wx.GridBagSizer(4, 4)

            sizer.Add(
                wx.StaticText(self.main_panel, label=u"字体："),
                (0, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                self.font_button,
                (0, 1), (1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

            sizer.Add(
                wx.StaticText(self.main_panel, label=u"分辨率："),
                (1, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                video_subsizer,
                (1, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"像素"),
                (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)

            sizer.Add(
                wx.StaticText(self.main_panel, label=u"同屏行数："),
                (2, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                self.line_count_spinbutton,
                (2, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"行"),
                (2, 2), flag=wx.ALIGN_CENTER_VERTICAL)

            sizer.Add(
                wx.StaticText(self.main_panel, label=u"底边距离："),
                (3, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                self.bottom_margin_spinbutton,
                (3, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"像素"),
                (3, 2), flag=wx.ALIGN_CENTER_VERTICAL)

            sizer.Add(
                wx.StaticText(self.main_panel, label=u"调整秒数："),
                (4, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                self.tune_seconds_spinbutton,
                (4, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                wx.StaticText(self.main_panel, label=u"秒"),
                (4, 2), flag=wx.ALIGN_CENTER_VERTICAL)

            sizer.Add(wx.StaticText(self.main_panel, label=u"输出文件："),
                (5, 0), flag=wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(
                    self.output_textcrtl, (5, 1),
                    flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self.output_button, (5, 2), flag=wx.ALIGN_CENTER_VERTICAL)

            sizer.AddGrowableCol(1)

            upsizer = wx.StaticBoxSizer(
                wx.StaticBox(self.main_panel, label=u"选项"),
                wx.VERTICAL)
            upsizer.Add(sizer, 0, wx.EXPAND)
            return upsizer

        def create_convert_widget():
            self.convert_button = wx.Button(self.main_panel, label=u"转换")
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(self.convert_button, 0, wx.ALIGN_RIGHT)
            return sizer

        create_menubar()
        main_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel_sizer.Add(create_analyse_widget(), 0, wx.ALL | wx.EXPAND, 4)
        main_panel_sizer.Add(create_summary_widget(), 0, wx.ALL | wx.EXPAND, 4)
        main_panel_sizer.Add(create_options_widget(), 0, wx.ALL | wx.EXPAND, 4)
        main_panel_sizer.Add(
            create_convert_widget(), 0, wx.ALL | wx.ALIGN_RIGHT, 4)

        main_panel_sizer.Fit(self.main_window)
        self.main_panel.SetSizer(main_panel_sizer)
        self.main_window.SetSize((480, -1))
        self.main_window.CenterOnScreen()

    def bind_event(self):
        self.main_window.Bind(
            wx.EVT_MENU, self.quit_menuitem_event_handler, id=wx.ID_EXIT)
        self.main_window.Bind(
            wx.EVT_MENU, self.about_menuitem_event_handler, id=wx.ID_ABOUT)
        self.fetch_button.Bind(wx.EVT_BUTTON, self.fetch_button_event_handler)
        self.font_button.Bind(wx.EVT_BUTTON, self.font_button_event_handler)
        self.output_button.Bind(wx.EVT_BUTTON, self.output_button_event_handler)
        self.output_textcrtl.Bind(
            wx.EVT_KILL_FOCUS, self.output_textcrtl_event_hanlder)
        self.convert_button.Bind(
            wx.EVT_BUTTON, self.convert_button_event_handler)

    def alert(self, message_type, message_text):
        dialog = wx.MessageDialog(
            self.main_window, "%s" % message_text, '', wx.OK | message_type)
        dialog.ShowModal()
        dialog.Destroy()

    def fetch_button_event_handler(self, event):
        url = self.url_textcrtl.GetValue().strip()
        if not url.startswith("http://"):
            return

        try:
            self.website = create_website(url)
        except StandardError as error:
            self.video_title_statictext.SetLabel('')
            self.comment_url_hyperlinkctrl.SetLabel('')
            self.comment_url_hyperlinkctrl.SetURL('')
            self.website = None
            self.alert(wx.ICON_ERROR, error)
            return

        if self.website is None:
            self.alert(wx.ICON_ERROR, u"不支持的网站")
            return

        title = self.website.downloader.title
        url = self.website.downloader.comment_url

        self.video_title_statictext.SetLabel(title)
        self.comment_url_hyperlinkctrl.SetLabel(url)
        self.comment_url_hyperlinkctrl.SetURL(url)
        if self.output_textcrtl.GetValue().strip() == '':
            self.output_textcrtl.SetValue(title + '.ass')

    def font_button_event_handler(self, event):
        font_name, font_size =  self.font_button.GetLabel().split(' | ')
        font_size = int(font_size)
        initial_font = wx.Font(
            font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, face = font_name)
        font_data = wx.FontData()
        font_data.SetInitialFont(initial_font)
        font_data.EnableEffects(True)

        dialog = wx.FontDialog(self.main_window, font_data)

        if dialog.ShowModal() == wx.ID_OK:
            font = dialog.GetFontData().GetChosenFont()
            font_label = "%s | %d" % (
                font.GetFaceName(), font.GetPointSize())
            self.font_button.SetLabel(font_label)

        dialog.Destroy()

    def output_button_event_handler(self, event):
        filename = 'output.ass'
        output = self.output_textcrtl.GetValue().strip()
        if output == '':
            if self.website is not None:
                filename = self.website.downloader.title + '.ass'
            foldername = os.getcwd()
        else:
            foldername, filename = os.path.split(output)

        dialog = wx.FileDialog(self.main_window,
            message=u"请选择一个文件", defaultDir=foldername,
            defaultFile=filename, style=wx.SAVE
        )

        response = dialog.ShowModal()
        if response == wx.ID_OK:
            output = dialog.GetPath()
            if not output.endswith('.ass'):
                output += '.ass'
            self.output_textcrtl.SetValue(output)
        dialog.Destroy()

    def output_textcrtl_event_hanlder(self, event):
        text = self.output_textcrtl.GetValue().strip()
        if text != '' and not text.endswith('.ass'):
            text += '.ass'
        self.output_textcrtl.SetValue(text)

    def convert_button_event_handler(self, event):
        font_name, font_size =  self.font_button.GetLabel().split(' | ')
        font_size = int(font_size)
        video_width = self.video_width_spinbutton.GetValue()
        video_height = self.video_height_spinbutton.GetValue()
        line_count = self.line_count_spinbutton.GetValue()
        bottom_margin = self.bottom_margin_spinbutton.GetValue()
        tune_seconds = self.tune_seconds_spinbutton.GetValue()

        output = self.output_textcrtl.GetValue().strip()
        errors = []
        if self.website is None:
            errors.append(u"未抓取源字幕")
        if output == '':
            errors.append(u"未选择输出路径")

        if len(errors) != 0:
            self.alert(wx.ICON_ERROR, '\n'.join(errors))
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
            self.alert(wx.ICON_ERROR, error)
            return

        message = u"转换成功，文件保存到\n %s" % output
        self.alert(wx.ICON_INFORMATION, message)

    def quit_menuitem_event_handler(self, event):
        self.main_window.Close()

    def about_menuitem_event_handler(self, event):
        webbrowser.open('https://github.com/muzuiget/niconvert#readme')

def main():
    #from wx.lib.inspection import InspectionTool
    app = wx.App(False)
    NiconvertWx().main_window.Show(True)
    #InspectionTool().Show()
    app.MainLoop()

if __name__ == '__main__':
    main()

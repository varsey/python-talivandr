import wx
import wx.html
import modules.config


class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        self.search_box = wx.TextCtrl(panel, 2, style=wx.TE_PROCESS_ENTER)

#        self.text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        self.lst = wx.ListBox(panel, size=(100, -1), style=wx.LB_SINGLE)

        self.label_header = wx.html.HtmlWindow(panel, style=wx.TE_READONLY |
                                                           wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.BORDER_NONE)

        box.Add(self.search_box , 0, wx.EXPAND)
        box.Add(self.lst, 1, wx.EXPAND)
#        box.Add(self.text, 2, wx.EXPAND)
        box.Add(self.label_header, 2, wx.EXPAND)


        panel.SetSizer(box)
        panel.Fit()

        self.Centre()
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst)

        self.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, id=2)

        self.Show(True)

    def Txt_Ent(self, event):
        self.search_button_click(event)

    def onListBox(self, event):
#        self.text.Clear()
        self.label_header.ClearBackground()

        index = event.GetEventObject().GetSelection()
        search_result = self.searching(self.search_box.GetValue())

        self.label_header.SetPage(search_result[index])
#        self.text.AppendText(search_result[index])

#========

    def search_button_click(self, event):
#        self.text.SetValue('')
        search = self.search_box.GetValue()
        self.searching(search)

    def searching(self, str):
        global output_str

        output_str = list()
        notfound = True
        str = str.lower()
        self.lst.Clear()

        if (len(str)) >= 3:
            for x in range(len(modules.config.data)):
#                if len(output_str) > 0:
#                    output_str.clear()
                if str in modules.config.data[x]['Term'] or str in modules.config.data[x]['Translation']:
                    notfound = False
                    self.lst.Append(
                        modules.config.data[x]['Term'] + ' - ' + modules.config.data[x]['Translation'])
                    output_str.append(modules.config.data[x]['Comment'])

        else:
#            self.text.AppendText('Search string is too short')
            self.label_header.SetPage('Search string is too short')

        if notfound == True and (len(str)) >= 3:
#            self.text.AppendText('Nothing found')
            self.label_header.SetPage('Nothing found. Please try again')

        return output_str
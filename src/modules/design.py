import wx
import wx.html
import modules.config


class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(800, 450),
                                    style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel_main = wx.Panel(self)
        self.search_box = wx.TextCtrl(panel_main, 2, style=wx.TE_PROCESS_ENTER)
#        self.search_box.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.BLUE))
        self.results_list = wx.html.SimpleHtmlListBox(panel_main, -1, style=wx.LB_SINGLE | wx.SUNKEN_BORDER)
#        self.lst2 = wx.html.SimpleHtmlListBox (panel_main, -1, style=wx.LB_SINGLE)
        self.comments_section = wx.html.HtmlWindow(panel_main, style=wx.TE_READONLY |
                                                           wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.BORDER_NONE)

        box = wx.BoxSizer(wx.VERTICAL)

        box.Add(self.search_box, 0, wx.EXPAND)
        box.Add(self.results_list, 1, wx.EXPAND)
        box.Add(self.comments_section, 2, wx.EXPAND)

        panel_main.SetSizer(box)

        self.Centre()
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.results_list)
        self.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, id=2)

        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Talivandr!")
        self.Show(True)

####MENU DESCRIPTION
    def makeMenuBar(self):

        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
         wx.MessageBox("Talivandr 5966 © by eugeny.varseev@gmail.com ",
                      "About",
                      wx.OK | wx.ICON_INFORMATION)
###MENU DESCRIPTIONS ENDS HERE###########

    def Txt_Ent(self, event):
        self.searching(self.search_box.GetValue())

    def onListBox(self, event):
        self.comments_section.SetPage('')
        self.comments_section.ClearBackground()

        index = self.results_list.GetSelection() #event.GetEventObject().GetSelection()
        search_result = self.searching(self.search_box.GetValue())
        self.results_list.SetSelection(index)
        self.comments_section.SetPage(search_result[index])
        search_result.clear()

#================================================================================#

    def searching(self, str):
        global output_str
        notfound = True

        self.results_list.Set(())

        output_str = list()
        output_str.clear()

        str = str.lower()

        if (len(str)) >= 3:
            for x in range(len(modules.config.data)):
#                if len(output_str) > 0:
#                    output_str.clear()
                if str in modules.config.data[x]['Term'] or str in modules.config.data[x]['Translation']:
                    notfound = False
                    self.results_list.AppendItems(modules.config.data[x]['Term'] + ' - ' + modules.config.data[x]['Translation'])
                    output_str.append('<h5>' + modules.config.data[x]['Term'] + ' - '
                                      + modules.config.data[x]['Translation'] + '</h5><br /><br />'
                                      + modules.config.data[x]['Comment'])

        else:
#            self.text.AppendText('Search string is too short')
            self.comments_section.SetPage('Search string is too short')

        if notfound == True and (len(str)) >= 3:
#            self.text.AppendText('Nothing found')
            self.comments_section.SetPage('Nothing found. Please try again')

        str = ''
        return output_str
import json
import requests
#from difflib import get_close_matches
import wx
import wx.grid as gridlib

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
#создаем не разворачивающееся окно
        wx.Frame.__init__(self, None, -1, 'pyTalivandr 2.2', size = (620, 430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

#элементы интерфейса
        self.panel = wx.Panel(self)
        self.search_box = wx.TextCtrl(self.panel, 2, style=wx.TE_PROCESS_ENTER, pos = (20, 10), size = (450, 20))
        self.search_box.SetValue('')
        self.comment_box = wx.TextCtrl(self.panel, pos=(20, 40), size=(550, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
#кнопки
        self.search_button = wx.Button(self.panel, label = 'Search', style=wx.ALIGN_LEFT, pos=(480,10),size = (50, 20))
        self.Bind(wx.EVT_BUTTON, self.search_button_click, self.search_button)

        closeBtn = wx.Button(self.panel, label="Exit", style=wx.ALIGN_LEFT, pos=(540,10),size = (30, 20))
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to Talivandr!")

        self.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, id = 2)

#        myGrid = gridlib.Grid(self.panel)
#        myGrid.CreateGrid(12, 8)

    def onClose(self, event):
            self.Close()

    def Txt_Ent(self,event):
           self.search_button_click(event)

    def searching(self, str):
        notfound = True
        if (len(str)) >= 3:
            for x in range(len(data['dict'])):
                if str in data['dict'][x]['Term'] or str in data['dict'][x]['Translation']:
                    notfound = False
                    output_str = ''
                    self.comment_box.AppendText(data['dict'][x]['Term'] + ' - ' + data['dict'][x]['Translation']+'\n\n')
                    for y in range(len(data['dict'][x]['Comment'].split("\\n", -1))):
                        output_str = output_str + data['dict'][x]['Comment'].split("\\n", -1)[y] + "\n"

                    if data['dict'][x]['Comment'].find("Источник") >= 0:
                        output_str = output_str.split("Источник", -1)[y - 1] + "\n" + "Источник" + \
                                     data['dict'][x]['Comment'].split("Источник", -1)[y]
                    self.comment_box.AppendText(
                        output_str + '\n' + '===========================================' + '\n')
        else:
            self.comment_box.AppendText('Search string is too short')
        if notfound == True and (len(str)) >= 3:
            self.comment_box.AppendText('Nothing found')
        return

    def search_button_click(self, event):
        self.comment_box.SetValue('')
        search = self.search_box.GetValue()
        self.searching(search)

#getting data online
try:
    r = requests.get('http://talivandr.site/db/talivandr_db.json')
    open('data', 'wb').write(r.content)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    error_code = err

data = r.json()
json.dumps(data)

app = wx.App(False)
frame = MyFrame(None, "")
frame.Show()
app.MainLoop()
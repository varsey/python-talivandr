import json
import requests
#from difflib import get_close_matches
import wx
import wx.grid as gridlib

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
#создаем не разворачивающееся окно
        wx.Frame.__init__(self, None, -1, 'pyTalivandr 2.1 Beta', size = (620, 430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

#элементы интерфейса
        self.panel = wx.Panel(self)
        self.search_box = wx.TextCtrl(self.panel, pos = (20, 10), size = (450, 20), style=wx.TE_PROCESS_ENTER)
        self.search_box.SetValue('')
        self.comment_box = wx.TextCtrl(self.panel, pos=(20, 40), size=(550, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
#кнопки
        self.search_button = wx.Button(self.panel, label = 'SEARCH', style=wx.ALIGN_CENTER, pos=(480,10),size = (50, 20))
        self.Bind(wx.EVT_BUTTON, self.search_button_click, self.search_button)

        closeBtn = wx.Button(self.panel, label="EXIT", style=wx.ALIGN_CENTER, pos=(540,10),size = (30, 20))
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to Talivandr!")

#        myGrid = gridlib.Grid(self.panel)
#        myGrid.CreateGrid(12, 8)

    def onClose(self, event):
            self.Close()

    def str_split(str):
        number = 0
        while str.split("\\n", -1)[number]:
            output_str = output_str + str.split("\\n", -1)[number]
            number = number + 1
            if str.find("Источник") >= 0:
                print("yes")
                output_str = output_str.split("Источник", -1)[number-1] + "\n" + "Источник" + str.split("Источник", -1)[number]
        return output_str

    def search_button_click(self, event):
        self.comment_box.SetValue('')
        search = self.search_box.GetValue()
        if (len(search))>=3:
            for x in range(len(data['dict'])):
                if search in data['dict'][x]['Term']:
                    output_str = ''
                    self.comment_box.AppendText(
                        "\n" + f"{data['dict'][x]['Term']}" + " - " + f"{data['dict'][x]['Translation']}\n" + "\n")

                    for y in range(len(data['dict'][x]['Comment'].split("\\n", -1))):
                        output_str = output_str + data['dict'][x]['Comment'].split("\\n", -1)[y] + "\n" + "\n"

                    if data['dict'][x]['Comment'].find("Источник") >= 0:
                        output_str = output_str.split("Источник", -1)[y - 1] + "\n\n" + "Источник" + \
                                data['dict'][x]['Comment'].split("Источник", -1)[y] + "\n"

                        self.comment_box.AppendText(output_str + "\n")
                        self.comment_box.AppendText("-------------------------------" +"\n")
        else:
            self.comment_box.AppendText("Please enter more than 3 letters"+"\n")

#getting data online
r = requests.get('http://talivandr.site/db/talivandr_db.json')
data = r.json()
json.dumps(data)

app = wx.App(False)
frame = MyFrame(None, "")
frame.Show()
app.MainLoop()
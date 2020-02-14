import json
from difflib import get_close_matches

data = json.load(open("dictionary.json"))

def retrive_definition(word):
    word = word.lower()

    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:
        return data[word.upper()]
    elif len(get_close_matches(word, data.keys())) > 0:
        self.comment_box.AppendText("We found %s instead: " % get_close_matches(word, data.keys())[0]) #HOW TO OUTPU???
        return data[get_close_matches(word, data.keys())[0]]

import wx
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
#создаем не разворачивающееся окно
        wx.Frame.__init__(self, None, -1, 'pyTalivandr 2.0 Beta', size = (620, 430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
#сквозная вспомогательная переменная-счетчик
        self.index = 0
#        self.state = ''
#элементы интерфейса
        self.panel = wx.Panel(self)
        self.search_box = wx.TextCtrl(self.panel, pos = (20, 10), size = (450, 20), style=wx.TE_PROCESS_ENTER)
        self.search_box.SetValue('')
#        self.search_box.Bind(wx.EVT_TEXT, self.TextChanged, self.search_box)
#        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.TextChanged, self.search_box) #style=wx.TE_PROCESS_ENTER
#вывод текста для отладки
#        self.text_box = wx.TextCtrl(self.panel, pos = (20, 350), size = (300, 200), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.comment_box = wx.TextCtrl(self.panel, pos=(20, 40), size=(550, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
#кнопки
        self.search_button = wx.Button(self.panel, label = 'SEARCH', style=wx.ALIGN_CENTER, pos=(480,10),size = (50, 20))
        self.Bind(wx.EVT_BUTTON, self.search_button_click, self.search_button)

        closeBtn = wx.Button(self.panel, label="EXIT", style=wx.ALIGN_CENTER, pos=(540,10),size = (30, 20))
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to Talivandr!")

    def onClose(self, event):
            self.Close()

    def search_button_click(self, event):
# основной поиск по кнопке
        self.comment_box.SetValue('')
        word_user = self.search_box.GetValue()
        output = retrive_definition(word_user)

        if type(output) == list:
            for item in output:
                self.comment_box.AppendText("- " + f"{item}\n")
#                self.search_box.SetValue("- " + item)
        else:
            self.comment_box.SetValue('')
            self.comment_box.AppendText("- " + f"{output}\n")
#            self.search_box.SetValue("- " + output)


app = wx.App(False)
frame = MyFrame(None, "")
frame.Show()
app.MainLoop()
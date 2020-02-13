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
        wx.Frame.__init__(self, None, -1, 'pyTalivandr 2.0 Beta', size = (800, 430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
#сквозная вспомогательная переменная-счетчик
        self.index = 0
#        self.state = ''
#элементы интерфейса
        self.panel = wx.Panel(self)
        self.search_box = wx.TextCtrl(self.panel, pos = (20, 10), size = (420, 20), style=wx.TE_PROCESS_ENTER)
        self.search_box.SetValue('err')
#        self.search_box.Bind(wx.EVT_TEXT, self.TextChanged, self.search_box)
#        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.TextChanged, self.search_box) #style=wx.TE_PROCESS_ENTER
#таблица
        self.list_box = wx.ListCtrl(self.panel, pos = (20, 40), size = (420, 300), style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.list_box.InsertColumn(0, "ID", width=50)
        self.list_box.InsertColumn(1, "Term", width=200)
        self.list_box.InsertColumn(2, "Translation", width=200)
        self.list_box.InsertColumn(3, "Comment", width=0)
        self.list_box.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_box_dclicked, self.list_box)
#вывод текста для отладки
#        self.text_box = wx.TextCtrl(self.panel, pos = (20, 350), size = (300, 200), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.comment_box = wx.TextCtrl(self.panel, pos=(460, 40), size=(300, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
#кнопки
        self.search_button = wx.Button(self.panel, label = 'SEARCH', style=wx.ALIGN_CENTER, pos=(460,10),size = (60, 20))
        self.Bind(wx.EVT_BUTTON, self.search_button_click, self.search_button)

        closeBtn = wx.Button(self.panel, label="EXIT", style=wx.ALIGN_CENTER, pos=(710,10),size = (40, 20))
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to Talivandr!")

        self.rb1 = wx.RadioButton(self.panel, 11, label='Value A', pos=(530, 10), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.panel, 22, label='Value B', pos=(610, 10))

    def onClose(self, event):
            self.Close()

    def list_box_dclicked(self, event):
# отображаем комментарий по выделению строки в таблице
        ind = event.GetIndex()
        item = self.list_box.GetItem(ind, 3)
#        print (item.GetText())
#для отладки
#        self.text_box.AppendText(f"{'List item selected ' + str(self.index)}\n")
        self.comment_box.SetValue('')
        self.comment_box.AppendText(f"{item.GetText()}\n")
        self.index += 1

    def TextChanged(self, event):
# дейсвтие при изменение текста в поиск (для отображения результатов на лету - пока не работает, слишком медленно)
        self.text_box.AppendText(f"{'The text is changed ' + str(self.index)}\n")
        self.index += 1

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
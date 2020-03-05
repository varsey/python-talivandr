import json
import tempfile
import requests
import wx
import os.path
from os import path

class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        self.search_box = wx.TextCtrl(panel, 2, style=wx.TE_PROCESS_ENTER)

        self.text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        self.lst = wx.ListBox(panel, size=(100, -1), style=wx.LB_SINGLE)

        box.Add(self.search_box , 0, wx.EXPAND)
        box.Add(self.lst, 1, wx.EXPAND)
        box.Add(self.text, 2, wx.EXPAND)

        panel.SetSizer(box)
        panel.Fit()

        self.Centre()
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst)

        self.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, id=2)

        self.Show(True)

    def Txt_Ent(self, event):
        self.search_button_click(event)

    def onListBox(self, event):
        self.text.Clear()

        index = event.GetEventObject().GetSelection()
        search_result = self.searching(self.search_box.GetValue())

        self.text.AppendText(search_result[index])

#========

    def searching(self, str):
        global output_str

        output_str = list()
        notfound = True
        str = str.lower()
        self.lst.Clear()

        if (len(str)) >= 3:
            for x in range(len(data['dict'])):
#                if len(output_str) > 0:
#                    output_str.clear()
                if str in data['dict'][x]['Term'] or str in data['dict'][x]['Translation']:
                    notfound = False
                    self.lst.Append(
                        data['dict'][x]['Term'] + ' - ' + data['dict'][x]['Translation'])
                    output_str.append(data['dict'][x]['Comment'])

        else:
            self.text.AppendText('Search string is too short')

        if notfound == True and (len(str)) >= 3:
            self.text.AppendText('Nothing found')

        return output_str

    def search_button_click(self, event):
        self.text.SetValue('')
        search = self.search_box.GetValue()
        self.searching(search)

#path to file
datafile = tempfile.gettempdir() + '\\' + 'talivata'
temp = tempfile.gettempdir() + '\\' + 'talivandrtemp'

try:
    # downloading a temp
    r = requests.get('http://talivandr.site/db/talivandr_db.json')
    open(temp, 'wb').write(r.content)
    r.raise_for_status()
    data = r.json()
    print("Temp data written")

    # checking for changes and updating if yes
    if path.exists(datafile) and (os.stat(datafile).st_size != os.stat(temp).st_size):
        os.rename(temp, datafile)
        print('Temp is diffrent, data updated')

    if path.exists(datafile) == False:
        os.rename(temp, datafile)
        print('Temp renamed')

except:
    print("Connection failed")
    # opening existing file if no connection
    if path.exists(datafile):
        with open(datafile, encoding="utf8") as f:
            data = json.load(f)
            print("File exist")

ex = wx.App()
Mywin(None, 'pyTalivandr 2.3')
ex.MainLoop()
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
#создаем не разворачивающееся окно
        wx.Frame.__init__(self, None, -1, 'pyTalivandr 2.1 Beta', size = (620, 430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.Text_Enter = wx.TextCtrl(self , 2 ,style = wx.TE_PROCESS_ENTER, size =(125,150), pos = (170,0))
        self.Text_Enter.SetForegroundColour(wx.RED)
        self.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, id = 2)

    def Txt_Ent(self,event):
           msg1 = (str(self.Text_Enter.GetValue()))
           wx.MessageBox(msg1)

app = wx.App(False)
frame = MyFrame(None, "")
frame.Show()
app.MainLoop()
import wx
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
#создаем не разворачивающееся окно
        wx.Frame.__init__(self, None, -1, 'pyTalivandr Beta', size = (800, 430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
#сквозная вспомогательная переменная-счетчик
        self.index = 0
#        self.state = ''
#элементы интерфейса
        self.panel = wx.Panel(self)
        self.search_box = wx.TextCtrl(self.panel, pos = (20, 10), size = (420, 20), style=wx.TE_PROCESS_ENTER)
        self.search_box.SetValue('Enter phrase here and click "search" button ->')
        self.search_box2 = wx.TextCtrl(self.panel, pos = (505, 10), size = (200, 20), style=wx.TE_PROCESS_ENTER)
        self.search_box2.SetValue('Enter abbrev here and hit "Abbrev"->')
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
        self.search_button = wx.Button(self.panel, label = 'Search', style=wx.ALIGN_CENTER, pos=(460,10),size = (40, 20))
        self.Bind(wx.EVT_BUTTON, self.search_button_click, self.search_button)
        self.abbrev_button = wx.Button(self.panel, label='Abbrev', style=wx.ALIGN_CENTER, pos=(710, 10), size=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.abbrev_button_click, self.abbrev_button)

#############КРАСИВОЕ МЕНЮ (необозательно)#######################
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Talivandr!")

    def makeMenuBar(self):

        fileMenu = wx.Menu()

        helloItem = fileMenu.Append(-1, "&Search\tCtrl-H",
                                    "Help string shown in status bar for this menu item")
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
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)

    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox("No action yet on this click. Sorry")

    def OnAbout(self, event):
         wx.MessageBox("Talivandr Dictionary 5966 v2.0 ©\n \n August 2019 by eugeny.varseev@gmail.com ",
                      "About",
                      wx.OK | wx.ICON_INFORMATION)
#############SOME UNNESSESARY BULSHIT ENDS HERE###################

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
        import configparser, pymysql.cursors

        self.index = 0
        self.search_box2.SetValue('')
# настраиваем забор имя пользователя и пароля из отдельного файла
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')
# настройка подключения
        connection = pymysql.connect(host='sql7.freesqldatabase.com',
                                     user=config.get('mysql', 'user'),
                                     password=config.get('mysql', 'password'),
                                     db=config.get('mysql', 'db'),
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        try:
#            with connection.cursor() as cursor:
#                    sql = "SELECT Term, Translation FROM dict LIMIT 1"
#                    cursor.execute(sql)
# подключение
            connection.commit()

            self.SetStatusText("Connection succesfull")

            with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT ID, Term, Translation, Comment FROM dict WHERE Term LIKE %s OR Translation LIKE %s"
                    cursor.execute(sql, ('%'+self.search_box.GetValue()+'%', '%'+self.search_box.GetValue()+'%'))
                    result = cursor.fetchall() #fetchmany(10) or fetchall
# очищщаем талбицу
                    self.list_box.DeleteAllItems()
# заполняем таблицу результатом
                    for row in result:
                        self.list_box.Append((row["ID"], row["Term"], row["Translation"], row["Comment"]))
                        self.index += 1

        finally:
                connection.close()
# служебная информация для отладки
#        self.text_box.AppendText(f"{'Success, number of results '+ str(self.index)}\n")

    def abbrev_button_click(self, event):
#  поиск в комментариях аналогично основному
        import configparser, pymysql.cursors

        self.index = 0

        self.search_box.SetValue('')

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')

        connection = pymysql.connect(host='sql7.freesqldatabase.com',
                                     user=config.get('mysql', 'user'),
                                     password=config.get('mysql', 'password'),
                                     db=config.get('mysql', 'db'),
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                    sql = "SELECT Term, Translation FROM dict LIMIT 1"
                    cursor.execute(sql)

            connection.commit()

            self.SetStatusText("Connection succesfull")

            with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT ID, Term, Translation, Comment FROM dict WHERE" \
                          " Comment LIKE %s"
                    cursor.execute(sql, ('%'+self.search_box2.GetValue()+'%',))
                    result = cursor.fetchall() #fetchmany(10) or fetchall

                    self.list_box.DeleteAllItems()

                    for row in result:
                        self.list_box.Append((row["ID"], row["Term"], row["Translation"], row["Comment"]))
                        self.index += 1

        finally:
                connection.close()
# служебная информация для отладки
#        self.text_box.AppendText(f"{'Success, number of results '+ str(self.index)}\n")

app = wx.App(False)
frame = MyFrame(None, "")
frame.Show()
app.MainLoop()
import json
import tempfile
import requests
import os.path
from shutil import move
from os import path
import modules.design
import modules.config


def searching(self, str):
    notfound = True
    str = str.lower()
    if (len(str)) >= 3:
        for x in range(len(data['dict'])):
            if str in data['dict'][x]['Term'] or str in data['dict'][x]['Translation']:
                notfound = False
                output_str = ''
                self.list_box.AppendText(
                    data['dict'][x]['Term'] + ' - ' + data['dict'][x]['Translation'] + '\n\n')
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

#path to file
datafile = tempfile.gettempdir() + '\\' + 'talivata'
temp = tempfile.gettempdir() + '\\' + 'talivandrtemp'

try:
    # downloading a temp file
    r = requests.get('http://varsey.pythonanywhere.com/static/talivandr_db.json') #http://talivandr.site/db/talivandr_db1.json')
    open(temp, 'wb').write(r.content)
    r.raise_for_status()
    modules.config.data = r.json()
    #data = json.load(temp)
    print("Temp data written: " + str(len(modules.config.data)) + " entries")

    # checking for changes and updating if yes
    if path.exists(datafile) and (os.stat(datafile).st_size != os.stat(temp).st_size):
        move(temp, datafile) #os.rename(temp, datafile)
        print('Local DB updated: ' + str(len(modules.config.data)) + " entries")

    #if file does not exist - rename temp
    if path.exists(datafile) == False:
        move(temp, datafile) #os.rename(temp, datafile)
        print('Local DB cached: ' + str(len(modules.config.data)) + " entries")

except Exception as ex:
    print("Something went wrong: " + str(ex))
    # opening existing file if no connection
    if path.exists(datafile):
        with open(datafile, encoding="utf8") as f:
            data = json.load(f)
            print("Local DB loaded: " + str(len(modules.config.data)) + " entries")

app = modules.design.wx.App(False)
frame = modules.design.Mywin(None, "pyTalivandr 2.4")
frame.Show()
app.MainLoop()

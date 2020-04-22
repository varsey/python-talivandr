import json
import tempfile
import requests
import os.path
from shutil import move
from os import path
import modules.design
import modules.config


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
modules.design.Mywin.SetStatusText(frame, str(len(modules.config.data)) + " entries in database")
frame.Show()
app.MainLoop()
import urllib

url = "http://talivandr.site/db/talivandr_db.json"

file_name = url.split('/')[-1]
u = urllib.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print("Downloading: %s Bytes: %s" % (file_name, file_size))
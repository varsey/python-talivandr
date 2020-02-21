import json
import requests

r = requests.get('http://talivandr.site/db/talivandr_db.json')
data = r.json()
json.dumps(data)

my_string="ENG: A facility (including associated buildings and equipment) in which nuclear material is produced, processed, used, handled, stored or disposed of.\\nRUS: ЯЭУ - ядерная энергетическая установка"

output_str = ''
x = 999
print(data['dict'][x]['Term'] + ' - ' + data['dict'][x]['Translation'])
for y in range(len(data['dict'][x]['Comment'].split("\\n", -1))):
    output_str = output_str + data['dict'][x]['Comment'].split("\\n", -1)[y] + "\n"
#    output_str = output_str + "Источник - " + data['dict'][x]['Comment'].split("Источник", 1)[y] + "\n"

if data['dict'][x]['Comment'].find("Источник") >= 0:
        print("YES")
        output_str = output_str.split("Источник", -1)[y-1] + "\n"+ "Источник"  + data['dict'][x]['Comment'].split("Источник", -1)[y]
else:
        print("NO")

print(output_str)

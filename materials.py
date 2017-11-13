import json
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#data is copied to clipboard, used for the http://cddawiki.chezzo.com/cdda_wiki/index.php?title=Materials page

with open('data/json/materials.json') as data_file:    
    data = json.load(data_file)

output = [ "" ]
for it in range(0, len(data)):
    output.append("{{row/{{PAGENAME}}|mat=")
    output.append(data[it]['ident'])
    output.append("|name=")
    output.append(data[it]['name'])
    output.append("|bashdv=")
    output.append(data[it]['bash_dmg_verb'])
    output.append("|cutdv=")
    output.append(data[it]['cut_dmg_verb'])
    output.append("|dmgadj1=")
    output.append(data[it]['dmg_adj'][0])
    output.append("|dmgadj2=")
    output.append(data[it]['dmg_adj'][1])
    output.append("|dmgadj3=")
    output.append(data[it]['dmg_adj'][2])
    output.append("|dmgadj4=")
    output.append(data[it]['dmg_adj'][3])
    output.append("|density=")
    output.append(str(data[it]['density']))
    if('edible' in  data[it]):
        if(data[it]['edible'] == True):
            output.append("|edible=Y")
    if('soft' in  data[it]):
        if(data[it]['soft'] == True):
            output.append("|soft=Y")        
        
    output.append("}}\n\n")

text = "".join(output)
text.replace("\n", "\\n")
print text
root.clipboard_clear()
root.clipboard_append(text)
root.update()
root.destroy()
exit()
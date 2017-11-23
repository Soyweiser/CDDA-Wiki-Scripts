import json
import sys
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#Data is copied to clipboard, used for the http://cddawiki.chezzo.com/cdda_wiki/index.php?title=Bionics generates the non faulty bionics list, if used without a command line argument, and if the command True is given, will list the faulty bionics.

with open('data/json/bionics.json') as data_file:    
    data = json.load(data_file)

ID_bionic = list()
for iterator in range(0, len(data)):
    if(len(sys.argv) > 1):
        if(str(sys.argv[1]).lower() == "true"):
            if("faulty" in data[iterator]): #faulty
                if((data[iterator]['faulty'] == True)):
                    ID_bionic.append(data[iterator]["name"])
    else:
        if("faulty" in data[iterator]): #only add bionics that are not faulty to this list.
            if(not (data[iterator]['faulty'] == True)):
                ID_bionic.append(data[iterator]["name"])
        else:
            ID_bionic.append(data[iterator]["name"])

ID_bionic.sort()

output = [ "" ]
if(len(sys.argv) > 1):
    if(str(sys.argv[1]).lower() == "true"):
        output.append("{{header/FaultyBionics}}\n")
else:
    output.append("{{header/Bionics}}\n")
output.append("<!--Automatically generated using https://github.com/Soyweiser/CDDA-Wiki-Scripts -->\n\n")
for it in range(0, len(ID_bionic)):
    output.append("{{:")
    output.append(ID_bionic[it])
    output.append("}}\n")
output.append("</table>\n")

text = "".join(output)
text.replace("\n", "\\n")
print text
root.clipboard_clear()
root.clipboard_append(text)
root.update()
root.destroy()
exit()
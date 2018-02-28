import json
import sys
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#data is copied to clipboard, used for the Template:Matbashres, Matfireres, Matcutres, Matelecres, Matacidres
#takes a command line argument, must be the json data field you are interested in. for example 'acid_resist'

with open('data/json/materials.json') as data_file:
    data = json.load(data_file)

output = [ "" ]
for it in range(0, len(data)):
    output.append("  |")
    output.append(data[it]['ident'])
    output.append(" = ")
    output.append(str(data[it][sys.argv[1]]))
    output.append("\n")

text = "".join(output)
text.replace("\n", "\\n")
print text
root.clipboard_clear()
root.clipboard_append(text)
root.update()
root.destroy()
exit()
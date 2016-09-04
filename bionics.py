import json
import sys
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#Data is copied to clipboard, used for the Bionics

with open('data/json/bionics.json') as data_file:    
    data = json.load(data_file)

with open('data/json/items/bionics.json') as data_file:    
    data1 = json.load(data_file)

output = []

def ID_To_WikiString(id):
    if id == "Infrared Vision":
        return "Infrared Vision (Mutation)|Infrared Vision"
    return id

ID_bionic = dict()
for iterator in range(0, len(data)):
    keyD = dict()
    keyD['id_nr'] = iterator
    keyD["name"] = data[iterator]["name"]
    ID_bionic[data[iterator]["id"]] = keyD

ID_bio_item = dict()
for iterator in range(0, len(data1)):
    keyD = dict()
    keyD['id_nr'] = iterator
    keyD["name"] = data1[iterator]["name"]
    ID_bio_item[data1[iterator]["id"]] = keyD

    
def ID_To_String(id):
    return ID_bionic[id]["name"]

def ID_To_Bio_Int(id):
    if(id in ID_bionic):
        return ID_bionic[id]["id_nr"]
    else:
        return -1

def ID_To_Item_String(id):
    return ID_bionic[id]["name"]
        
def ID_To_Item_Int(id): #this should return the location of the bionic inside the items file. However, not all bionics have items.
    if(id in ID_bio_item):
        return ID_bio_item[id]["id_nr"]
    else:
        return -1

var = raw_input(">")
while True:
    while var.isdigit():
        var = int(var)
        if(var < 0):
            root.update()
            root.destroy()
            exit()
        output = []
        
        #Add item if this bionic is made from an item.
        if( ID_To_Item_Int(data[var]['id']) != -1):
            item_id = ID_To_Item_Int(data[var]['id'])
            output.append( """<noinclude>{{Infobox/Bionics</noinclude>
<includeonly>{{Row/Bionics</includeonly>
 |name=""" )
            output.append(data1[item_id]['name'])
            output.append("\n|id=")
            output.append(data1[item_id]['id'])
            output.append("\n|glyph=")
            output.append(data1[item_id]['symbol'])
            output.append("\n|symbol=")
            output.append(data1[item_id]['color'])
            output.append("\n")

        text = "".join(output)
        text.replace("\n", "\\n")
        print text
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        var = raw_input(">")
    else:
        if ( var == 'exit' ):
            root.update()
            root.destroy()
            exit()
        else:
            print ID_To_int(var)
            var = raw_input(">")
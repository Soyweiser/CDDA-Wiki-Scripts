import json
import sys
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#Data is copied to clipboard, used for the Faulty Bionics, or bionics without a CBM item, which means they cannot be directly installed, do not use on normal bionics (with a direct CBM).

with open('data/json/bionics.json') as data_file:    
    data = json.load(data_file)

output = []

ID_bionic = dict()
for iterator in range(0, len(data)):
    keyD = dict()
    keyD['id_nr'] = iterator
    keyD["name"] = data[iterator]["name"]
    ID_bionic[data[iterator]["id"]] = keyD

def ID_To_String(id):
    return ID_bionic[id]["name"]

def ID_To_Bio_Int(id):
    if(id in ID_bionic):
        return ID_bionic[id]["id_nr"]
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
        
        output.append( """<noinclude>{{Infobox/Bionics</noinclude>
<includeonly>{{Row/Bionics</includeonly>
|name=""" )
        output.append(data[var]['name'])
        output.append("\n|b_id=")
        output.append(str(data[var]['id']))
        output.append("\n|b_name=")
        output.append(data[var]['name'])
        if('capacity' in data[var]):
            output.append("\n|capacity=")
            output.append(str(data[var]['capacity']))
        if('toggled' in data[var]):
            output.append("\n|toggled=")
            output.append(str(data[var]['toggled']).lower())
        if('power_source' in data[var]):
            output.append("\n|power_source=")
            output.append(str(data[var]['power_source']))
        if('act_cost' in data[var]):
            output.append("\n|act_cost=")
            output.append(str(data[var]['act_cost']))
        if('react_cost' in data[var]):
            output.append("\n|react_cost=")
            output.append(str(data[var]['react_cost']))
        if('time' in data[var]):
            output.append("\n|time=")
            output.append(str(data[var]['time']))
        if('deact_cost' in data[var]):
            output.append("\n|deact_cost=")
            output.append(str(data[var]['deact_cost']))
        if('faulty' in data[var]):
            output.append("\n|faulty=")
            output.append(str(data[var]['faulty']).lower())
        if('description' in data[var]):
            output.append("\n|b_description=")
            output.append(str(data[var]['description']))

        #footer
        output.append("""\n}}<noinclude>
==Notes==
""")
        if('occupied_bodyparts' in data[var]):
            output.append("* Uses the following [[Bionics#Bionic_Slots|bionic slot(s)]]:\n")
            for it in range(0, len(data[var]["occupied_bodyparts"])):
                output.append("** {{btt|")
                output.append(str(data[var]["occupied_bodyparts"][it][0]))
                output.append("}} ")
                output.append(str(data[var]["occupied_bodyparts"][it][1]))
                output.append(".\n")
        if('faulty' in data[var]):
            output.append("* This is considered a [[Bionics#Malfunctioning_bionics|malfunctioning bionic]].\n")
        if('capacity' in data[var]):
            output.append("* This bionic adds ")
            output.append(str(data[var]['capacity']))
            output.append(" capacity.\n")
        if('power_source' in data[var]):
            output.append("* This bionic a source of power. The actual type of power source depends on the item. Could be solar, kinetic, atomics, or anything else.\n")
        if('toggled' in data[var] or 'act_cost' in data[var]):
            output.append("* This bionic can be turned on, which might have an power cost.\n")
        if('react_cost' in data[var]):
            output.append("* This bionic can react automatically, which costs ")
            output.append(str(data[var]['react_cost']))
            output.append(" power units.\n")
        if('included_bionics' in data[var]):
            output.append("* Installing this bionic also gives the")
            for it in range(0, len(data[var]["included_bionics"])):
                if (it > 0):
                    output.append(",")
                output.append(" [[")
                output.append(ID_To_String(data[ID_To_Bio_Int(str(data[var]['included_bionics'][it]))]['id']))
                output.append("]]")
            output.append(" bionic")
            if (len(data[var]["included_bionics"]) > 0):
                output.append("s")
            output.append(".\n")
        if('fake_item' in data[var]):
            output.append("* This gives the use of the following 'fake item' [http://cdda-trunk.chezzo.com/")
            output.append(str(data[var]['fake_item']))
            output.append(" ")
            output.append(str(data[var]['fake_item']))
            output.append("]")
            if('toggled' in data[var] or 'act_cost' in data[var]):
                output.append(" when activated")
            output.append(".\n")
        if('gun_bionic' in data[var]):
            output.append("* This bionic counts as a gun.\n")
        if('weapon_bionic' in data[var]):
            output.append("* This bionic counts as a weapon.\n")
        if('time' in data[var]):
            output.append("* This bionic has an over time effect.\n")

        output.append("""<!-- *YOUR PERSONAL NOTES AND HINTS GO BELOW HERE* -->

[[Category:CBMs]]
{{footer/CBM}}
{{ver|0.D}}
</noinclude>""")
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
            print ID_To_Bio_Int(var)
            var = raw_input(">")
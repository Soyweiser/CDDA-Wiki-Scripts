import json
import sys
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#Data is copied to clipboard, used for the Bionics, doesn't work on bionics that are not defined in 'data\json\bionics.json'

with open('data/json/bionics.json') as data_file:
    data = json.load(data_file)

with open('data/json/items/bionics.json') as data_file:
    data1 = json.load(data_file)

with open('data/json/mutations.json') as data_file:
    mutation_data = json.load(data_file)

ID_mut = dict()
for iterator in range(0, len(mutation_data)):
    keyD = dict()
    keyD['id_nr'] = iterator
    keyD["name"] = mutation_data[iterator]["name"]
    ID_mut[mutation_data[iterator]["id"]] = keyD
    
def MUT_ID_To_String(id):
    return ID_mut[id]["name"]

output = []

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
    if ('id' in data1[iterator]):
        ID_bio_item[data1[iterator]["id"]] = keyD
    else:
        data1[iterator]["id"] = data1[iterator]["abstract"]
        ID_bio_item[data1[iterator]["id"]] = keyD

def ID_To_String(id):
    return ID_bionic[id]["name"]

def ID_To_Bio_Int(id):
    if(id in ID_bionic):
        return ID_bionic[id]["id_nr"]
    else:
        return -1

def ID_To_Item_String(id):
    return ID_bio_item[id]["name"]
        
def ID_To_Item_Int(id): #should return the location of the bionic inside the items file. However, not all bionics have items.
    if(id in ID_bio_item):
        return ID_bio_item[id]["id_nr"]
    else:
        return -1

def getValue(id, value): #returns the value field of the bionic item. It is a recursive function that takes into account the abstract item.
    if(value in data1[id]):
        return data1[id][value]
    else:
        return getValue(ID_To_Item_Int(data1[id]["copy-from"]), value)

def checkValue(id, value): #returns if the value field is defined in the item description. Or if it is defined in on of the abstracts.
    if(value in data1[id]):
        return True
    if("copy-from" in data1[id]):
        return checkValue(ID_To_Item_Int(data1[id]["copy-from"]), value)
    else:
        return False

var = raw_input(">")
while True:
    while var.isdigit():
        var = int(var)
        if(var < 0):
            root.update()
            root.destroy()
            exit()
        output = []
        
#        if(ID_To_Item_Int(data[var]['id']) == -1):
#            sys.stdout.write("bionic does not have an CBM item, use bionicsFaulty.py to generate instead.")

        #Add item if this bionic is made from an item.
        if(ID_To_Item_Int(data[var]['id']) != -1):
            item_id = ID_To_Item_Int(data[var]['id'])
            #don't print if it is the abstract bionic.
            if( not "abstract" in data1[item_id]):
                output.append( """<noinclude>{{Infobox/Bionics</noinclude>
<includeonly>{{Row/Bionics</includeonly>
|name=""" )
                output.append(data1[item_id]['name'])
                output.append("\n|id=")
                output.append(data1[item_id]['id'])
                output.append("\n|b_id=")
                output.append(str(data[var]['id']))
                output.append("\n|glyph=")
                output.append(getValue(item_id,'symbol'))
                output.append("\n|color=")
                output.append(getValue(item_id,'color'))
                for it in range(0, len(getValue(item_id,'material'))):
                    output.append("\n|mat")
                    output.append(str(it+1))
                    output.append("=")
                    output.append(getValue(item_id,'material')[it])
                output.append("\n|volume=")
                output.append(str(getValue(item_id,'volume')))
                output.append("\n|weight=")
                output.append(str(getValue(item_id,'weight')))
                output.append("\n|b_name=")
                output.append(ID_To_String(data1[item_id]['id']))
                output.append("\n|difficulty=")
                output.append(str(getValue(item_id,'difficulty')))
                if('capacity' in data[var]):
                    output.append("\n|capacity=")
                    output.append(str(data[var]['capacity']))
                if('flags' in data[var]):
                    if('BIONIC_TOGGLED' in data[var]['flags']):
                        output.append("\n|toggled=true")
                if('flags' in data[var]):
                    if('BIONIC_POWER_SOURCE' in data[var]['flags']):
                        output.append("\n|power_source=true")
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
                if('flags' in data[var]):
                    if('BIONIC_FAULTY' in data[var]['flags']):
                        output.append("\n|faulty=true")
                if(checkValue(item_id,'price')):
                    output.append("\n|price=")
                    output.append(str(getValue(item_id,'price')))
                else:
                    output.append("\n|price=0")
                if(checkValue(item_id,'bashing')):
                    output.append("\n|bash=")
                    output.append(str(getValue(item_id,'bashing')))
                else:
                    output.append("\n|bash=0")
                if(checkValue(item_id,'cut')):
                    output.append("\n|cut=")
                    output.append(str(getValue(item_id,'cut')))
                else:
                    output.append("\n|cut=0")
                if(checkValue(item_id,'tohit')):
                    output.append("\n|tohit=")
                    output.append(str(getValue(item_id,'tohit')))
                else:
                    output.append("\n|tohit=0")
                if(checkValue(item_id,'description')):
                    output.append("\n|description=")
                    output.append(str(getValue(item_id,'description')))
                if('description' in data[var]):
                    output.append("\n|b_description=")
                    output.append(str(data[var]['description']))
        else: #bionic doesn't have an item. Which probably means it is a faulty bionic.
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
            if('flags' in data[var]):
                if('BIONIC_TOGGLED' in data[var]['flags']):
                    output.append("\n|toggled=true")
            if('flags' in data[var]):
                if('BIONIC_POWER_SOURCE' in data[var]['flags']):
                    output.append("\n|power_source=true")
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
            if('flags' in data[var]):
                if('BIONIC_FAULTY' in data[var]['flags']):
                    output.append("\n|faulty=true")
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
        if('flags' in data[var]):
            if('BIONIC_FAULTY' in data[var]['flags']):
                output.append("* This is considered a [[Bionics#Malfunctioning_bionics|malfunctioning bionic]].\n")
        if('capacity' in data[var]):
            output.append("* This bionic adds ")
            output.append(str(data[var]['capacity']))
            output.append(" capacity.\n")
        if('flags' in data[var]):
            if('BIONIC_POWER_SOURCE' in data[var]['flags']):
                output.append("* This bionic is a source of power. The actual type of power source depends on the item. Could be solar, kinetic, atomics, or anything else.\n")
        toggle = False
        if('flags' in data[var]):
            if('BIONIC_TOGGLED' in data[var]['flags']):
                toggle = True
                output.append("* This bionic can be turned on, which might have an power cost.\n")
        if(not toggle):
            if('act_cost' in data[var]):
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
            if (len(data[var]["included_bionics"]) > 1):
                output.append("s")
            output.append(".\n")
        if('fake_item' in data[var]):
            output.append("* This gives the use of the following 'fake item' [http://cdda-trunk.chezzo.com/")
            output.append(str(data[var]['fake_item']))
            output.append(" ")
            output.append(str(data[var]['fake_item']))
            output.append("]")
            toggle = False
            if('flags' in data[var]):
                if('BIONIC_TOGGLED' in data[var]['flags']):
                    toggle = True
                    output.append(" when activated")
            if(not toggle):
                if('act_cost' in data[var]):
                    output.append(" when activated")
            output.append(".\n")
        if('flags' in data[var]):
            if('BIONIC_GUN' in data[var]['flags']):
                output.append("* This bionic counts as a gun.\n")
        if('flags' in data[var]):
            if('BIONIC_WEAPON' in data[var]['flags']):
                output.append("* This bionic counts as a weapon.\n")
        if('time' in data[var]):
            output.append("* This bionic has an over time effect.\n")
        if('upgraded_bionic' in data[var]):
            output.append("* When installed this bionic upgrades the [[")
            output.append(ID_To_String(data[ID_To_Bio_Int(str(data[var]['upgraded_bionic']))]['id']))
            output.append("]] bionic. The old bionic will be removed.\n")
        if('canceled_mutations' in data[var]):
            output.append("* When installed this bionic removes the following [[Mutation|mutations]]:\n")
            for it in range(0, len(data[var]["canceled_mutations"])):
                output.append("** [[")
                output.append(MUT_ID_To_String(str(data[var]["canceled_mutations"][it])))
                output.append("]]\n")
        if('flags' in data[var]):
            if('BIONIC_ARMOR_INTERFACE' in data[var]['flags']):
                output.append("* This bionic can provide power to [[Power armor|powered armor]].\n")

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
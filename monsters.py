import json
import sys
from version import version
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#Data is copied to clipboard, used for the Monsters

list_monster_files = [ 'data/json/monsters.json', 'data/json/monsters/bird.json', 'data/json/monsters/defense_bot.json', 'data/json/monsters/drones.json', 'data/json/monsters/fish.json', 'data/json/monsters/insect_spider.json', 'data/json/monsters/mammal.json', 'data/json/monsters/military.json', 'data/json/monsters/reptile_amphibian.json', 'data/json/monsters/triffid.json', 'data/json/monsters/zed_children.json', 'data/json/monsters/zed_explosive.json' ]

list_monster_egg_files = [ 'data/json/items/comestibles/egg.json' ]

data = list()

ID_monster = dict()

def merge_json_data(x,y): #expects two lists
    retval = x + y
    return retval

def check_duplicates(x,y): #check if there are duplicate ID's which might mess things up. Takes two lists as arguments.
    for iterator in range(0, len(x)):
        if ('id' in x[iterator]): #check for abstract item ID's.
            id = x[iterator]["id"]
            for iterator2 in range(0, len(y)):
                if ('id' in y[iterator2]): #abstract check.
                    if (id == y[iterator2]["id"]):
                        print "duplicate ID detected " + str(id)

def setAbstractIds(data): #some items have no ID value set, which this code depends on, but they do have an abstract. This function copies the abstract value into the id value.
    for it in range(0, len(data)):
        if(not 'id' in data[it]):
            if('abstract' in data[it]):
                data[it]['id'] = data[it]['abstract']
            else:
                print 'both no id and no abstract detected ' + str(it)
    return data

def ID_To_String(id):
    return getValue(ID_monster[id]["id_nr"],'name')

def ID_To_Mon_Int(id):
    if(id in ID_monster):
        return ID_monster[id]["id_nr"]
    else:
        return -1

def getValue(id, value): #returns the value field of the monster, takes into account 'copy-from'.
    if(value in data[id]):
        return data[id][value]
    else:
        return getValue(ID_To_Mon_Int(data[id]["copy-from"]), value)

def checkValue(id, value): #returns if the value field is defined in the monster description, takes into account 'copy-from'.
    if(value in data[id]):
        return True
    if("copy-from" in data[id]):
        return checkValue(ID_To_Mon_Int(data[id]["copy-from"]), value)
    else:
        return False

def hasFlag (object, flag): #returns true if this json object has the flag defined in its "flags" list.
    if('flags' in object):
        if(flag in object['flags']):
            return True
    return False

def fill_ID_List (data):
    retval = dict()
    for iterator in range(0, len(data)):
        keyD = dict()
        keyD['id_nr'] = iterator
        retval[data[iterator]["id"]] = keyD
    return retval

## Egg items
for it in range(0, len(list_monster_egg_files)):
    with open(list_monster_egg_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (data, new_data)
        data = merge_json_data(data, new_data)
eggData = setAbstractIds(data)

def getEggName(id):
    for it in range(0, len(eggData)):
        if(eggData[it]['id'] == id):
            if('name'in eggData[it]):
                return eggData[it]['name']
            else:
                return "Egg doesn't have name set"

## Species
with open('data/json/species.json') as data_file:
    species = json.load(data_file)

def species_tostring (id):
    for it in range(0, len(species)):
        if(species[it]['id'] == id):
            return species[it]['name']
    return "species not found"

def species_categories (species_list): #species_list is a list of species, prints a list of categories
    retval = ""
    for it in range(0, len(species_list)):
        retval += "[[Category:"+species_tostring(species_list[it])+"]]\n"
    return retval

output = []

for it in range(0, len(list_monster_files)):
    with open(list_monster_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (data, new_data)
        data = merge_json_data(data, new_data)
data = setAbstractIds(data)
ID_monster = fill_ID_List(data)

Species_to_text = dict()
for iterator in range(0, len(species)):
    Species_to_text[species[iterator]["id"]] = species[iterator]["name"]

var = raw_input(">")
while True:
    while var.isdigit():
        var = int(var)
        if(var < 0):
            root.update()
            root.destroy()
            exit()
        output = []
        
        if(ID_To_Mon_Int(data[var]['id']) != -1):
            id = ID_To_Mon_Int(data[var]['id'])
            if('debug' in data[id]):
                if(data[id]['debug'] == 'true'):
                    break
            #don't print if it is the abstract
            if( not "abstract" in data[id]):
                output.append( """<noinclude>{{enemydescription</noinclude>
<includeonly>{{Row/Enemies1</includeonly>""")
                output.append("\n|name="+getValue(id,'name'))
                output.append("\n|id="+getValue(id, 'id'))
                if(checkValue(id, 'symbol')):
                    output.append("\n|glyph=<nowiki>"+getValue(id, 'symbol')+"</nowiki>")
                if(checkValue(id, 'color')):
                    output.append("\n|color="+getValue(id, 'color'))
                if(checkValue(id, 'hp')):
                    output.append("\n|hitpoints="+str(getValue(id, 'hp')))
                if(checkValue(id, 'species')):
                    species_list = getValue(id, 'species')
                    output.append("\n|species=")
                    for it in range(0, len(species_list)):
                        if (it > 0):
                            output.append(", ")
                        output.append(species_list[it])
                if(checkValue(id, 'size')):
                    output.append("\n|size="+getValue(id, 'size'))
                if(checkValue(id, 'material')):
                    mat = getValue(id, 'material')
                    output.append("\n|material=")
                    for it in range(0, len(mat)):
                        if (it > 0):
                            output.append(", ")
                        output.append(mat[it])
                if(checkValue(id, 'phase')):
                    output.append("\n|phase="+getValue(id, 'phase').lower())
                if(checkValue(id, 'diff')):
                    output.append("\n|difficulty="+str(getValue(id, 'diff')))
                if(checkValue(id, 'aggression')):
                    output.append("\n|aggression="+str(getValue(id, 'aggression')))
                if(checkValue(id, 'speed')):
                    output.append("\n|speed="+str(getValue(id, 'speed')))
                if(checkValue(id, 'melee_skill')):
                    output.append("\n|meleesk="+str(getValue(id, 'melee_skill')))
                if(checkValue(id, 'melee_dice')):
                    output.append("\n|meleedamage="+str(getValue(id, 'melee_dice')))
                else:
                    output.append("\n|meleedamage=")
                if(checkValue(id, 'melee_dice_sides')):
                    output.append("d"+str(getValue(id, 'melee_dice_sides')))
                if(checkValue(id, 'melee_cut')):
                    output.append("\n|cutdamage="+str(getValue(id, 'melee_cut')))
                if(checkValue(id, 'dodge')):
                    output.append("\n|dodgesk="+str(getValue(id, 'dodge')))
                if(checkValue(id, 'armor_bash')):
                    output.append("\n|basharmor="+str(getValue(id, 'armor_bash')))
                if(checkValue(id, 'armor_cut')):
                    output.append("\n|cutarmor="+str(getValue(id, 'armor_cut')))
                if(checkValue(id, 'armor_fire')):
                    output.append("\n|armor_fire="+str(getValue(id, 'armor_fire')))
                if(checkValue(id, 'armor_acid')):
                    output.append("\n|armor_acid="+str(getValue(id, 'armor_acid')))
                if(checkValue(id, 'flags')):
                    flags = getValue(id, 'flags')
                    for it in range(0, len(flags)):
                        output.append("\n|flag"+str(it+1)+"=")
                        output.append(flags[it])
                if(checkValue(id, 'special_attacks')):
                    attacks = getValue(id, 'special_attacks')
                    for it in range(0, len(attacks)):
                        output.append("\n|specialabil"+str(it+1)+"=")
                        if( isinstance( attacks[it], list)):
                            output.append(attacks[it][0])
                        elif( isinstance( attacks[it], dict)):
                            if('type' in attacks[it]):
                                output.append(attacks[it]['type'])
                    for it in range(0, len(attacks)):
                        output.append("\n|specialtime"+str(it+1)+"=")
                        if( isinstance( attacks[it], list)):
                            output.append(str(attacks[it][1]))
                        elif( isinstance( attacks[it], dict)):
                            if('cooldown' in attacks[it]):
                                output.append(str(attacks[it]['cooldown']))
                if(checkValue(id, 'morale')):
                    output.append("\n|morale="+str(getValue(id, 'morale')))
                if(checkValue(id, 'default_faction')):
                    output.append("\n|default_faction="+getValue(id, 'default_faction'))
                if(checkValue(id, 'death_function')):
                    death = getValue(id, 'death_function')
                    output.append("\n|ondeath=")
                    for it in range(0, len(death)):
                        if (it > 0):
                            output.append(", ")
                        output.append(death[it])
                if(checkValue(id, 'reproduction')): #Add reproduction data.
                    reproduction = getValue(id, 'reproduction')
                    if('baby_monster' in reproduction):
                        output.append("\n|reproductionID=")
                        output.append(reproduction['baby_monster'])
                        output.append("\n|reproductionName=")
                        output.append(ID_To_String(reproduction['baby_monster']))
                    if('baby_egg' in reproduction):
                        output.append("\n|reproductionEggID=")
                        output.append(reproduction['baby_egg'])
                        output.append("\n|reproductionEggName=")
                        output.append(getEggName(reproduction['baby_egg']))
                    if('baby_count' in reproduction):
                        output.append("\n|reproductionCount=")
                        output.append(str(reproduction['baby_count']))
                    if('baby_timer' in reproduction):
                        output.append("\n|reproductionTimer=")
                        output.append(str(reproduction['baby_timer']))
                if(checkValue(id, 'description')):
                    output.append("\n|description="+getValue(id, 'description'))

        output.append("""\n}}<noinclude>
==Notes==
<!-- *YOUR PERSONAL NOTES AND HINTS GO BELOW HERE* -->

{{Enemies}}
"""+species_categories(getValue(id, 'species'))+version+"""</noinclude>""")


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
            print ID_To_Mon_Int(var)
            var = raw_input(">")
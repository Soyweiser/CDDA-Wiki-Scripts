import json
import sys
from version import version
from name_hacks import monster_name
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#Data is copied to clipboard, used for the Monsters
## accepts a mon_id value like mon_zombie, which returns the monster ID number, or a int which prints that the monster data of that number, or '_idtotal' which shows the total number of monsters.

list_monster_files = [ 'data/json/monsters.json', 'data/json/monsters/bird.json', 'data/json/monsters/defense_bot.json', 'data/json/monsters/drones.json', 'data/json/monsters/fish.json', 'data/json/monsters/insect_spider.json', 'data/json/monsters/mammal.json', 'data/json/monsters/military.json', 'data/json/monsters/reptile_amphibian.json', 'data/json/monsters/triffid.json', 'data/json/monsters/zed_children.json', 'data/json/monsters/zed_explosive.json' ]

list_item_files = [ 'data/json/items/biosignatures.json', 'data/json/items/comestibles/egg.json' ]

#Copied from navbox_enemies.py, used to add additional categories to monster pages.
monster_group_list = [ 'Domesticated Animals', 'Forest Animals', 'River animals', 'Wild Mutants', 'Insectoids', 'Giant worms', 'Zombies', 'Zombie Animals', 'Plants', 'Fungi', 'Blobs', 'Underground dwellers', 'Swamp creatures', 'Spiders', 'Unearthed horrors', 'Netherworld inhabitants', 'Cult', 'Robots', 'Hallucinations', 'Joke Monsters', 'Other', 'ignored' ]

monster_cat_list_file = "wiki_data/monsters_list.json"

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
    name_hack = monster_name(id)
    if( not name_hack == id):
        return name_hack
    else:
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

## Normal items
for it in range(0, len(list_item_files)):
    with open(list_item_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (data, new_data)
        data = merge_json_data(data, new_data)
itemData = setAbstractIds(data)
data = list()

def getItemName(id):
    for it in range(0, len(itemData)):
        if(itemData[it]['id'] == id):
            if('name'in itemData[it]):
                return itemData[it]['name']
            else:
                return "Item " + itemData[it]['id'] + "doesn't have name set"

## Species
with open('data/json/species.json') as data_file:
    species = json.load(data_file)

def species_tostring (id):
    for it in range(0, len(species)):
        if(species[it]['id'] == id):
            return species[it]['name']
    return "species not found"

def species_categories (species_list, id): #species_list is a list of species, prints a list of categories
    retval = ""
    species_list_strings = []
    for it in range(0, len(species_list)):
        species_list_strings.append(species_tostring(species_list[it]))
    #now use the 'wiki_data\monster_list.json' file to set any additional categories.
    for ite in range(0, len(monster_cat_list)):
        if(monster_cat_list[ite]['id'] == id):
            if(not monster_group_list[monster_cat_list[ite]['cat']].lower() in species_list_strings):
                species_list_strings.append(monster_group_list[monster_cat_list[ite]['cat']])
    for it in range(0, len(species_list_strings)):
        retval += "[[Category:"+species_list_strings[it]+"]]\n"
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

#monster_list.json (copied from navbox_enemies.py)
with open(monster_cat_list_file) as data_file:
    monster_cat_list = json.load(data_file)
#now check if there are missing monster id's
for ite in range(0, len(data)):
    exists = False
    for it in range(0, len(monster_cat_list)):
        if(monster_cat_list[it]['id'] == data[ite]['id']):
            exists = True
    if(not exists):
        print "monster ID " + data[ite]['id'] + " missing from monster_list.json"

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
                output.append( """<!-- Automatically generated by https://github.com/Soyweiser/CDDA-Wiki-Scripts The monsters.py script. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page.
--><noinclude>{{enemydescription</noinclude>
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
                if(checkValue(id, 'path_settings')): #most of these path settings values are not used yet ingame by any monsters. Added for completion.
                    path = getValue(id, 'path_settings')
                    output.append("\n<!--path settings-->")
                    if('max_dist' in path):
                        output.append("\n|max_dist=")
                        output.append(str(path['max_dist']))
                    if('max_length' in path):
                        output.append("\n|max_length=")
                        output.append(str(path['max_length']))
                    if('bash_strength' in path):
                        output.append("\n|bash_strength=")
                        output.append(str(path['bash_strength']))
                    if('allow_open_doors' in path):
                        output.append("\n|allow_open_doors=")
                        output.append(str(path['allow_open_doors']))
                    if('avoid_traps' in path):
                        output.append("\n|avoid_traps=")
                        output.append(str(path['avoid_traps']))
                    if('allow_climb_stairs' in path):
                        output.append("\n|allow_climb_stairs=")
                        output.append(str(path['allow_climb_stairs']))
                    output.append("\n<!--end of path settings-->")
                if(checkValue(id, 'anger_triggers')):
                    triggers = getValue(id, 'anger_triggers')
                    for it in range(0, len(triggers)):
                        output.append("\n|anger"+str(it+1)+"=")
                        output.append(triggers[it])
                if(checkValue(id, 'fear_triggers')):
                    triggers = getValue(id, 'fear_triggers')
                    for it in range(0, len(triggers)):
                        output.append("\n|fear"+str(it+1)+"=")
                        output.append(triggers[it])
                if(checkValue(id, 'placate_triggers')):
                    triggers = getValue(id, 'placate_triggers')
                    for it in range(0, len(triggers)):
                        output.append("\n|placate"+str(it+1)+"=")
                        output.append(triggers[it])
                if(checkValue(id, 'death_function')):
                    death = getValue(id, 'death_function')
                    output.append("\n|ondeath=")
                    for it in range(0, len(death)):
                        if (it > 0):
                            output.append(", ")
                        output.append(death[it])
                if(checkValue(id, 'harvest')): #Harvest data is the name of a special sort of droplist see: data/json/harvest.json. Use harvest.py (which doesn't exist yet) to populate these wiki pages.
                    output.append("\n|harvest=")
                    output.append(getValue(id,'harvest'))
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
                        output.append(getItemName(reproduction['baby_egg']))
                    if('baby_count' in reproduction):
                        output.append("\n|reproductionCount=")
                        output.append(str(reproduction['baby_count']))
                    if('baby_timer' in reproduction):
                        output.append("\n|reproductionTimer=")
                        output.append(str(reproduction['baby_timer']))
                if(checkValue(id, 'baby_flags')):
                    babyf = getValue(id, 'baby_flags')
                    output.append("\n|baby_flag=")
                    for it in range(0, len(babyf)):
                        if (it >0):
                            output.append(", ")
                        output.append(str(babyf[it]).lower())
                if(checkValue(id, 'biosignature')): #Add poop data.
                    waste = getValue(id, 'biosignature')
                    if('biosig_item' in waste):
                        output.append("\n|biosig_item=")
                        output.append(getItemName(waste['biosig_item']))
                    if('biosig_timer' in waste):
                        output.append("\n|biosig_timer=")
                        output.append(str(waste['biosig_timer']))
                if(checkValue(id, 'vision_day')):
                    output.append("\n|vision_day=")
                    output.append(str(getValue(id,'vision_day')))
                if(checkValue(id, 'vision_night')):
                    output.append("\n|vision_night=")
                    output.append(str(getValue(id,'vision_night')))
                if(checkValue(id, 'special_when_hit')): #Some monsters have special effects when hit.
                    output.append("\n|special_when_hit=")
                    output.append(getValue(id,'special_when_hit')[0])
                    output.append("\n|special_when_hit_chance=")
                    output.append(str(getValue(id,'special_when_hit')[1]))
                if(checkValue(id, 'burn_into')): #Monsters can be burned into other monsters
                    output.append("\n|BurnID=")
                    output.append(getValue(id,'burn_into'))
                    output.append("\n|BurnName=")
                    output.append(ID_To_String(getValue(id,'burn_into')))
                if(checkValue(id, 'upgrades')): #Monsters evolution
                    if('into' in getValue(id,'upgrades')):
                        output.append("\n|upgrade=")
                        output.append(ID_To_String(getValue(id,'upgrades')['into']))
                    elif('into_group' in getValue(id,'upgrades')):
                        output.append("\n|upgrade_group=")
                        output.append(getValue(id,'upgrades')['into_group'])
                    if('half_life' in getValue(id,'upgrades')):
                        output.append("\n|upgrade_half_life=")
                        output.append(str(getValue(id,'upgrades')['half_life']))
                    elif('age_grow' in getValue(id,'upgrades')):
                        output.append("\n|upgrade_time=")
                        output.append(str(getValue(id,'upgrades')['age_grow']))
                if(checkValue(id, 'description')):
                    output.append("\n|description="+getValue(id, 'description'))
        output.append("""\n}}<noinclude>
<div style="margin: 1em; border: 1px solid #aaa; background-color: #white; padding: 5px;">
<h2><span class="plainlinks" style="float: right; font-size: small">
([[{{lc:{{PAGENAME}}}}/doc|<span title="View user added notes">View</span>]] - [{{fullurl:{{lc:{{PAGENAME}}}}/doc|action=edit}} <span title="Edit user notes">Edit Notes</span>] )</span>Notes</h2>
<!-- 

*YOUR PERSONAL NOTES AND HINTS SHOULD GO IN THE """ + ID_To_String(data[var]['id']).split('|',1)[0] +"""/doc PAGE DO NOT EDIT HERE*

-->
{{#ifexist:{{lc:{{PAGENAME}}}}/doc| {{:{{lc:{{PAGENAME}}}}/doc}} |}}<!-- list the doc page if it exists-->
<span class="plainlinks" style="font-size: small"><center>( [{{fullurl:{{lc:{{PAGENAME}}}}/doc|action=edit}} <span title="Edit user notes">Edit Notes</span>] )</center></span>
</div>
{{Enemies}}
"""+species_categories(getValue(id, 'species'), getValue(id, 'id'))+version + "</noinclude>")
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
        if ( var == '_idtotal' ): #prints the max number of monsters
            print len(data)
            var = raw_input(">")
        else:
            print ID_To_Mon_Int(var)
            var = raw_input(">")
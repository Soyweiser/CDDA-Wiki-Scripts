import json
import sys
import string
from version import version
from name_hacks import monster_name
import pywikibot

#Documentation
#data is uploaded automatically, used for the Template:Navbox/enemies page, and the various Template:Enemiestable lists.
#Uses wiki_data/monsters_list.json, the script will mention missing monsterids from the list. (the json is a list of 'id's and 'cat's matched.
#Usage: python [location of pywikibotinstall]\pwb.py navbox_enemies.py
#   Then input your password, and wait for the page to be updated.
#script will warn you about missing ID's, the missing base_drone is normal.


list_monster_files = [ 'data/json/monsters.json', 'data/json/monsters/bird.json', 'data/json/monsters/defense_bot.json', 'data/json/monsters/drones.json', 'data/json/monsters/fish.json', 'data/json/monsters/insect_spider.json', 'data/json/monsters/mammal.json', 'data/json/monsters/military.json', 'data/json/monsters/reptile_amphibian.json', 'data/json/monsters/triffid.json', 'data/json/monsters/zed_children.json', 'data/json/monsters/zed_explosive.json' ]

monster_group_list = [ 'Domesticated Animals', 'Forest Animals', 'River animals', 'Wild Mutants', 'Insectoids', 'Giant worms', 'Zombies', 'Zombie Animals', 'Plants', 'Fungi', 'Blobs', 'Underground dwellers', 'Swamp creatures', 'Spiders', 'Unearthed horrors', 'Netherworld inhabitants', 'Cult', 'Robots', 'Hallucinations', 'Crazy Cataclysm', 'Other', 'ignored' ]

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

def capitalize(s):
   if len(s) == 0:
      return s
   else:
      return s[0].upper() + s[1:]

master_mon_list = []
for iterator in range(0, len(data)):
    if( not "abstract" in data[iterator]):
        master_mon_list.append(data[iterator]["id"])

for it in range(0, len(list_monster_files)):
    with open(list_monster_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (data, new_data)
        data = merge_json_data(data, new_data)
data = setAbstractIds(data)
ID_monster = fill_ID_List(data)

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

output = []
output.append("""{{Navbox
|name       = Enemies
|title      = [[Enemies]]
|state      = uncollapsed

|bodystyle = background:#fdfdfd; width:100%; vertical-align:middle; border-color: #CCAAAA;
|titlestyle = background:#CCAAAA; color:#ffffff; padding-left:1em; padding-right:1em; text-align:center;
|groupstyle = background:#CCAAAA; color:#ffffff; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold;
""")

for it in range(0, len(monster_group_list)):
    if( it+1 == len(monster_group_list)):
        break #don't print the ignored list.
    output.append("|group" + str(it+1) + " = [[")
    output.append(monster_group_list[it])
    output.append("]]\n|list" + str(it+1) + " =\n")
    monsters_list = []
    for ite in range(0, len(monster_cat_list)):
        if(monster_cat_list[ite]['cat'] == it):
            if (monster_cat_list[ite]['id'] != monster_name(monster_cat_list[ite]['id']) and not monster_name(monster_cat_list[ite]['id']) in monsters_list):
                monsters_list.append(monster_name(monster_cat_list[ite]['id']))
            elif (not ID_To_String(monster_cat_list[ite]['id']) in monsters_list):
                monsters_list.append(ID_To_String(monster_cat_list[ite]['id']))
    monsters_list = sorted(monsters_list, key=lambda s: s.lower())
    for ite in range(0, len(monsters_list)):
        output.append('''<!--
  -->''')
        if ( ite > 0):
            output.append("{{md}}")
        output.append("[[" + capitalize(monsters_list[ite]) + "]]")
    output.append('''<!--
  -->

''')

output.append("""\n}}<noinclude>
Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts The navbox_enemies.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.\n\n
Navbox template that shows all enemies in some arbitrary categories.\n
[[Category:Navigational templates]]
"""+version+"</noinclude>")

text = "".join(output)
text.replace("\n", "\\n")

site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:Navbox/enemies')
page.text = text
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts navbox_enemies.py script')

header = "{{header/Enemies1}}\n"
footer = '''</table><noinclude>
Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts The navbox_enemies.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.\n'''+version+"\n</noinclude>"
for it in range(0, len(monster_group_list)):
    output = []
    output.append(header)
    if( it+1 == len(monster_group_list)):
        break #don't print the ignored list.
    pagename = "Template:Enemiestable/" + monster_group_list[it]
    monsters_list = []
    for ite in range(0, len(monster_cat_list)):
        if(monster_cat_list[ite]['cat'] == it):
            if (monster_cat_list[ite]['id'] != monster_name(monster_cat_list[ite]['id']) and not monster_cat_list[ite]['id'] in monsters_list):
                monsters_list.append(monster_name(monster_cat_list[ite]['id']))
            elif (not ID_To_String(monster_cat_list[ite]['id']) in monsters_list):
                monsters_list.append(ID_To_String(monster_cat_list[ite]['id']))
    monsters_list = sorted(monsters_list, key=lambda s: s.lower())
    for ite in range(0, len(monsters_list)):
        output.append("{{:" + capitalize(monsters_list[ite]) + "}}\n")
    output.append(footer)
    text = "".join(output)
    text.replace("\n", "\\n")
    page = pywikibot.Page(site, pagename)
    page.text = text
    page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts navbox_enemies.py script')

exit()

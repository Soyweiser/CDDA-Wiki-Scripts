import json
import sys
import copy
import string
import math
import pywikibot

#documentation
#Usage: python [location of pywikibotinstall]\pwb.py foragingList.py
#   Then input your password, and wait for the page to be updated.

list_item_files = [ 'data/json/items/comestibles.json', 'data/json/items/comestibles/brewing.json', 'data/json/items/comestibles/carnivore.json', 'data/json/items/comestibles/drink.json', 'data/json/items/comestibles/med.json', 'data/json/items/comestibles/mutagen.json', 'data/json/items/comestibles/protein.json', 'data/json/items/comestibles/seed.json', 'data/json/items/comestibles/spice.json', 'data/json/items/classes/comestible.json', 'data/core/basic.json', 'data/json/items/melee.json', 'data/json/items/generic.json', 'data/json/items/chemicals_and_resources.json', 'data/json/items/newspaper.json', 'data/json/items/containers.json', 'data/json/items/tools.json', 'data/json/items/generic/string.json', 'data/json/items/resources/metals.json' ]
list_itemgroup_files = [ 'data/json/item_groups.json', 'data/json/itemgroups/forage.json' ]
data = list()
itemgroup_data = list()

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
                        print "duplicate ID detected "
                        print id
                        print ".\n"

def setAbstractIds(): #some items have no ID value set, which this code depends on, but they do have an abstract. This function copies the abstract value into the id value.
    for it in range(0, len(data)):
        if(not 'id' in data[it]):
            if('abstract' in data[it]):
                data[it]['id'] = data[it]['abstract']
            else:
                print 'both no id and no abstract detected '
                print it
                print '.\n'

ID_to_item = dict()
def ID_To_Item_Int(id): #should return the location of the item inside the items list. Input, string containing the item Id, returns, int location in the data list.
    if(id in ID_to_item):
        return ID_to_item[id]["id_nr"]
    else:
        return -1

def fill_ID_to_item ():
    for it in range(0, len(data)):
        keyD = dict()
        keyD['id_nr'] = it
        keyD["name"] = data[it]["name"]
        if ('id' in data[it]):
            ID_to_item[data[it]["id"]] = keyD

def getValue(id, value): #returns the value field of the item. It is a recursive function that takes into account the abstract item.
    if(value in data[id]):
        return data[id][value]
    else:
        if('copy-from' in data[id]):
            return getValue(ID_To_Item_Int(data[id]["copy-from"]), value)
        else:
            return 'error:no such value field, in getValue'

def checkValue(id, value): #returns if the value field is defined in the item description. Or if it is defined in on of the abstracts.
    if(value in data[id]):
        return True
    if("copy-from" in data[id]):
        return checkValue(ID_To_Item_Int(data[id]["copy-from"]), value)
    else:
        return False

def getValueOrZero(id, value):
    if(checkValue(id, value)):
        return getValue(id, value)
    else:
        return 0

def getValueRecursive(id, value): # gets values taking proportional and relatives values into account. Only use on ints, returns zero if not set.
    retval = 0
    if(value in data[id]): # proportional and relative values don't matter if this value is set.
        return data[id][value]
    if(checkValue(id, 'copy-from')):
        retval = getValueRecursive(ID_To_Item_Int(data[id]["copy-from"]),value)
    if("relative" in data[id]):
        if(value in data[id]['relative']):
            retval += data[id]['relative'][value]
            retval = int(retval)
    if('proportional' in data[id]):
        if(value in data[id]['proportional']):
            retval *= data[id]['proportional'][value]
            retval = int(retval)
    return retval

kcal_per_nutr = 2500.0 / ( 12 * 24 ) #from itype.h
def getNutrition(id):
    if(checkValue(id, 'nutrition')):
        return getValue(id,'nutrition')
    elif(checkValue(id, 'calories')):
        retval = getValueRecursive(id, 'calories') / kcal_per_nutr
        retval = int(retval)
        return retval
    return 0

def getMaterialsString(id): #Returns a list of strings. Because that is why my code uses.
    retval = [ "" ]
    if (checkValue(id,'material')):
        if (isinstance(getValue(id,'material'), list)):
            materialList = sorted(getValue(id,'material'), key=string.lower)
            for ite in range(0, len(materialList)):
                if(ite > 0):
                    retval.append(", ")
                retval.append("{{Materialtoname|")
                retval.append(str(materialList[ite]))
                retval.append("}}")
        else:
            retval.append("{{Materialtoname|")
            retval.append(str(getValue(id,'material')))
            retval.append("}}")
    else:
        retval.append("none")
    return retval

def getUseFunctionString(id): #Returns a list of strings. Because that is why my code uses.
#Healing items are just listed as 'healing item' (see item). (as they have a pretty big list of results, and not all that interesting, and these results are visible ingame).
#Drugs have their various effects listed, which in contrast to the healing items, vary wildly, and cannot be seen ingame.
#Double check if all the options are properly listed in 'Template:Usefunctiontotext'. Please add any missing ones.
    retval = [ "" ]
    if(checkValue(id,'use_action')): #usefunction (add any missing options to 'Template:Row/Food'
        useaction = getValue(id,'use_action')
        if (isinstance(useaction, dict)):
            if('type' in useaction):
                if(useaction['type'] == 'heal'):
                    retval.append("Healing item (see item)")
                elif(useaction['type'] == 'consume_drug'):
                    if('effects' in useaction):
                        for it in range(0, len(useaction['effects'])):
                            if(it > 0):
                                retval.append(", ")
                            retval.append("{{Usefunctiontotext|")
                            retval.append(str(useaction['effects'][it]['id']))
                            retval.append("}}")
                else:
                    retval.append("See Item")
            else:
                retval.append("See Item")
        else:
            retval.append(str(useaction))
    else:
        retval.append("none")
    return retval

def InItemgroupData (group_id): #returns if the this id string is a valid id for an itemgroup.
    for it in range(0, len(itemgroup_data)):
        if(itemgroup_data[it]['id'] == group_id):
            return True
    return False

def GetItemGroupData (group_id): #returns the itemgroup for the id string. returns False if not found.
    for it in range(0, len(itemgroup_data)):
        if(itemgroup_data[it]['id'] == group_id):
            return itemgroup_data[it]
    return False

for it in range(0, len(list_item_files)):
    with open(list_item_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (data, new_data)
        data = merge_json_data(data, new_data)
setAbstractIds()
fill_ID_to_item()

for it in range(0, len(list_itemgroup_files)):
    with open(list_itemgroup_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (itemgroup_data, new_data)
        itemgroup_data = merge_json_data(itemgroup_data, new_data)

ID_masterlist = list()
for it in range(0, len(data)):
    ID_masterlist.append(data[it]["id"])
ID_masterlist = sorted(ID_masterlist, key=string.lower)

def itemgroupRow(item_id, group_entry, prob):
    retval = [ "" ]
    id = ID_To_Item_Int(item_id)
    retval.append("{{row/ItemGroup|name=")
    retval.append(str(getValue(id, 'name')))
    retval.append("|color=")
    retval.append(str(getValue(id, 'color')))
    retval.append("|symbol=")
    retval.append(str(getValue(id, 'symbol')))
    retval.append("|id=")
    retval.append(item_id)
    retval.append("|prob=")
    retval.append(str(prob))
    if('count-min' in group_entry):
        retval.append("|min=")
        retval.append(str(group_entry['count-min']))
    if('count-max' in group_entry):
        retval.append("|max=")
        retval.append(str(group_entry['count-max']))
    retval.append("}}\n")
    return retval

def itemgroupToList(id_name, max_prob = 0.0): #id_name should be the name of the itemgroup id.
#Recursive function to easily make long lists of all possible drops.
    retval = [ "" ]
    entries_are_groups = False
    probs = 0.0
    for it in range(0, len(itemgroup_data)):
        if(itemgroup_data[it]['id'] == id_name):
            retval.append("<!--Start of group: ")
            retval.append(itemgroup_data[it]['id'])
            retval.append(" \n-->")
            itemgroup = itemgroup_data[it]
            subtype = 'old' #if substype is not set, it defaults to the 'old' subtype, which according to ITEM_SPAWN.md is the same as 'Distribution'
            if('subtype' in itemgroup):
                if(itemgroup['subtype'] == 'distribution'):
                    subtype = 'distribution'
                elif(itemgroup['subtype'] == 'collection'):
                    subtype = 'collection'

            if('entries' in itemgroup): #the list of items/item_groups that can drop can be called items or entries.
                entries = itemgroup['entries']
            elif('items' in itemgroup):
                entries = itemgroup['items']
            elif('groups' in itemgroup):
                entries = itemgroup['groups']
                entries_are_groups = True

            if(subtype == 'old' or subtype == 'distribution'):#if the subtype is the distribution, calculate the total amount of probablities.
                for ite in range(0, len(entries)):
                    if('prob' in entries[ite]):
                        max_prob += entries[ite]['prob']
                    elif(type(entries[ite]) is list):
                        max_prob += entries[ite][1]
                    else: #items without a prob listed have a default of 100
                        max_prob += 100.0
            
            for ite in range(0, len(entries)):
                #calculate prob for this entry.
                if('prob' in entries[ite]):
                    prob = entries[ite]['prob']
                elif(type(entries[ite]) is list):
                    prob = entries[ite][1]
                else: #items without a prob listed have a default of 100
                    prob = 100.0
                if(subtype == 'old' or subtype == 'distribution'):
                    prob = int(math.ceil((prob / max_prob)*10000.0))/100.0

                #print entry
                if(entries_are_groups):
                    id = 'error in group entry'
                    if(type(entries[ite]) is list):
                        if(InItemgroupData(entries[ite][0])):
                            id = entries[ite][0]
                    elif('item' in entries[ite]):
                        if(InItemgroupData(entries[ite]['item'])):
                            id = entries[ite]['item'][0]
                    else:
                        if(InItemgroupData(entries[ite]['item'])):
                            id = entries[ite]['item']
                    retval.extend(itemgroupToList(id, prob))
                else:
                    if(type(entries[ite]) is list):
                        if(ID_To_Item_Int(entries[ite][0]) == -1):
                            retval.append("missing ")
                        retval.extend(itemgroupRow(entries[ite][0], entries[ite], prob))
                    elif('item' in entries[ite]):
                        retval.extend(itemgroupRow(entries[ite]['item'], entries[ite], prob))
                    elif('group' in entries[ite]):
                        if(InItemgroupData(entries[ite]['group'])):
                            retval.extend(itemgroupToList(entries[ite]['group'], prob))
                        else:
                            retval.append("List not found")
                    else:
                        retval.append(str(entries[ite]))
                probs += prob
            retval.append("<!-- End of group -->")
    return retval

header = '''<!--Automatically generated using https://github.com/Soyweiser/CDDA-Wiki-Scripts foragingList.py -->\n\n'''
footer = '''</table>
<noinclude>Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts The foragingList.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.\n[[Category:Templates]]\n</noinclude>\n'''

springText = [ "" ]
springText.append("{{header/ItemGroup}}\n")
springText.append(header)
springText.extend(itemgroupToList('forage_spring'))
springText.append(footer)
springText = "".join(springText)
springText.replace("\n", "\\n")

summerText = [ "" ]
summerText.append("{{header/ItemGroup}}\n")
summerText.append(header)
summerText.extend(itemgroupToList('forage_summer'))
summerText.append(footer)
summerText = "".join(summerText)
summerText.replace("\n", "\\n")

autumnText = [ "" ]
autumnText.append("{{header/ItemGroup}}\n")
autumnText.append(header)
autumnText.extend(itemgroupToList('forage_autumn'))
autumnText.append(footer)
autumnText = "".join(autumnText)
autumnText.replace("\n", "\\n")

winterText = [ "" ]
winterText.append("{{header/ItemGroup}}\n")
winterText.append(header)
winterText.extend(itemgroupToList('forage_winter'))
winterText.append(footer)
winterText = "".join(winterText)
winterText.replace("\n", "\\n")

trashText = [ "" ]
trashText.append("{{header/ItemGroup}}\n")
trashText.append(header)
trashText.extend(itemgroupToList('trash_forest'))
trashText.append(footer)
trashText = "".join(trashText)
trashText.replace("\n", "\\n")


site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:ItemGroup/forage_spring')
page.text = springText
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts foragingList.py script')
page = pywikibot.Page(site, 'Template:ItemGroup/forage_summer')
page.text = summerText
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts foragingList.py script')
page = pywikibot.Page(site, 'Template:ItemGroup/forage_autumn')
page.text = autumnText
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts foragingList.py script')
page = pywikibot.Page(site, 'Template:ItemGroup/forage_winter')
page.text = winterText
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts foragingList.py script')
page = pywikibot.Page(site, 'Template:ItemGroup/trash_forest')
page.text = trashText
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts foragingList.py script')

exit()
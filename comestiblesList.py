import json
import sys
import copy
import string
import math
import pywikibot
from version import version

#documentation
#Usage: python [location of pywikibotinstall]\pwb.py comestiblesList.py
#   Then input your password, and wait for the page to be updated.

list_comestibles_files = [ 'data/json/items/comestibles.json', 'data/json/items/comestibles/brewing.json', 'data/json/items/comestibles/carnivore.json', 'data/json/items/comestibles/drink.json', 'data/json/items/comestibles/med.json', 'data/json/items/comestibles/mutagen.json', 'data/json/items/comestibles/protein.json', 'data/json/items/comestibles/seed.json', 'data/json/items/comestibles/spice.json', 'data/json/items/classes/comestible.json', 'data/core/basic.json' ]
data = list()

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

for it in range(0, len(list_comestibles_files)):
    with open(list_comestibles_files[it]) as data_file:
        new_data = json.load(data_file)
        check_duplicates (data, new_data)
        data = merge_json_data(data, new_data)
setAbstractIds()
fill_ID_to_item()

ID_masterlist = list()
for it in range(0, len(data)):
    ID_masterlist.append(data[it]["id"])
ID_masterlist = sorted(ID_masterlist, key=string.lower)

ID_comes = list()
for it in range(0, len(data)):
    if(getValue(it,'comestible_type')):
        if ('FOOD' == getValue(it,'comestible_type')):
            ID_comes.append(data[it]["id"])
ID_comes = sorted(ID_comes, key=string.lower)

ID_drinks = list()
for it in range(0, len(data)):
    if(getValue(it, 'comestible_type')):
        if ('DRINK' == getValue(it, 'comestible_type')):
            ID_drinks.append(data[it]["id"])
ID_drinks = sorted(ID_drinks, key=string.lower)

ID_meds = list()
for it in range(0, len(data)):
    if(getValue(it, 'comestible_type')):
        if ('MED' == getValue(it, 'comestible_type')):
            ID_meds.append(data[it]["id"])
ID_meds = sorted(ID_meds, key=string.lower)

ID_mutagen = list()
for it in range(0, len(data)):
    if(getValue(it, 'use_action')):
        if ('MUTAGEN' == getValue(it, 'use_action')):
            ID_mutagen.append(data[it]["id"])
        elif ('MUT_IV' == getValue(it, 'use_action')):
            ID_mutagen.append(data[it]["id"])
        elif ('PURIFY_IV' == getValue(it, 'use_action')):
            ID_mutagen.append(data[it]["id"])
        elif ('PURIFIER' == getValue(it, 'use_action')):
            ID_mutagen.append(data[it]["id"])
ID_mutagen = sorted(ID_mutagen, key=string.lower)

header = '''<!--Automatically generated using https://github.com/Soyweiser/CDDA-Wiki-Scripts ComestiblesList.py -->\n\n'''
footer = '''</table>
<noinclude>Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts The ComestiblesList.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.\n[[Category:Templates]]\n'''
footer+=version+"</noinclude>\n"

##Food list
output = [ "" ]
output.append("{{header/Comestibles|food}}\n")
output.append(header)
#'{{row/Food'|name|price|color|item materials|container|volume|weight|quench|nutrition|spoils|stimulant|health|addiction|charges|fun|usefunction|addiction_function|description|weight/volume|parasites'}}'
for it in range(0, len(ID_comes)):
    id = ID_To_Item_Int(ID_comes[it])
    if(not 'abstract' in data[id]): #don't print abstract items.
        output.append("<!--"+ID_comes[it]+"-->")
        output.append("{{row/Food|")
        output.append(getValue(id,'name'))
        output.append("|")
        output.append(str(getValueRecursive(id,'price')))
        output.append("|")
        output.append(getValue(id,'color'))
        output.append("|")
        output.extend(getMaterialsString(id))
        output.append("|")
        if(checkValue(id,'container')): #containers
            output.append(str(getValue(id,'container')))
        else:
            output.append("itm_null")
        output.append("|")
        output.append(str(getValueRecursive(id,'volume')))
        output.append("|")
        output.append(str(getValueRecursive(id,'weight')))
        output.append("|")
        output.append(str(getValueRecursive(id,'quench')))
        output.append("|")
        output.append(str(getNutrition(id))) #due to calories and nutrition being used, this is a special case.
        output.append("|")
        output.append(str(getValueOrZero(id,'spoils_in')))
        output.append("|")
        output.append(str(getValueOrZero(id,'stim')))
        output.append("|")
        output.append(str(getValueOrZero(id,'healthy')))
        output.append("|")
        output.append(str(getValueOrZero(id,'addiction_potential')))
        output.append("|")
        charges = getValueOrZero(id,'charges')
        if(charges == 0):
            charges = 1
        output.append(str(charges))
        output.append("|")
        output.append(str(getValueRecursive(id,'fun')))
        output.append("|")
        output.extend(getUseFunctionString(id))
        output.append("|")
        if(checkValue(id,'addiction_type')):
            output.append(str(getValue(id,'addiction_type')))
        else:
            output.append("ADD_NULL")
        output.append("|")
        output.append(str(getValue(id,'description')))
        output.append("|")
        if( not getValueOrZero(id, 'weight') == 0 ):
            output.append(str(math.ceil(float(getValueOrZero(id, 'nutrition') / float(getValueOrZero(id, 'weight')))*100)/100))
        else:
            output.append("!")
        output.append("|")
        output.append(str(getValueRecursive(id,'parasites')))
        if(checkValue(id,'price_postapoc')):
            output.append("|trade_price=")
            output.append(str(getValueRecursive(id,'price_postapoc')))
        output.append("}}\n")
output.append(footer)

Foodtext = "".join(output)
Foodtext.replace("\n", "\\n")
#print Foodtext

##Drinks list
output = [ "" ]
output.append("{{header/Comestibles|drinks}}\n")
output.append(header)
#'{{row/drinks'|name|price|color|material|container|quench|nutrition|spoils|stimulant|health|addiction|charges|fun|usefunction|addiction_function|description'}}'
for it in range(0, len(ID_drinks)):
    id = ID_To_Item_Int(ID_drinks[it])
    if(not 'abstract' in data[id]): #don't print abstract items.
        output.append("<!--"+ID_drinks[it]+"-->")
        output.append("{{row/Drinks|")
        output.append(getValue(id,'name'))
        output.append("|")
        output.append(str(getValueRecursive(id,'price')))
        output.append("|")
        output.append(getValue(id,'color'))
        output.append("|")
        output.extend(getMaterialsString(id))
        output.append("|")
        if(checkValue(id,'container')): #containers
            output.append(str(getValue(id,'container')))
        else:
            output.append("itm_null")
        output.append("|")
        output.append(str(getValueRecursive(id,'quench')))
        output.append("|")
        output.append(str(getNutrition(id))) #due to calories and nutrition being used, this is a special case.
        output.append("|")
        output.append(str(getValueOrZero(id,'spoils_in')))
        output.append("|")
        output.append(str(getValueOrZero(id,'stim')))
        output.append("|")
        output.append(str(getValueOrZero(id,'healthy')))
        output.append("|")
        output.append(str(getValueOrZero(id,'addiction_potential')))
        output.append("|")
        charges = getValueOrZero(id,'charges')
        if(charges == 0):
            charges = 1
        output.append(str(charges))
        output.append("|")
        output.append(str(getValueRecursive(id,'fun')))
        output.append("|")
        output.extend(getUseFunctionString(id))
        output.append("|")
        if(checkValue(id,'addiction_type')):
            output.append(str(getValue(id,'addiction_type')))
        else:
            output.append("ADD_NULL")
        output.append("|")
        output.append(str(getValue(id,'description')))
        if(checkValue(id,'price_postapoc')):
            output.append("|trade_price=")
            output.append(str(getValueRecursive(id,'price_postapoc')))
        output.append("}}\n")
output.append(footer)

Drinktext = "".join(output)
Drinktext.replace("\n", "\\n")

##Meds list
output = [ "" ]
output.append("{{header/Comestibles|meds}}\n")
output.append(header)
#'{{row/meds'|name|price|color|container|material|stimulant|health|addiction|charges|fun|usefunction|addiction_function|description'}}'
for it in range(0, len(ID_meds)):
    id = ID_To_Item_Int(ID_meds[it])
    if(not 'abstract' in data[id]): #don't print abstract items.
        output.append("<!--"+ID_meds[it]+"-->")
        output.append("{{row/Meds|")
        output.append(getValue(id,'name'))
        output.append("|")
        output.append(str(getValueRecursive(id,'price')))
        output.append("|")
        output.append(getValue(id,'color'))
        output.append("|")
        if(checkValue(id,'container')): #containers
            output.append(str(getValue(id,'container')))
        else:
            output.append("itm_null")
        output.append("|")
        output.extend(getMaterialsString(id))
        output.append("|")
        output.append(str(getValueOrZero(id,'stim')))
        output.append("|")
        output.append(str(getValueOrZero(id,'healthy')))
        output.append("|")
        output.append(str(getValueOrZero(id,'addiction_potential')))
        output.append("|")
        charges = getValueOrZero(id,'charges')
        if(charges == 0):
            charges = 1
        output.append(str(charges))
        output.append("|")
        output.append(str(getValueRecursive(id,'fun')))
        output.append("|")
        output.extend(getUseFunctionString(id))
        output.append("|")
        if(checkValue(id,'addiction_type')):
            output.append(str(getValue(id,'addiction_type')))
        else:
            output.append("ADD_NULL")
        output.append("|")
        output.append(str(getValue(id,'description')))
        if(checkValue(id,'price_postapoc')):
            output.append("|trade_price=")
            output.append(str(getValueRecursive(id,'price_postapoc')))
        output.append("}}\n")
output.append(footer)

Medstext = "".join(output)
Medstext.replace("\n", "\\n")

##Mutagen list
output = [ "" ]
output.append("{{header/Comestibles|food}}\n")
output.append(header)
#'{{row/Food'|name|price|color|item materials|container|volume|weight|quench|nutrition|spoils|stimulant|health|addiction|charges|fun|usefunction|addiction_function|description|weight/volume|parasites'}}'
for it in range(0, len(ID_mutagen)):
    id = ID_To_Item_Int(ID_mutagen[it])
    if(not 'abstract' in data[id]): #don't print abstract items.
        output.append("<!--"+ID_mutagen[it]+"-->")
        output.append("{{row/Food|")
        output.append(getValue(id,'name'))
        output.append("|")
        output.append(str(getValueRecursive(id,'price')))
        output.append("|")
        output.append(getValue(id,'color'))
        output.append("|")
        output.extend(getMaterialsString(id))
        output.append("|")
        if(checkValue(id,'container')): #containers
            output.append(str(getValue(id,'container')))
        else:
            output.append("itm_null")
        output.append("|")
        output.append(str(getValueRecursive(id,'volume')))
        output.append("|")
        output.append(str(getValueRecursive(id,'weight')))
        output.append("|")
        output.append(str(getValueRecursive(id,'quench')))
        output.append("|")
        output.append(str(getNutrition(id))) #due to calories and nutrition being used, this is a special case.
        output.append("|")
        output.append(str(getValueOrZero(id,'spoils_in')))
        output.append("|")
        output.append(str(getValueOrZero(id,'stim')))
        output.append("|")
        output.append(str(getValueOrZero(id,'healthy')))
        output.append("|")
        output.append(str(getValueOrZero(id,'addiction_potential')))
        output.append("|")
        charges = getValueOrZero(id,'charges')
        if(charges == 0):
            charges = 1
        output.append(str(charges))
        output.append("|")
        output.append(str(getValueRecursive(id,'fun')))
        output.append("|")
        output.extend(getUseFunctionString(id))
        output.append("|")
        if(checkValue(id,'addiction_type')):
            output.append(str(getValue(id,'addiction_type')))
        else:
            output.append("ADD_NULL")
        output.append("|")
        output.append(str(getValue(id,'description')))
        output.append("|")
        if( not getValueOrZero(id, 'weight') == 0 ):
            output.append(str(math.ceil(float(getValueOrZero(id, 'nutrition') / float(getValueOrZero(id, 'weight')))*100)/100))
        else:
            output.append("!")
        output.append("|")
        output.append(str(getValueRecursive(id,'parasites')))
        if(checkValue(id,'price_postapoc')):
            output.append("|trade_price=")
            output.append(str(getValueRecursive(id,'price_postapoc')))
        output.append("}}\n")
output.append(footer)

Mutagentext = "".join(output)
Mutagentext.replace("\n", "\\n")

site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:Comestibles/Food')
page.text = Foodtext
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts ComestiblesList.py script')
page = pywikibot.Page(site, 'Template:Comestibles/Drinks')
page.text = Drinktext
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts ComestiblesList.py script')
page = pywikibot.Page(site, 'Template:Comestibles/Meds')
page.text = Medstext
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts ComestiblesList.py script')
page = pywikibot.Page(site, 'Template:Comestibles/Mutagen')
page.text = Mutagentext
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts ComestiblesList.py script')

exit()
import json
import sys
import copy
import string
import math
from version import version
#import pywikibot
from cddaWiki import *

#documentation
#Usage: python [location of pywikibotinstall]\pwb.py foragingList.py
#   Then input your password, and wait for the page to be updated.

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
<noinclude>Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts The foragingList.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.\n[[Category:Templates]]\n'''
footer+ = version+'\n</noinclude>'

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

print trashText

'''
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
'''
exit()
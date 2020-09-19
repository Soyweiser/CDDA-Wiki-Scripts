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

def setAbstractIds(): #some items have no ID value set, which this code depends on, but they do have an abstract. This function copies the abstract value into the id value.
    for it in range(0, len(data)):
        if(not 'id' in data[it]):
            if('abstract' in data[it]):
                data[it]['id'] = data[it]['abstract']
            else:
                print 'both no id and no abstract detected ' + str(it)

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

def GetName (element): #when given an element it returns a string with the name it. This is to deal with the system where a json name field can be a string, a dict with 'str', 'str_sp', 'str_pl' (return pref in that order). Returns "" when none can be found.
    if (isinstance(element, str)):
        return element #the simple legacy case.
    if (isinstance(element, dict)):
        if 'str' in element:
            return element['str']
        if 'str_sp' in element:
            return element['str_sp']
        if 'str_pl' in element:
            return element['str_pl']
    return ""

list_item_files = [ 'data/json/items/comestibles.json', 'data/json/items/comestibles/brewing.json', 'data/json/items/comestibles/carnivore.json', 'data/json/items/comestibles/drink.json', 'data/json/items/comestibles/med.json', 'data/json/items/comestibles/mutagen.json', 'data/json/items/comestibles/protein.json', 'data/json/items/comestibles/seed.json', 'data/json/items/comestibles/spice.json', 'data/json/items/classes/comestible.json', 'data/core/basic.json', 'data/json/items/melee.json', 'data/json/items/generic.json', 'data/json/items/chemicals_and_resources.json', 'data/json/items/newspaper.json', 'data/json/items/containers.json', 'data/json/items/tools.json', 'data/json/items/generic/string.json', 'data/json/items/resources/metals.json' ]
list_itemgroup_files = [ 'data/json/item_groups.json', 'data/json/itemgroups/forage.json' ]
data = list()
itemgroup_data = list()


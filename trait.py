import json
import sys
import pywikibot
from version import version
from name_hacks import trait_name
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#on start windows might lose focus for a second due to the Tkinter clipboard hack.
#Data can be automatically copied to the wiki mutation pages.
#Usage: python [location of pywikibotinstall]\pwb.py trait.py
#   Either input 'all' or 'ALL', and then your password, and wait for the pages to be updated.
#   Or: Input a mutation ID to get the mutations location in the array. These are supposed to be permanent ID's.
#   Or: Input an integer, which will print the generated page of that mutation on screen, and copy it to the clipboard.
#   input 'exit' to exit
#Do note that a few of the mutation pages might need some work afterwards, stuff like 'infrared vision' being on the 'Infrared_Vision_(Mutation)' page and bionic variants are not automatically generated.

with open('data/json/mutations/mutations.json') as data_file:
    data = json.load(data_file)

with open('data/json/mutations/mutation_type.json') as data_file: #not needed for wiki editing, but added as a sort of typo check for the json data.
    type_data = json.load(data_file)

types_muts_names = list() #lists of names of the types.
types_muts_dict = dict() #dictionary of types with a list of mutation ID's
for it in range(0, len(type_data)):
    if("type" in type_data[it]):
        if(type_data[it]['type'] == "mutation_type"):
            types_muts_names.append(type_data[it]['id'])
            types_muts_dict[types_muts_names[it]] = list()

ID_mut = dict()
for iterator in range(0, len(data)): #fill the ID_mut dictionary with 'id' data, and fill the types lists.
    keyD = dict()
    keyD['id_nr'] = iterator
    keyD["name"] = data[iterator]["name"]["str"]
    ID_mut[data[iterator]["id"]] = keyD
    if("types" in data[iterator]): #fill the types_muts_dict
        for it in range(0, len(data[iterator]["types"])):
            if (data[iterator]["types"][it] in types_muts_names):
                types_muts_dict[data[iterator]["types"][it]].append(data[iterator]["id"])
            else:
                print "Mutation type not found " + str(data[iterator]["types"][it])

#Prints the mutation types, used for bugfixing.
#for it in range(0, len(types_muts_names)):
#    print types_muts_names[it]
#    for ite in range(0, len(types_muts_dict[types_muts_names[it]])):
#        print " " + types_muts_dict[types_muts_names[it]][ite]

def ID_To_String(id): #Use the name_hacks.py file for some name hacks.
    retval = trait_name (id)
    if (retval == id):
        return ID_mut[id]["name"]
    else:
        return retval

def PageName(id): #returns the pagename of the wiki page, slightly differs from ID_To_String due to ID_To_String leaving in wiki formatting (such as 'Prototype (threshold mutation)|Prototype').
#The ID argument is the integer position of the trait in the data list.
    return ID_To_String(data[id]['id']).split('|',1)[0]

def ID_To_int(id):
    if(id in ID_mut):
        return ID_mut[id]["id_nr"]
    else:
        return -1

#Creates a string with the various attacks this mutation gives or can give.
def Attack_To_String(attack):
    retval = list()
    retval.append("* ")
    if("required_mutations" in attack):
        retval.append("If you also have the ")
        for it in range(0, len(attack["required_mutations"])):
            retval.append('[[')
            retval.append(ID_To_String(attack["required_mutations"][it]))
            retval.append(']]<!--')
            retval.append(attack["required_mutations"][it])
            retval.append('-->')
            if(not(it+1 == len(attack["required_mutations"]))):
                retval.append(", ")
        retval.append(" mutation")
        if(len(attack["required_mutations"]) > 1):
            retval.append("s")
        retval.append(", ")
    
    if("blocker_mutations" in attack):
        if("required_mutations" in attack):
            retval.append("unless you have the ")
        else:
            retval.append("Unless you have the ")
        for it in range(0, len(attack["blocker_mutations"])):
            retval.append('[[')
            retval.append(ID_To_String(attack["blocker_mutations"][it]))
            retval.append(']]<!--')
            retval.append(attack["blocker_mutations"][it])
            retval.append('-->')
            if(not(it+1 == len(attack["blocker_mutations"]))):
                retval.append(", ")
        retval.append(" mutation")
        if(len(attack["blocker_mutations"]) > 1):
            retval.append("s")
        retval.append(", ")
    
    if("blocker_mutations" in attack) or ("required_mutations" in attack):
        retval.append("this mutation gives an additional attack, with a ")
    else:
        retval.append("This mutation gives an additional attack, with a ")
    if(attack["chance"] == 1):
        retval.append("100% chance of activating")
    else:
        retval.append("at minimum one in ")
        retval.append(str(attack["chance"]))
        retval.append(" chance of activating")
    if("body_part" in attack):
        retval.append(", using the {{btt|")
        retval.append(attack["body_part"])
        retval.append("}} body part")
    if ("base_damage" in attack):
        retval.append(", doing ")
        if (isinstance(attack["base_damage"], list)):
            for it2 in range(0, len(attack["base_damage"])):
                retval.append(str(attack["base_damage"][it2]["amount"]))
                retval.append(" points of ")
                retval.append(attack["base_damage"][it2]["damage_type"])
                retval.append(" damage")
                if(not(it2+1 == len(attack["base_damage"]))):
                    retval.append(", and ")
        else:
            retval.append(str(attack["base_damage"]["amount"]))
            retval.append(" points of ")
            retval.append(attack["base_damage"]["damage_type"])
            retval.append(" damage")
    if ("strength_damage" in attack):
        retval.append(", ")
        if ("base_damage" in attack):
            retval.append("and also ")
        retval.append("doing ")
        if (isinstance(attack["strength_damage"], list)):
            for it2 in range(0, len(attack["strength_damage"])):
                retval.append(str(attack["strength_damage"][it2]["amount"]))
                retval.append(" points of ")
                retval.append(attack["strength_damage"][it2]["damage_type"])
                retval.append(" damage ")
                if(not(it2+1 == len(attack["strength_damage"]))):
                    retval.append(", and ")
        else:
            retval.append(str(attack["strength_damage"]["amount"]))
            retval.append(" points of ")
            retval.append(attack["strength_damage"]["damage_type"])
            retval.append(" damage, which is multiplied by [[Strength|strength]]")
    if ("hardcoded_effect" in attack):
        retval.append(", ")
        if ("base_damage" in attack) or ("strength_damage" in attack):
            retval.append("additionally ")
        retval.append("it has a special hardcoded attack effect")
    retval.append(".\n")
    return retval

def generatePage (var): #generates all the data which should be in one of the wiki pages. var is the position of the mutation in the list of mutations.
    output = []
    
    if("player_display" in data[var]): #Just going to assume that if this value is in the data, it is set to false.
        return output
    if("debug" in data[var]): #Just going to assume that if this value is in the data, it is set to true.
        return output
    output = [ "<!-- Automatically generated by https://github.com/Soyweiser/CDDA-Wiki-Scripts The trait.py script. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page.-->{{trait|", data[var]["id"], '|', data[var]["name"]["str"], '|' ]
    
    if("prereqs" in data[var]):
        output.append("PREREQS=")
        for it in range(0, len(data[var]["prereqs"])):
            output.append('[[')
            output.append(ID_To_String(data[var]["prereqs"][it]))
            output.append(']]<!--')
            output.append(data[var]["prereqs"][it])
            output.append('-->')
            if(not(it+1 == len(data[var]["prereqs"]))):
                output.append(", ")
        output.append('|')
        
    if("prereqs2" in data[var]):
        output.append("PREREQS2=")
        for it in range(0, len(data[var]["prereqs2"])):
            output.append('[[')
            output.append(ID_To_String(data[var]["prereqs2"][it]))
            output.append(']]<!--')
            output.append(data[var]["prereqs2"][it])
            output.append('-->')
            if(not(it+1 == len(data[var]["prereqs2"]))):
                output.append(", ")
        output.append('|')
    
    if("cancels" in data[var] or "types" in data[var]): # check if there are cancels that should be listed, also includes the type system, which forces only one option.
        output.append("CANCELS=")
        if("cancels" in data[var]):
            for it in range(0, len(data[var]["cancels"])):
                output.append('[[')
                output.append(ID_To_String(data[var]["cancels"][it]))
                output.append(']]<!--')
                output.append(data[var]["cancels"][it])
                output.append('-->')
                if(it+1 < len(data[var]["cancels"])):
                    output.append(", ")
        if("types" in data[var]):
            if("cancels" in data[var] and "types" in data[var]):
                output.append(", ")
            for it in range(0, len(data[var]["types"])): # loop over the types mutations and add them.
                cancel_types = data[var]["types"][it]
                for ite in range(0, len(types_muts_dict[cancel_types])):
                    if( not types_muts_dict[cancel_types][ite] == data[var]["id"] ): #ignore the mutation we are creating
                        output.append('[[')
                        output.append(ID_To_String(types_muts_dict[cancel_types][ite]))
                        output.append(']]<!--')
                        output.append(types_muts_dict[cancel_types][ite])
                        output.append('-->')
                        if(ite+1 < len(types_muts_dict[cancel_types])):
                             output.append(", ")
                if(it+1 < len(data[var]["types"])):
                    output.append(", ")
        output.append('|')
        
    if("changes_to" in data[var]):
        output.append("CHANGES_TO=")
        for it in range(0, len(data[var]["changes_to"])):
            output.append('[[')
            output.append(ID_To_String(data[var]["changes_to"][it]))
            output.append(']]<!--')
            output.append(data[var]["changes_to"][it])
            output.append('-->')
            if(not(it+1 == len(data[var]["changes_to"]))):
                output.append(", ")
        output.append('|')
        
    if("leads_to" in data[var]):
        output.append("LEADS_TO=")
        for it in range(0, len(data[var]["leads_to"])):
            output.append('[[')
            output.append(ID_To_String(data[var]["leads_to"][it]))
            output.append(']]<!--')
            output.append(data[var]["leads_to"][it])
            output.append('-->')
            if(not(it+1 == len(data[var]["leads_to"]))):
                output.append(", ")
        output.append('|')
        
    
    if("points" in data[var]):
        output.append(str(data[var]["points"]))
        output.append('|')
    else:
        output.append('0|')

    if("visibility" in data[var]):
        output.append(str(data[var]["visibility"]))
        output.append('|')
    else:
        output.append('0|')
    
    if("ugliness" in data[var]):
        output.append(str(data[var]["ugliness"]))
        output.append('|')
    else:
        output.append('0|')
    if(isinstance(data[var]["description"], dict)):
        output.append(data[var]["description"]["str"])
    else:
        output.append(data[var]["description"])
    
    if( "starting_trait" in data[var]):
        output.append('|trait=1')
    
    if( "profession" in data[var]):
        output.append('|profession=1')
    
    if( "valid" in data[var]):
        output.append('|invalid=1')
    
    if( "threshreq" in data[var]):
        output.append('|threshold=1')
        
    if( "purifiable" in data[var]): #naively assuming that when set it is to not be the default value.
        output.append('|purifiable=1')
    
    if( "category" in data[var]):
        if( "LIZARD" in data[var]["category"] ):
            output.append('|lizard=1')
        if( "BIRD" in data[var]["category"] ):
            output.append('|bird=1')
        if( "FISH" in data[var]["category"] ):
            output.append('|fish=1')
        if( "BEAST" in data[var]["category"] ):
            output.append('|beast=1')
        if( "FELINE" in data[var]["category"] ):
            output.append('|feline=1')
        if( "LUPINE" in data[var]["category"] ):
            output.append('|lupine=1')
        if( "URSINE" in data[var]["category"] ):
            output.append('|ursine=1')
        if( "CATTLE" in data[var]["category"] ):
            output.append('|cattle=1')
        if( "INSECT" in data[var]["category"] ):
            output.append('|insect=1')
        if( "PLANT" in data[var]["category"] ):
            output.append('|plant=1')
        if( "SLIME" in data[var]["category"] ):
            output.append('|slime=1')
        if( "TROGLOBITE" in data[var]["category"] ):
            output.append('|troglobite=1')
        if( "CEPHALOPOD" in data[var]["category"] ):
            output.append('|cephalopod=1')
        if( "SPIDER" in data[var]["category"] ):
            output.append('|spider=1')
        if( "MEDICAL" in data[var]["category"] ):
            output.append('|medical=1')
        if( "ALPHA" in data[var]["category"] ):
            output.append('|alpha=1')
        if( "ELFA" in data[var]["category"] ):
            output.append('|elfa=1')
        if( "CHIMERA" in data[var]["category"] ):
            output.append('|chimera=1')
        if( "RAPTOR" in data[var]["category"] ):
            output.append('|raptor=1')
        if( "RAT" in data[var]["category"] ):
            output.append('|rat=1')
        if( "MOUSE" in data[var]["category"] ):
            output.append('|mouse=1')
        if( "MYCUS" in data[var]["category"] ):
            output.append('|mycus=1')
        if( "MARLOSS" in data[var]["category"] ):
            output.append('|marloss=1')
    #footer
    output.append("""}}<noinclude>
<div style="margin: 1em; border: 1px solid #aaa; background-color: #white; padding: 5px;">
<h2><span class="plainlinks" style="float: right; font-size: small">
([[{{lc:{{PAGENAME}}}}/doc|<span title="View user added notes">View</span>]] - [{{fullurl:{{lc:{{PAGENAME}}}}/doc|action=edit}} <span title="Edit user notes">Edit Notes</span>] )</span>Notes</h2>
<!-- *DO NOT EDIT THIS AREA, AUTOMATICALLY GENERATED, USE THE EDIT NOTES BUTTON* -->
""")
    #Active
    if( "active" in data[var] ):
        output.append("* Can be activated, use the {{k|[}} mutation menu.")
        if( "starts_active" in data[var] ):
            output.append(" Starts active.")
        if( "cost" in data[var] ):
            output.append(" Costs: ")
            output.append(str(data[var]['cost']))
            if( "fatigue" in data[var] ):
                output.append(" fatigue")
                if( "hunger" in data[var] or "thirst" in data[var]):
                    output.append(", ")
            if( "hunger" in data[var] ):
                output.append(" hunger")
                if("thirst" in data[var]):
                    output.append(",")
            if( "thirst" in data[var] ):
                output.append(" thirst")
            output.append(" points.")
        if( "time" in data[var] ):
            output.append(" Per ")
            output.append(str(data[var]['time']))
            output.append(" turns of use.")
        output.append("\n")
    #Bodytemp
    if( "bodytemp_modifiers" in data[var] ):
        output.append("* Adds [[Body temperature|body temperature]], adds ")
        output.append(str(data[var]['bodytemp_modifiers'][0]))
        output.append(" when overheating, and ")
        output.append(str(data[var]['bodytemp_modifiers'][1]))
        output.append(" normally.\n")
    if( "bodytemp_sleep" in data[var] ):
        output.append("* ")
        output.append(str(data[var]['bodytemp_sleep']))
        output.append(" additional body temperature will be added while sleeping.\n")

    #Wet_protection
    if( "wet_protection" in data[var] ):
        output.append("* Gives [[wet]] protection:\n")
        for it in range(0, len(data[var]["wet_protection"])):
            output.append("** {{btt|")
            output.append(data[var]["wet_protection"][it]["part"])
            output.append("}}")
            for it2 in range(0, len(data[var]["wet_protection"][it])):
                if (it2 > 1):
                    output.append(",")
                if (data[var]["wet_protection"][it].keys()[it2] != "part"):
                    output.append(" ")
                    output.append(str(data[var]["wet_protection"][it][data[var]["wet_protection"][it].keys()[it2]]))
                    output.append(" ")
                    output.append(data[var]["wet_protection"][it].keys()[it2])
                    output.append(" protection")
            output.append(".\n")
    #Armor
    if( "armor" in data[var] ):
        output.append("* Provides the following armor values.\n")
        for it in range(0, len(data[var]["armor"])):
            if not (isinstance(data[var]["armor"][it]["parts"], list)):
                if (data[var]["armor"][it]["parts"] == "ALL"):
                    output.append("** All locations:")
                    for it2 in range(0, len(data[var]["armor"][it])):
                        if (it2 > 1):
                            output.append(",")
                        if (data[var]["armor"][it].keys()[it2] != "parts"):
                            output.append(" ")
                            output.append(str(data[var]["armor"][it][data[var]["armor"][it].keys()[it2]]))
                            output.append(" ")
                            output.append(data[var]["armor"][it].keys()[it2])
                            output.append(" protection")
                    output.append(".\n")
                        
        for it in range(0, len(data[var]["armor"])):
            if (data[var]["armor"][it]["parts"] != "ALL"):
                output.append("** ")
                if (isinstance(data[var]["armor"][it]["parts"], list)):
                    for it2 in range(0, len(data[var]["armor"][it]["parts"])):
                        if(it2 > 0):
                            output.append(", ")
                        output.append("{{btt|")
                        output.append(data[var]["armor"][it]["parts"][it2])
                        output.append("}}")
                else:
                    output.append("{{btt|")
                    output.append(data[var]["armor"][it]["parts"])
                    output.append("}}")
                output.append(" location")
                if (it > 0):
                    output.append("s")
                output.append(":")
                for it2 in range(0, len(data[var]["armor"][it])):
                    if (it2 > 0):
                        output.append(",")
                    if (data[var]["armor"][it].keys()[it2] != "parts"):
                        output.append(" ")
                        output.append(str(data[var]["armor"][it][data[var]["armor"][it].keys()[it2]]))
                        output.append(" ")
                        output.append(data[var]["armor"][it].keys()[it2])
                        output.append(" protection")
                output.append("\n")
                
    #Restricts Gear
    if( "restricts_gear" in data[var] ):
        output.append("* This mutation removes the ability to wear gear in the ")
        for it in range(0, len(data[var]["restricts_gear"])):
            output.append("{{btt|")
            output.append(data[var]["restricts_gear"][it])
            output.append("}}")
            if(not(it+1 == len(data[var]["restricts_gear"]))):
                output.append(", ")
        output.append(" location")
        if(it > 1):
            output.append("s")
        output.append(".\n")
        
    if( "allow_soft_gear" in data[var] ):
        output.append("** Unless the gear is made of a soft [[material]].\n")
    if( "destroys_gear" in data[var] ):
        output.append("** Any invalid gear that is equipped in the slots above will be destroyed on mutation.\n")
    
    if( "encumbrance_always" in data[var] ):
        output.append("* Adds permanent encumbrance in the following locations: ")
        if (isinstance(data[var]["encumbrance_always"], list)):
            for it in range(0, len(data[var]["encumbrance_always"])):
                output.append("{{btt|")
                output.extend(data[var]["encumbrance_always"][it][0])
                output.extend("}} : ")
                output.extend(str(data[var]["encumbrance_always"][it][1]))
                if(not(it+1 == len(data[var]["encumbrance_always"]))):
                    output.append(", ")
        else:
            print(type(data[var]["encumbrance_always"]))
            output.extend((data[var]["encumbrance_always"]))
        output.append(".\n")
        
    if( "encumbrance_covered" in data[var] ):
        output.append("* Adds encumbrance in the following locations: ")
        if (isinstance(data[var]["encumbrance_covered"], list)):
            for it in range(0, len(data[var]["encumbrance_covered"])):
                output.append("{{btt|")
                output.extend(data[var]["encumbrance_covered"][it][0])
                output.extend("}} : ")
                output.extend(str(data[var]["encumbrance_covered"][it][1]))
                if(not(it+1 == len(data[var]["encumbrance_covered"]))):
                    output.append(", ")
        else:
            print(type(data[var]["encumbrance_covered"]))
            output.extend((data[var]["encumbrance_covered"]))
        output.append(", if the location is covered by clothing lacking the OVERSIZE flag.\n")
    
    #Metabolism/healing/HP modifiers.
    if( "hp_adjustment" in data[var] ):
        if( data[var]["hp_adjustment"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("maximum [[Stats#Hit points|Hit points]] of each body part by ")
        output.extend(str(abs(data[var]["hp_adjustment"])))
        output.extend(".\n")
    if( "hp_modifier" in data[var] ):
        if( data[var]["hp_modifier"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("maximum [[Stats#Hit points|Hit points]] of each body part by: ")
        output.extend(str(abs(data[var]["hp_modifier"]) * 100))
        output.extend("%.\n")
    if( "hp_modifier_secondary" in data[var] ):
        if( data[var]["hp_modifier_secondary"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("maximum [[Stats#Hit points|Hit points]] of each body part by: ")
        output.extend(str(abs(data[var]["hp_modifier_secondary"]) * 100))
        output.extend("%. This bonus stacks with any bonus generated by starting traits like [[Tough]]\n")
    if( "metabolism_modifier" in data[var] ):
        if( data[var]["metabolism_modifier"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("[[Hidden_stats#Hunger|hunger]] increase over time by ")
        output.extend(str(abs(data[var]["metabolism_modifier"]) * 100))
        output.extend("%.\n")
    if( "thirst_modifier" in data[var] ):
        if( data[var]["thirst_modifier"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("[[Hidden_stats#Thirst|thirst]] increase over time by ")
        output.extend(str(abs(data[var]["thirst_modifier"]) * 100))
        output.extend("%.\n")
    if( "fatigue_modifier" in data[var] ):
        if( data[var]["fatigue_modifier"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("[[Hidden_stats#Fatigue|fatigue]] increase over time by ")
        output.extend(str(abs(data[var]["fatigue_modifier"]) * 100))
        output.extend("%.\n")
    if( "fatigue_regen_modifier" in data[var] ):
        if( data[var]["fatigue_regen_modifier"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("the rate at which [[Hidden_stats#Fatigue|fatigue]] drops while [[Sleep|resting]] by ")
        output.extend(str(abs(data[var]["fatigue_regen_modifier"]) * 100))
        output.extend("%.\n")
    if( "stamina_regen_modifier" in data[var] ):
        if( data[var]["stamina_regen_modifier"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("the rate at which [[Hidden_stats#Stamina|stamina]] regenerates by ")
        output.extend(str(abs(data[var]["stamina_regen_modifier"]) * 100))
        output.extend("%.\n")
    if( "max_stamina_modifier" in data[var] ):
        if( data[var]["max_stamina_modifier"] >= 1 ):
            output.extend("* Increases max stamina by ")
            output.extend(str((abs(data[var]["max_stamina_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces max stamina by ")
            output.extend(str((1 - abs(data[var]["max_stamina_modifier"])) * 100))
            output.extend("%.\n")
    if( "healing_awake" in data[var] ):
        if( data[var]["healing_awake"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Damages (also causes [[Pain]]) ")
        output.extend("[[Stats#Hit points|hit points]] over time while awake by ")
        output.extend(str(abs(data[var]["healing_awake"])))
        output.extend(" per turn.\n")
    if( "healing_resting" in data[var] ):
        if( data[var]["healing_resting"] >= 0 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("the rate of [[Stats#Hit points|healing]] while [[Sleep|sleeping]] by ")
        output.extend(str(abs(data[var]["healing_resting"])))
        output.extend(".\n")
    if( "mending_modifier" in data[var] ):
        if( data[var]["mending_modifier"] >= 1 ):
            output.extend("* Increases the rate at which [[Broken limb|broken limbs]] heal by ")
            output.extend(str((abs(data[var]["mending_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces the rate at which [[Broken limb|broken limbs]] heal by ")
            output.extend(str((1 - abs(data[var]["mending_modifier"])) * 100))
            output.extend("%.\n")
        
    #Speed mods
    if( "reading_speed_multiplier" in data[var] ):
        if( data[var]["reading_speed_multiplier"] >= 1 ):
            output.extend("* Increases ")
        else:
            output.extend("* Reduces ")
        output.extend("[[books]] reading time to ")
        output.extend(str(abs(data[var]["reading_speed_multiplier"]) * 100))
        output.extend("% of normal.\n")
    if( "movecost_modifier" in data[var] ):
        if( data[var]["movecost_modifier"] >= 1 ):
            output.extend("* Increases movement cost by ")
            output.extend(str((abs(data[var]["movecost_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces movement cost by ")
            output.extend(str((1 - abs(data[var]["movecost_modifier"])) * 100))
            output.extend("%.\n")
    if( "movecost_flatground_modifier" in data[var] ):
        if( data[var]["movecost_flatground_modifier"] >= 1 ):
            output.extend("* Increases movement cost on flat ground by ")
            output.extend(str((abs(data[var]["movecost_flatground_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces movement cost on flat ground by ")
            output.extend(str((1 - abs(data[var]["movecost_flatground_modifier"])) * 100))
            output.extend("%.\n")
    if( "movecost_swim_modifier" in data[var] ):
        if( data[var]["movecost_swim_modifier"] >= 1 ):
            output.extend("* Increases swimming movement cost by roughly ")
            output.extend(str((abs(data[var]["movecost_swim_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces swimming movement cost by roughly ")
            output.extend(str((1 - abs(data[var]["movecost_swim_modifier"])) * 100))
            output.extend("%.\n")
    if( "movecost_obstacle_modifier" in data[var] ):
        if( data[var]["movecost_obstacle_modifier"] >= 1 ):
            output.extend("* Increases movement cost on difficulty terrain (movecost > 100) by ")
            output.extend(str((abs(data[var]["movecost_obstacle_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces movement cost on difficulty terrain (movecost > 100) by ")
            output.extend(str((1 - abs(data[var]["movecost_obstacle_modifier"])) * 100))
            output.extend("%. (minimum move cost is still 100).\n")
    if( "speed_modifier" in data[var] ):
        if( data[var]["speed_modifier"] >= 1 ):
            output.extend("* Increases speed by ")
            output.extend(str((abs(data[var]["speed_modifier"]) - 1) * 100))
            output.extend("%. This basically makes you do everything faster.\n")
        else:
            output.extend("* Reduces speed (which influences the amount of actions taken) by ")
            output.extend(str((1 - abs(data[var]["speed_modifier"])) * 100))
            output.extend("%. This basically makes you do everything slower.\n")
    # if( "temperature_speed_modifier" in data[var] ): no need to include this, mutation descriptions already do.
    if( "attackcost_modifier" in data[var] ):
        if( data[var]["attackcost_modifier"] >= 1 ):
            output.extend("* Increases attack and throwing cost by ")
            output.extend(str((abs(data[var]["attackcost_modifier"]) - 1) * 100))
            output.extend("%.\n")
        else:
            output.extend("* Reduces attack and throwing cost by ")
            output.extend(str((1 - abs(data[var]["attackcost_modifier"])) * 100))
            output.extend("%.\n")
    
    #Martial Arts
    if( "initial_ma_styles" in data[var] ):
        if (isinstance(data[var]["initial_ma_styles"], list)):
            output.extend("* This trait gives access to one of the following [[Martial arts|martial art styles]]: ")
            for it in range(0, len(data[var]["initial_ma_styles"])):
                output.extend("{{MArttoname|")
                output.extend(data[var]["initial_ma_styles"][it])
                output.extend("}}")
                if(not(it+1 == len(data[var]["initial_ma_styles"]))):
                    output.extend(", ")
                else:
                    output.extend(".\n")
    
    #Passive mods
    if( "passive_mods" in data[var] ):
        if( "str_mod" in data[var]["passive_mods"] ):
            output.extend("* Modifies [[Stats|strength]] by ")
            output.extend(str(data[var]["passive_mods"]["str_mod"]))
            output.extend(".\n")
        if( "dex_mod" in data[var]["passive_mods"] ):
            output.extend("* Modifies [[Stats|dexterity]] by ")
            output.extend(str(data[var]["passive_mods"]["dex_mod"]))
            output.extend(".\n")
        if( "int_mod" in data[var]["passive_mods"] ):
            output.extend("* Modifies [[Stats|intelligence]] by ")
            output.extend(str(data[var]["passive_mods"]["int_mod"]))
            output.extend(".\n")
        if( "per_mod" in data[var]["passive_mods"] ):
            output.extend("* Modifies [[Stats|perception]] by ")
            output.extend(str(data[var]["passive_mods"]["per_mod"]))
            output.extend(".\n")
    
    #Convert attacks.
    if( "attacks" in data[var] ):
        if (isinstance(data[var]["attacks"], list)):
            for it in range(0, len(data[var]["attacks"])):
                output.extend(Attack_To_String(data[var]["attacks"][it]))
        else:
            output.extend(Attack_To_String(data[var]["attacks"]))
    #Convert social modifiers.
    if( "social_modifiers" in data[var] ):
        if (isinstance(data[var]["social_modifiers"], dict)):
            if( "lie" in data[var]['social_modifiers'] ):
                if( data[var]['social_modifiers']['lie'] >= 0 ):
                    output.extend("* Increases ")
                else:
                    output.extend("* Reduces ")
                output.extend("chance of lying to [[NPC]]s by ")
                output.extend(str(abs(data[var]['social_modifiers']['lie'])))
                output.extend("%.\n")
            if( "persuade" in data[var]['social_modifiers'] ):
                if( data[var]['social_modifiers']['persuade'] >= 0 ):
                    output.extend("* Increases ")
                else:
                    output.extend("* Reduces ")
                output.extend("chance of persuading [[NPC]]s to do your bidding by ")
                output.extend(str(abs(data[var]['social_modifiers']['persuade'])))
                output.extend("%.\n")
            if( "intimidate" in data[var]['social_modifiers'] ):
                if( data[var]['social_modifiers']['intimidate'] >= 0 ):
                    output.extend("* Increases ")
                else:
                    output.extend("* Reduces ")
                output.extend("chance of intimidating [[NPC]]s by ")
                output.extend(str(abs(data[var]['social_modifiers']['intimidate'])))
                output.extend("%.\n")
    output.append("""<!-- 

*YOUR PERSONAL NOTES AND HINTS SHOULD GO IN THE """ + PageName(var) +"""/doc PAGE DO NOT EDIT HERE*

-->
{{#ifexist:{{lc:{{PAGENAME}}}}/doc| {{:{{lc:{{PAGENAME}}}}/doc}} |}}<!-- list the doc page if it exists-->
<span class="plainlinks" style="font-size: small"><center>( [{{fullurl:{{lc:{{PAGENAME}}}}/doc|action=edit}} <span title="Edit user notes">Edit Notes</span>] )</center></span>
</div>""")
    output.append("\n")
    if( "starting_trait" in data[var] ) or ( "profession" in data[var] ) :
        output.append("{{Navbar/traits}}\n")
    output.append("[[category: Mutations]]\n")
    if( "threshreq" in data[var]):
        output.append("[[category: Post-threshold mutations]]\n")
    output.append(version + "</noinclude>")
    output = "".join(output)
    output.replace("\n", "\\n")
    return output

var = raw_input(">")
while True:
    while var.isdigit():
        var = int(var)
        if(var < 0):
            root.update()
            root.destroy()
            exit()
        text = generatePage(var)
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
        elif ( var == 'all' or var == 'ALL' ):
            site = pywikibot.Site('en', 'cddawiki')
            for x in range(0, len(data)):
                
                text = generatePage(x)
                if( text != []): #don't print an empty page
                    page = pywikibot.Page(site, PageName(x) )
                    page.text = text
                    page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts trait.py script')
            var = raw_input(">")
        else:
            print ID_To_int(var)
            var = raw_input(">")
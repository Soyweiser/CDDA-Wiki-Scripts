import json
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

#on start windows might lose focus for a second due to the Tkinter clipboard hack.
#Use 'exit' to exit
#Type in a positive int to convert a mutation at that location in the data list into the mediawiki code. Positioning over different versions of the json files is not guaranteed.
#   The conversion is echoed, and automatically loaded in the clipboard. Just copy paste and edit into the wiki.
#Enter a mutation ID to get the mutations location in the array. These are supposed to be permanent ID's.
#Do note that a few of the mutation pages need some work afterwards, stuff like 'infrared vision' being on the 'Infrared_Vision_(Mutation)' page and bionic variants are not automatically generated.


with open('data/json/mutations.json') as data_file:
    data = json.load(data_file)

ID_mut = dict()
for iterator in range(0, len(data)):
    keyD = dict()
    keyD['id_nr'] = iterator
    keyD["name"] = data[iterator]["name"]
    ID_mut[data[iterator]["id"]] = keyD
    
def ID_To_String(id):
    return ID_mut[id]["name"]

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


var = raw_input(">")
while True:
    while var.isdigit():
        var = int(var)
        if(var < 0):
            root.update()
            root.destroy()
            exit()
        output = [ "{{trait|", data[var]["id"], '|', data[var]["name"], '|' ]
        
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
        
        if("cancels" in data[var]):
            output.append("CANCELS=")
            for it in range(0, len(data[var]["cancels"])):
                output.append('[[')
                output.append(ID_To_String(data[var]["cancels"][it]))
                output.append(']]<!--')
                output.append(data[var]["cancels"][it])
                output.append('-->')
                if(it+1 < len(data[var]["cancels"])):
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
        output.append("}}\n<noinclude>\n==Notes==\n")
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
                        output.append(", ")
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
                    if (it2 > 0):
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
            output.extend(str(data[var]["hp_adjustment"]))
            output.extend(".\n")
        if( "hp_modifier" in data[var] ):
            if( data[var]["hp_modifier"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("maximum [[Stats#Hit points|Hit points]] of each body part by a factor of: ")
            output.extend(str(data[var]["hp_modifier"]))
            output.extend(". (1.0 is a 100% bonus, 0.1 is a 10%).\n")
        if( "hp_modifier_secondary" in data[var] ):
            if( data[var]["hp_modifier_secondary"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("maximum [[Stats#Hit points|Hit points]] of each body part by a factor of: ")
            output.extend(str(data[var]["hp_modifier_secondary"]))
            output.extend(". (1.0 is a 100% bonus, 0.1 is a 10%). This bonus stacks with any bonus generated by starting traits like [[Tough]]\n")
        if( "metabolism_modifier" in data[var] ):
            if( data[var]["metabolism_modifier"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("[[Hidden_stats#Hunger|hunger]] increase over time by ")
            output.extend(str(data[var]["metabolism_modifier"]))
            output.extend(" (1.0 doubles usage, -0.5 halves).\n")
        if( "thirst_modifier" in data[var] ):
            if( data[var]["thirst_modifier"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("[[Hidden_stats#Thirst|thirst]] increase over time by ")
            output.extend(str(data[var]["thirst_modifier"]))
            output.extend(" (1.0 doubles usage, -0.5 halves).\n")
        if( "fatigue_modifier" in data[var] ):
            if( data[var]["fatigue_modifier"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("[[Hidden_stats#Fatigue|fatigue]] increase over time by ")
            output.extend(str(data[var]["fatigue_modifier"]))
            output.extend(" (1.0 doubles usage, -0.5 halves).\n")
        if( "fatigue_regen_modifier" in data[var] ):
            if( data[var]["fatigue_regen_modifier"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("the rate at which [[Hidden_stats#Fatigue|fatigue]] drops while [[Sleep|resting]] by ")
            output.extend(str(data[var]["fatigue_regen_modifier"]))
            output.extend(" (1.0 doubles usage, -0.5 halves).\n")
        if( "stamina_regen_modifier" in data[var] ):
            if( data[var]["stamina_regen_modifier"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("the rate at which [[Hidden_stats#Stamina|stamina]] regenerates by ")
            output.extend(str(data[var]["stamina_regen_modifier"]))
            output.extend(" (1.0 doubles usage, -0.5 halves).\n")
        if( "healing_awake" in data[var] ):
            if( data[var]["healing_awake"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Damages (also causes [[Pain]]) ")
            output.extend("[[Stats#Hit points|hit points]] over time while awake by ")
            output.extend(str(data[var]["healing_awake"]))
            output.extend(" per turn.\n")
        if( "healing_resting" in data[var] ):
            if( data[var]["healing_resting"] >= 0 ):
                output.extend("* Increases ")
            else:
                output.extend("* Reduces ")
            output.extend("the rate of [[Stats#Hit points|healing]] while [[Sleep|sleeping]] by ")
            output.extend(str(data[var]["healing_resting"]))
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
                print(type(data[var]["attacks"]))
                output.extend(Attack_To_String(data[var]["attacks"]))
        #Convert social modifiers.
        if( "social_modifiers" in data[var] ):
            if (isinstance(data[var]["social_modifiers"], dict)):
                if( "lie" in data[var]['social_modifiers'] ):
                    output.extend("* Increases chance of lying to [[NPC]]s by ")
                    output.extend(str(data[var]['social_modifiers']['lie']))
                    output.extend("%.\n")
                if( "persuade" in data[var]['social_modifiers'] ):
                    output.extend("* Increases chance of persuading [[NPC]]s to do your bidding by ")
                    output.extend(str(data[var]['social_modifiers']['persuade']))
                    output.extend("%.\n")
                if( "intimidate" in data[var]['social_modifiers'] ):
                    output.extend("* Increases chance of intimidating [[NPC]]s by ")
                    output.extend(str(data[var]['social_modifiers']['intimidate']))
                    output.extend("%.\n")

        output.append("<!-- *YOUR PERSONAL NOTES AND HINTS GO BELOW HERE* -->\n")
        
        output.append("\n")
        if( "starting_trait" in data[var] ) or ( "profession" in data[var] ) :
            output.append("{{Navbar/traits}}\n")

        output.append("[[category: Mutations]]\n")
        if( "threshreq" in data[var]):
            output.append("[[category: Post-threshold mutations]]\n")
            
        output.append("{{ver|0.D}}\n</noinclude>")

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
            print ID_To_int(var)
            var = raw_input(">")
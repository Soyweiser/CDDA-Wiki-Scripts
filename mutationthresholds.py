import json
import sys
import pywikibot
from version import version
from name_hacks import trait_name

#Documentation
#Data is uploaded automatically, on various used for the Template:Mutationthresholds/[mutation category name] pages, which are then included by the various mutation category pages.
#Usage: python [location of pywikibotinstall]\pwb.py mutationthresholds.py
#   Then input your password, and wait for the page to be updated.


with open('data/json/mutations/mutations.json') as data_file:    
    data = json.load(data_file)

list_categories = [ 'Lizard', 'Bird', 'Fish', 'Beast', 'Feline', 'Lupine', 'Ursine', 'Cattle', 'Insect', 'Plant', 'Slime (Mutation category)|Slime', 'Troglobite_(Mutation_category)|Troglobite', 'Cephalopod', 'Spider', 'Rat', 'Medical', 'Alpha', 'Elf-A', 'Chimera', 'Raptor', 'Mouse', 'Mycus (Mutation category)|Mycus', 'Marloss' ]

dict_categories = { 'LIZARD' : 'Lizard', 'BIRD' : 'Bird', 'FISH' : 'Fish', 'BEAST' : 'Beast', 'FELINE' : 'Feline', 'LUPINE' : 'Lupine', 'URSINE' : 'Ursine', 'CATTLE' : 'Cattle', 'INSECT' : 'Insect', 'PLANT' : 'Plant', 'SLIME' : 'Slime (Mutation category)|Slime', 'TROGLOBITE' : 'Troglobite_(Mutation_category)|Troglobite', 'CEPHALOPOD' : 'Cephalopod', 'SPIDER' : 'Spider', 'RAT' : 'Rat', 'MEDICAL' : 'Medical', 'ALPHA' : 'Alpha', 'ELFA' : 'Elf-A', 'CHIMERA' : 'Chimera', 'RAPTOR' : 'Raptor', 'MOUSE' : 'Mouse', 'MYCUS' : 'Mycus (Mutation category)|Mycus', 'MARLOSS' : 'Marloss' }

Name_Mut = dict()
for iterator in range(0, len(data)): #fill the Name_mut dictionary with 'name' -> ID data
    keyD = dict()
    keyD['name'] = data[iterator]["name"]["str"]
    keyD["id"] = data[iterator]["id"]
    Name_Mut[data[iterator]["name"]["str"]] = keyD

def Name_To_String(name): #Use the name_hacks.py file for some name hacks.
    retval = trait_name (Name_Mut[name]["id"])
    if (retval == Name_Mut[name]["id"]):
        return name
    else:
        return retval

mut_trait = dict()
for iterator in range(0, len(list_categories)):
    traits = dict()
    traits['traits'] = list()
    traits['mutations'] = list()
    traits['threshold'] = list()
    mut_trait[list_categories[iterator]] = traits
    
for iterator in range(0, len(data)):
    if("category" in data[iterator]):
        if("starting_trait" in data[iterator]):
            for it in data[iterator]['category']:
                mut_trait[dict_categories[it]]['traits'].append(data[iterator]['name']["str"])
        elif("threshreq" in data[iterator]):
            for it in data[iterator]['category']:
                mut_trait[dict_categories[it]]['threshold'].append(data[iterator]['name']["str"])
        else:
            for it in data[iterator]['category']:
                mut_trait[dict_categories[it]]['mutations'].append(data[iterator]['name']["str"])
    
def generate_mutationthreshold_data(var): #variable var is the index of the list_categories list. Returns string.
    output = []
    if (var > len(list_categories)):
        return output
    output = [ "<!--Automatically generated using https://github.com/Soyweiser/CDDA-Wiki-Scripts mutationthresholds.py Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. -->\n= Traits = \n"]
    for it in range(0, len(mut_trait[list_categories[int(var)]]['traits'])):
        output.append("{{:")
        output.append(Name_To_String(mut_trait[list_categories[int(var)]]['traits'][it]))
        output.append("}}\n")
    
    output.append("\n= Normal Mutations =\n")
    for it in range(0, len(mut_trait[list_categories[int(var)]]['mutations'])):
        output.append("{{:")
        output.append(Name_To_String(mut_trait[list_categories[int(var)]]['mutations'][it]))
        output.append("}}\n")
        
    output.append("\n= Post-threshold mutations =\n")
    for it in range(0, len(mut_trait[list_categories[int(var)]]['threshold'])):
        output.append("{{:")
        output.append(Name_To_String(mut_trait[list_categories[int(var)]]['threshold'][it]))
        output.append("}}\n")
    output.append("<!-- End of automatically generated data --><noinclude>This page is used to automatically include various mutations on the threshold mutation category page. Please don't edit this, but use [https://github.com/Soyweiser/CDDA-Wiki-Scripts mutationthresholds.py] to update this page.\n"+version+"</noinclude>")
    text = "".join(output)
    text.replace("\n", "\\n")
    print "generated " + list_categories[var]
    return text

site = pywikibot.Site('en', 'cddawiki')
for it in range(0, len(list_categories)):
    output = generate_mutationthreshold_data(it)
    if(list_categories[it].find("|") == -1):
        pagename = "Template:Mutationthresholds/" + list_categories[it]
    else:
        pagename = "Template:Mutationthresholds/" + list_categories[it].split('|',2)[1]
    page = pywikibot.Page(site, pagename)
    page.text = output
    page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts mutationthresholds.py script')
exit()
import json
import sys
import pywikibot
from version import version
from name_hacks import trait_name

#Data is automatically copied to the wiki template page.
#Usage: python [location of pywikibotinstall]\pwb.py mutationtable.py
#   Then input your password, and wait for the page to be updated.

with open('data/json/mutations/mutations.json') as data_file:
    data = json.load(data_file)

list_categories = [ 'Lizard', 'Bird', 'Fish', 'Beast', 'Feline', 'Lupine', 'Ursine', 'Cattle', 'Insect', 'Plant', 'Slime (Mutation category)|Slime', 'Troglobite_(Mutation_category)|Troglobite', 'Cephalopod', 'Spider', 'Rat', 'Medical', 'Alpha', 'Elf-A', 'Chimera', 'Raptor', 'Mouse', 'Mycus', 'Marloss' ]

dict_categories = { 'LIZARD' : 'Lizard', 'BIRD' : 'Bird', 'FISH' : 'Fish', 'BEAST' : 'Beast', 'FELINE' : 'Feline', 'LUPINE' : 'Lupine', 'URSINE' : 'Ursine', 'CATTLE' : 'Cattle', 'INSECT' : 'Insect', 'PLANT' : 'Plant', 'SLIME' : 'Slime (Mutation category)|Slime', 'TROGLOBITE' : 'Troglobite_(Mutation_category)|Troglobite', 'CEPHALOPOD' : 'Cephalopod', 'SPIDER' : 'Spider', 'RAT' : 'Rat', 'MEDICAL' : 'Medical', 'ALPHA' : 'Alpha', 'ELFA' : 'Elf-A', 'CHIMERA' : 'Chimera', 'RAPTOR' : 'Raptor', 'MOUSE' : 'Mouse', 'MYCUS' : 'Mycus', 'MARLOSS' : 'Marloss' }

dict_styles = { 'Lizard' : "background:khaki; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Bird' : "groupstyle = background:DeepSkyBlue; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Fish' : "background:Aquamarine; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Beast' : "background:tomato; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Feline' : "background:SandyBrown; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Lupine' : "background:darkgrey; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Ursine' : "background:brown; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Cattle' : "background:Peru; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Insect' : "background:yellow; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Plant' : "background:ForestGreen; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Slime (Mutation category)|Slime' : "background:GreenYellow; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Troglobite_(Mutation_category)|Troglobite' : "background:SlateGray; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Cephalopod' : "background:purple; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Spider' : "background:orange; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Rat' : "background:grey; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Medical' : "background:red; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Alpha' : "background:SkyBlue; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Elf-A' : "background:lightgreen; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Chimera' : "background:IndianRed; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Raptor' : "background:green; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;",
 'Mouse' : "background:lightgrey; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;"
 }
    
output = [ """<!-- Automatically generated by https://github.com/Soyweiser/CDDA-Wiki-Scripts The mutationtable.py script. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page.
-->{{Navbox
|name       = Mutationtable
|title      = [[Mutation|Mutations]]
|state      = uncollapsed

|bodystyle = background:white; width:100%; vertical-align:middle; border-color: #CCAAAA;
|titlestyle = background:Aqua; color:darkblue; padding-left:1em; padding-right:1em; text-align:center;
|groupstyle = background:Aqua; color:black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold;

"""]

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

mut_neutral = list()

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
    else:
        if("valid" not in data[iterator]):
            mut_neutral.append(data[iterator]['name']["str"])
        elif("starting_trait" in data[iterator]):
            mut_neutral.append(data[iterator]['name']["str"])

for iterator in range(0, len(list_categories)):
    if (list_categories[iterator] != 'Marloss') and (list_categories[iterator] != 'Mycus'):
        output.append("|group")
        output.append(str(iterator+1))
        output.append("     = [[")
        output.append(list_categories[iterator])
        output.append("]]\n|list")
        output.append(str(iterator+1))
        output.append("""      = {{Navbox|child 
	| groupstyle = """)
        output.append(dict_styles[list_categories[iterator]])
        output.append("""

	| group1 = Trait-like
	| list1  = <!--\n""")
        for it in range(0, len(mut_trait[list_categories[iterator]]['traits'])):
            output.append("        -->")
            if it > 0:
                output.append(" {{md}}")
            output.append("[[")
            output.append(Name_To_String(mut_trait[list_categories[iterator]]['traits'][it]))
            output.append("]]<!--\n")
        output.append("""-->

	| group2 = Normal
	| list2  = <!--\n""")
        for it in range(0, len(mut_trait[list_categories[iterator]]['mutations'])):
            output.append("        -->")
            if it > 0:
                output.append(" {{md}}")
            output.append("[[")
            output.append(Name_To_String(mut_trait[list_categories[iterator]]['mutations'][it]))
            output.append("]]<!--\n")
        output.append("""-->

	| group3 = Post-threshold
	| list3  = <!--\n""")
        for it in range(0, len(mut_trait[list_categories[iterator]]['threshold'])):
            output.append("        -->")
            if it > 0:
                output.append(" {{md}}")
            output.append("[[")
            output.append(Name_To_String(mut_trait[list_categories[iterator]]['threshold'][it]))
            output.append("]]<!--\n")
    
        output.append("""        -->
        }}""")

output.append("""
|group""")
output.append(str(len(list_categories)-1))
output.append("""     = Neutral
|list""")
output.append(str(len(list_categories)-1))
output.append("""      = <!--\n""")
for it in range(0, len(mut_neutral)):
    output.append("        -->")
    if it > 0:
        output.append(" {{md}}")
    output.append("[[")
    output.append(Name_To_String(mut_neutral[it]))
    output.append("]]<!--\n")


output.append("""\n        -->\n}}<noinclude>
<!--Automatically generated using https://github.com/Soyweiser/CDDA-Wiki-Scripts -->
[[Category:Navigational templates]]\n""")
output.append(version)
output.append("</noinclude>")

text = "".join(output)
text.replace("\n", "\\n")
site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:Mutationtable')
page.text = text
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts mutationtable.py script')
exit()

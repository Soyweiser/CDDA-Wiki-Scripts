import json
import sys
import pywikibot

#Data is automatically copied to the wiki template page.
#Usage: python [location of pywikibotinstall]\pwb.py mutationtable.py
#   Then input your password, and wait for the page to be updated.

with open('data/json/mutations.json') as data_file:    
    data = json.load(data_file)

list_categories = [ 'Lizard', 'Bird', 'Fish', 'Beast', 'Feline', 'Lupine', 'Ursine', 'Cattle', 'Insect', 'Plant', 'Slime (Mutation category)|Slime', 'Troglobite_(Mutation_category)|Troglobite', 'Cephalopod', 'Spider', 'Rat', 'Medical', 'Alpha', 'Elf-A', 'Chimera', 'Raptor', 'Mycus', 'Marloss' ]

dict_categories = { 'MUTCAT_LIZARD' : 'Lizard', 'MUTCAT_BIRD' : 'Bird', 'MUTCAT_FISH' : 'Fish', 'MUTCAT_BEAST' : 'Beast', 'MUTCAT_FELINE' : 'Feline', 'MUTCAT_LUPINE' : 'Lupine', 'MUTCAT_URSINE' : 'Ursine', 'MUTCAT_CATTLE' : 'Cattle', 'MUTCAT_INSECT' : 'Insect', 'MUTCAT_PLANT' : 'Plant', 'MUTCAT_SLIME' : 'Slime (Mutation category)|Slime', 'MUTCAT_TROGLOBITE' : 'Troglobite_(Mutation_category)|Troglobite', 'MUTCAT_CEPHALOPOD' : 'Cephalopod', 'MUTCAT_SPIDER' : 'Spider', 'MUTCAT_RAT' : 'Rat', 'MUTCAT_MEDICAL' : 'Medical', 'MUTCAT_ALPHA' : 'Alpha', 'MUTCAT_ELFA' : 'Elf-A', 'MUTCAT_CHIMERA' : 'Chimera', 'MUTCAT_RAPTOR' : 'Raptor', 'MUTCAT_MYCUS' : 'Mycus', 'MUTCAT_MARLOSS' : 'Marloss' }

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
 'Raptor' : "background:green; color:Black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold; white-space:nowrap;"
 }
    
output = [ """{{Navbox
|name       = Mutations
|title      = [[Mutations]]
|state      = uncollapsed

|bodystyle = background:white; width:100%; vertical-align:middle; border-color: #CCAAAA;
|titlestyle = background:Aqua; color:darkblue; padding-left:1em; padding-right:1em; text-align:center;
|groupstyle = background:Aqua; color:black; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold;

"""]

def ID_To_WikiString(id):
    if id == "Infrared Vision":
        return "Infrared Vision (Mutation)|Infrared Vision"
    return id

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
                mut_trait[dict_categories[it]]['traits'].append(data[iterator]['name'])
        elif("threshreq" in data[iterator]):
            for it in data[iterator]['category']:
                mut_trait[dict_categories[it]]['threshold'].append(data[iterator]['name'])
        else:
            for it in data[iterator]['category']:
                mut_trait[dict_categories[it]]['mutations'].append(data[iterator]['name'])
    else:
        if("valid" not in data[iterator]):
            mut_neutral.append(data[iterator]['name'])
        elif("starting_trait" in data[iterator]):
            mut_neutral.append(data[iterator]['name'])

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
            output.append(ID_To_WikiString(mut_trait[list_categories[iterator]]['traits'][it]))
            output.append("]]<!--\n")
        output.append("""-->

	| group2 = Normal
	| list2  = <!--\n""")
        for it in range(0, len(mut_trait[list_categories[iterator]]['mutations'])):
            output.append("        -->")
            if it > 0:
                output.append(" {{md}}")
            output.append("[[")
            output.append(ID_To_WikiString(mut_trait[list_categories[iterator]]['mutations'][it]))
            output.append("]]<!--\n")
        output.append("""-->

	| group3 = Post-threshold
	| list3  = <!--\n""")
        for it in range(0, len(mut_trait[list_categories[iterator]]['threshold'])):
            output.append("        -->")
            if it > 0:
                output.append(" {{md}}")
            output.append("[[")
            output.append(ID_To_WikiString(mut_trait[list_categories[iterator]]['threshold'][it]))
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
    output.append(ID_To_WikiString(mut_neutral[it]))
    output.append("]]<!--\n")


output.append("""\n        -->\n}}<noinclude>
<!--Automatically generated using https://github.com/Soyweiser/CDDA-Wiki-Scripts -->
[[Category:Navigational templates]]
</noinclude>""")
    
text = "".join(output)
text.replace("\n", "\\n")
site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:Mutationtable')
page.text = text
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts mutationtable.py script')
exit()

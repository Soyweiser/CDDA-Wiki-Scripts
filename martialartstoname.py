import json
import sys
import string
import pywikibot
from version import version

#Data is automatically copied to the wiki Template:MArttoname page.
#Usage: python [location of pywikibotinstall]\pwb.py martialartstoname.py
#   Then input your password, and wait for the pages to be updated.

with open('data/json/martialarts.json') as data_file:
    data = json.load(data_file)

with open('data/json/martialarts_fictional.json') as data_file:
    data_fictional = json.load(data_file)

footer = '''
  |#default={{{1|Unknown}}}
}}</includeonly><noinclude>
Template for converting JSON [[martial arts|martial art ID's]] to their correct names.

* Source: [https://raw.github.com/CleverRaven/Cataclysm-DDA/master/data/json/martialarts.json martialarts.json]
* Source: [https://raw.github.com/CleverRaven/Cataclysm-DDA/master/data/json/martialarts_fictional.json martialarts_fictional.json]
* Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts/blob/master/martialartstoname.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.

* Usage: ''<nowiki>{{MArttoname|foo}}</nowiki>'' For example ''<nowiki>{{MArttoname|style_aikido }}</nowiki>'' outputs ''Aikido''
'''
footer+= version+"[[Category:Templates]]\n</noinclude>"

header = '''<includeonly>{{#switch:{{lc:{{{1}}}}}'''

output = [ "" ]
output.append(header)
for iterator in range(0, len(data)):
    if('type' in data[iterator]):
        if('martial_art' == data[iterator]['type']): #only add martial arts.
            output.append("\n  |")
            output.append(data[iterator]["id"].lower())
            output.append(" = ")
            output.append(data[iterator]["name"]["str"])
output.append("<!-- Fictional Martial Arts -->")
for iterator in range(0, len(data_fictional)):
    if('type' in data_fictional[iterator]):
        if('martial_art' == data_fictional[iterator]['type']): #only add martial arts.
            output.append("\n  |")
            output.append(data_fictional[iterator]["id"].lower())
            output.append(" = ")
            output.append(data_fictional[iterator]["name"]["str"])
output.append(footer)

text = "".join(output)
text.replace("\n", "\\n")
site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:MArttoname')
page.text = text
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts martialartstoname.py script')
exit()
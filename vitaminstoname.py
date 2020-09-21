import json
import sys
import string
import pywikibot
from version import version

#Data is automatically copied to the wiki Template:Vitaminstoname page.
#Usage: python [location of pywikibotinstall]\pwb.py Vitaminstoname.py
#   Then input your password, and wait for the pages to be updated.

with open('data/json/vitamin.json') as data_file:
    data = json.load(data_file)

footer = '''
  |#default={{{1|Unknown}}}
}}</includeonly><noinclude>
Template for converting JSON [[Vitamins|Vitamin ID's]] to their correct names.

* Source: [https://raw.github.com/CleverRaven/Cataclysm-DDA/master/data/json/vitamin.json vitamin.json]
* Automatically generated by [https://github.com/Soyweiser/CDDA-Wiki-Scripts/blob/master/Vitaminstoname.py script]. Any edits made to this can and will be overwritten. Please contact [[User:Soyweiser|Soyweiser]] if you want make changes to this page. Especially as any changes made here probably also means there have been changes in other pages. And there are tools to update those a little bit quicker.

* Usage: ''<nowiki>{{Vitaminstoname|foo}}</nowiki>'' For example ''<nowiki>{{Vitaminstoname|vitb}}</nowiki>'' outputs ''Vitamin B12''
'''
footer+= version+"[[Category:Templates]]\n</noinclude>"

header = '''<includeonly>{{#switch:{{lc:{{{1}}}}}'''

output = [ "" ]
output.append(header)
for iterator in range(0, len(data)):
    if('type' in data[iterator]):
        if('vitamin' == data[iterator]['type']): #only add vitamins
            output.append("\n  |")
            output.append(data[iterator]["id"].lower())
            output.append(" = ")
            output.append(data[iterator]["name"]["str"])
output.append(footer)

text = "".join(output)
text.replace("\n", "\\n")
site = pywikibot.Site('en', 'cddawiki')
page = pywikibot.Page(site, 'Template:Vitaminstoname')
page.text = text
page.save('Updated text automatically via the https://github.com/Soyweiser/CDDA-Wiki-Scripts vitaminstoname.py script')
exit()
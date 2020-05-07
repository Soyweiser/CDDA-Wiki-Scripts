# CDDA-Wiki-Scripts
Collection of scripts used to convert the Cataclysm-DDA json files to media wiki content.

CDDA main repository: https://github.com/CleverRaven/Cataclysm-DDA

CDDA Wiki: http://cddawiki.chezzo.com/cdda_wiki/index.php?title=Main_Page

Uses python 2.7

Some scripts do not directly add content to the wiki. Only converts the json files. Need to be manually copy pasted in.

Other scripts use pywikibot ( https://www.mediawiki.org/wiki/Manual:Pywikibot ) to automatically upload information to the wiki.

# Install
Get python 2.7

Copy the most recent json files into data/json

Get Microsoft Visual C++ Compiler for Python 2.7 (note to self, why? Sorry this documentation is a bit incomplete, also install Pywikibot )

Windows:

Download and install https://www.microsoft.com/en-in/download/details.aspx?id=44266
```
pip install --upgrade setuptools
pip install ez_setup
pip install requests
```
If it's still not working, maybe pip didn't install/upgrade setup_tools properly so you might want to try
```
easy_install -U setuptools
pip install --upgrade setuptools
pip install requests (again)
pip.exe install -U requests[security] 
```

Configure pywikibot:
Copy the pywikibot_config\cddawiki_family.py to [location of pywikibotinstall]\pywikibot\families

In the [location of pywikibotinstall] run `python .\pwb.py generate_user_files` setup your userfiles, and the account used by the bot to connect to the wiki.

# Documentation of scripts

## bionics.py

Data can be automatically copied to the wiki bionic pages.
Usage: python [location of pywikibotinstall]\pwb.py bionics.py
   Either input 'all' or 'ALL', and then your password, and wait for the pages to be updated.
   Or: Input a bionic ID from 'data/json/bionics.json' to get the position of that bionic in the data list.
   Or: Input an integer, which will print the generate page of that bionic on screen, and copy it to the clipboard.
Doesn't work on bionics that are not defined in 'data\json\bionics.json'

## materials.py

Data is copied to clipboard, used for the http://cddawiki.chezzo.com/cdda_wiki/index.php?title=Materials page

## monsters.py

Data is copied to clipboard, Used to create the a monster page. Does need some manual editing.

## trait.py

This script generates the individual pages for the traits/mutations. Works via command line. You need to give the index number of the trait/mutation for the text to generate. Generated text is automaticly placed in the clipboard. Use the mutation/trait id value (for example 'SHELL2') as a command line argument to get the index of that mutation.

## Automated scripts
The following scripts simply use pywikibot to upload content to the pages automatically.
- bionicsList.py -> Template:List/bionics‎‎, Template:List/faultybionics‎‎
- bionics.py -> use the 'all' command to update all the bionic pages.
- comestiblesList.py -> Template:Comestibles/food, Template:Comestibles/Drinks, Template:Comestibles/Meds, Template:Comestibles/Seeds, Template:Comestibles/Mutagen
- materialtoname.py -> Template:Materialtoname
- materialresistances.py -> Template:Matbashres, Template:Matfireres, Template:Matcutres, Template:Matelecres, Template:Matacidres
- mutationtable.py -> Template:Mutationtable
- mutationthresholds.py -> creates various Template:Mutationthresholds/[mutation category name] pages, which are then included by the various mutation category pages.
- navbar_trait.py -> Template:Navbar/traits
- navbox_enemies.py -> Template:Navbox/enemies, and various Template:Enemiestable/ pages.
- foragingList.py -> Template:ItemGroup/forage_spring, Template:ItemGroup/forage_summer, Template:ItemGroup/forage_autumn, Template:ItemGroup/forage_winter, Template:ItemGroup/trash_forest
- techniques.py -> Template:TECtoname page.
- speciestoname.py -> Template:Speciestoname
- speciesangers.py -> Template:Speciesangers
- speciesfears.py -> Template:Speciesfears

# Troubleshooting

## Pywikibot can't connect to the site. Error mentions that 'http' is not a valid protocol return value.

Seems they fixed the bug. (According to the documentation the 'http' protocol value is not allowed).

## Getting a UnicodeEncodeError crash while processing the json files.

In some rare cases people used a ’ instead of a ' or a ` this can cause some issues. You prob need to manually edit the json files and change the ’ into a '. Prob also best to make a PR to fix the wrong character in the main json files.
# CDDA-Wiki-Scripts
Collection of scripts used to convert the Cataclysm-DDA json files to media wiki content.

CDDA main repository: https://github.com/CleverRaven/Cataclysm-DDA

CDDA Wiki: http://cddawiki.chezzo.com/cdda_wiki/index.php?title=Main_Page

Uses python 2.7
Does not directly add content to the wiki. Only converts the json files. Need to be manually copy pasted in.

Install
Get python 2.7
Copy the most recent json files into data/json

Documentation of scripts

bionics.py
Data is copied to clipboard, used for the Bionics

materialresistances.py
Data is copied to clipboard, used for the Template:Matbashres, Matfireres, Matcutres, Matelecres, Matacidres, takes a command line argument, must be the json data field you are interested in. for example 'acid_resist'

materials.py
Data is copied to clipboard, used for the http://cddawiki.chezzo.com/cdda_wiki/index.php?title=Materials page

materialtoname.py
Data is copied to clipboard, used for the Template:Materialtoname

mutationtable.py
Data is copied to clipboard, used for the Template:Mutationtable

mutationthresholds.py
Data is copied to clipboard, Used to create the various lists for the threshold pages.
After executing, select the window running python again. And input a number. This creates a list of mutations copied into the clipboard. Copy and paste into the wiki. For the mapping between the input number and the page created look at the list_categories list. Start counting at zero.

navbar_trait.py
Data is copied to clipboard, used for the Template:Navbar/traits

trait.py
This script generates the individual pages for the traits/mutations. Works via command line. You need to give the index number of the trait/mutation for the text to generate. Generated text is automaticly placed in the clipboard. Use the mutation/trait id value (for example 'SHELL2') as a command line argument to get the index of that mutation.

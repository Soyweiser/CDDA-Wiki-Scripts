#the following dict is made for monster id's and specific wiki page names. For example the 'mon_dog_thing' has as a page name 'Dog (nether)', but the links are called 'dog' for spoilers sake. The second hacks is for the Template:Enemiestable pages.
monster_name_hacks = { 'mon_dog_thing' : 'Dog (nether)|Dog', 'mon_triffid_heart' : 'Triffid heart (creature)|Triffid heart' }

def monster_name(x): #checks if the id x is in the monster_name_hack list, and if it is it returns the correct hack name. If it isn't it returns the ID.
    if(x in monster_name_hacks):
        return monster_name_hacks[x]
    else:
        return x
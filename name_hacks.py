#the following dict is made for monster id's and specific wiki page names. For example the 'mon_dog_thing' has as a page name 'Dog (nether)', but the links are called 'dog' for spoilers sake. The second hacks is for the Template:Enemiestable pages.
monster_name_hacks = { 'mon_dog_thing' : 'Dog (nether)|Dog', 'mon_triffid_heart' : 'Triffid heart (creature)|Triffid heart', 'mon_breather' : 'Breather (spawn)|Breather spawn' }

#The following dict is made for mutation/trait ID's and the wiki page names. Atm it is only used to translate the various threshold mutations into subpages so they can be included into the threshold page, and for the infrared vision mutation which is an exception.
trait_name_hacks = { 'INFRARED' : 'infrared Vision (Mutation)|Infrared Vision', 'THRESH_LIZARD' : 'Lizard (threshold mutation)|Lizard', 'THRESH_BIRD' : 'Bird (threshold mutation)|Bird', 'THRESH_FISH' : 'Aquatic (threshold mutation)|Aquatic', 'THRESH_BEAST' : 'Beast (threshold mutation)|Beast', 'THRESH_FELINE' : 'Feline (threshold mutation)|Feline', 'THRESH_LUPINE' : 'Wolf (threshold mutation)|Wolf', 'THRESH_URSINE' : 'Bear (threshold mutation)|Bear', 'THRESH_CATTLE' : 'Bovine (threshold mutation)|Bovine', 'THRESH_INSECT' : 'Insect (threshold mutation)|Insect', 'THRESH_PLANT' : 'Plant (threshold mutation)|Plant', 'THRESH_SLIME' : 'Aqueous (threshold mutation)|Aqueous', 'THRESH_TROGLOBITE' : 'Subterranean (threshold mutation)|Subterranean', 'THRESH_CEPHALOPOD' : 'Cephalopod (threshold mutation)|Cephalopod', 'THRESH_SPIDER' : 'Arachnid (threshold mutation)|Arachnid', 'THRESH_RAT' : 'Survivor (threshold mutation)|Survivor', 'THRESH_MEDICAL' : 'Prototype (threshold mutation)|Prototype', 'THRESH_ALPHA' : 'Prime (threshold mutation)|Prime', 'THRESH_ELFA' : 'Fey (threshold mutation)|Fey', 'THRESH_CHIMERA' : 'Chaos (threshold mutation)|Chaos', 'THRESH_RAPTOR' : 'Raptor (threshold mutation)|Raptor', 'THRESH_MOUSE' : 'Diminutive (threshold mutation)|Diminutive' }

def monster_name(x): #checks if the id x is in the monster_name_hack list, and if it is it returns the correct hack name. If it isn't it returns the ID.
    if(x in monster_name_hacks):
        return monster_name_hacks[x]
    else:
        return x

def trait_name(x): #checks if the id x is in the trait_name_hack list, and if it is it returns the correct hack name. If it isn't it returns the ID.
    if(x in trait_name_hacks):
        return trait_name_hacks[x]
    else:
        return x

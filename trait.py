import json
from pprint import pprint
from Tkinter import Tk
root = Tk()
root.withdraw()

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
    
var = raw_input(">")
while True:
    while var.isdigit():
        var = int(var)
        if(var < 0):
            root.update()
            root.destroy()
            exit()
        list = [ "{{trait|", data[var]["id"], '|', data[var]["name"], '|' ]
        
        if("prereqs" in data[var]):
            list.append("PREREQS=")
            for it in range(0, len(data[var]["prereqs"])):
                list.append('[[')
                list.append(ID_To_String(data[var]["prereqs"][it]))
                list.append(']]<!--')
                list.append(data[var]["prereqs"][it])
                list.append('-->')
                if(not(it+1 == len(data[var]["prereqs"]))):
                    list.append(", ")
            list.append('|')
            
        if("prereqs2" in data[var]):
            list.append("PREREQS2=")
            for it in range(0, len(data[var]["prereqs2"])):
                list.append('[[')
                list.append(ID_To_String(data[var]["prereqs2"][it]))
                list.append(']]<!--')
                list.append(data[var]["prereqs2"][it])
                list.append('-->')
                if(not(it+1 == len(data[var]["prereqs2"]))):
                    list.append(", ")
            list.append('|')
        
        if("cancels" in data[var]):
            list.append("CANCELS=")
            for it in range(0, len(data[var]["cancels"])):
                list.append('[[')
                list.append(ID_To_String(data[var]["cancels"][it]))
                list.append(']]<!--')
                list.append(data[var]["cancels"][it])
                list.append('-->')
                if(it+1 < len(data[var]["cancels"])):
                    list.append(", ")
            list.append('|')
            
        if("changes_to" in data[var]):
            list.append("CHANGES_TO=")
            for it in range(0, len(data[var]["changes_to"])):
                list.append('[[')
                list.append(ID_To_String(data[var]["changes_to"][it]))
                list.append(']]<!--')
                list.append(data[var]["changes_to"][it])
                list.append('-->')
                if(not(it+1 == len(data[var]["changes_to"]))):
                    list.append(", ")
            list.append('|')
            
        if("leads_to" in data[var]):
            list.append("LEADS_TO=")
            for it in range(0, len(data[var]["leads_to"])):
                list.append('[[')
                list.append(ID_To_String(data[var]["leads_to"][it]))
                list.append(']]<!--')
                list.append(data[var]["leads_to"][it])
                list.append('-->')
                if(not(it+1 == len(data[var]["leads_to"]))):
                    list.append(", ")
            list.append('|')
            
        
        if("points" in data[var]):
            list.append(str(data[var]["points"]))
            list.append('|')
        else:
            list.append('0|')

        if("visibility" in data[var]):
            list.append(str(data[var]["visibility"]))
            list.append('|')
        else:
            list.append('0|')
        
        if("ugliness" in data[var]):
            list.append(str(data[var]["ugliness"]))
            list.append('|')
        else:
            list.append('0|')
        list.append(data[var]["description"])
        
        if( "starting_trait" in data[var]):
            list.append('|trait=1')
        
        if( "profession" in data[var]):
            list.append('|profession=1')
        
        if( "valid" in data[var]):
            list.append('|invalid=1')
        
        if( "threshreq" in data[var]):
            list.append('|threshold=1')
            
        if( "purifiable" in data[var]): #naively assuming that when set it is to not be the default value.
            list.append('|purifiable=1')
        
        if("category" in data[var]):
            if( "MUTCAT_LIZARD" in data[var]["category"] ):
                list.append('|lizard=1')
            if( "MUTCAT_BIRD" in data[var]["category"] ):
                list.append('|bird=1')
            if( "MUTCAT_FISH" in data[var]["category"] ):
                list.append('|fish=1')
            if( "MUTCAT_BEAST" in data[var]["category"] ):
                list.append('|beast=1')
            if( "MUTCAT_FELINE" in data[var]["category"] ):
                list.append('|feline=1')
            if( "MUTCAT_LUPINE" in data[var]["category"] ):
                list.append('|lupine=1')
            if( "MUTCAT_URSINE" in data[var]["category"] ):
                list.append('|ursine=1')
            if( "MUTCAT_CATTLE" in data[var]["category"] ):
                list.append('|cattle=1')
            if( "MUTCAT_INSECT" in data[var]["category"] ):
                list.append('|insect=1')
            if( "MUTCAT_PLANT" in data[var]["category"] ):
                list.append('|plant=1')
            if( "MUTCAT_SLIME" in data[var]["category"] ):
                list.append('|slime=1')
            if( "MUTCAT_TROGLOBITE" in data[var]["category"] ):
                list.append('|troglobite=1')
            if( "MUTCAT_CEPHALOPOD" in data[var]["category"] ):
                list.append('|cephalopod=1')
            if( "MUTCAT_SPIDER" in data[var]["category"] ):
                list.append('|spider=1')
            if( "MUTCAT_MEDICAL" in data[var]["category"] ):
                list.append('|medical=1')
            if( "MUTCAT_ALPHA" in data[var]["category"] ):
                list.append('|alpha=1')
            if( "MUTCAT_ELFA" in data[var]["category"] ):
                list.append('|elfa=1')
            if( "MUTCAT_CHIMERA" in data[var]["category"] ):
                list.append('|chimera=1')
            if( "MUTCAT_RAPTOR" in data[var]["category"] ):
                list.append('|raptor=1')
            if( "MUTCAT_RAT" in data[var]["category"] ):
                list.append('|rat=1')
            if( "MUTCAT_MYCUS" in data[var]["category"] ):
                list.append('|mycus=1')
            if( "MUTCAT_MARLOSS" in data[var]["category"] ):
                list.append('|marloss=1')                
            
        list.append("}}\n<noinclude>\n<!-- *YOUR PERSONAL NOTES AND HINTS GO BELOW HERE* -->\n==Notes==\n\n")
        if( "starting_trait" in data[var] ) or ( "profession" in data[var] ) :
            list.append("{{Navbar/traits}}\n")

        list.append("[[category: Mutations]]\n")
        if( "threshreq" in data[var]):
            list.append("[[category: Post-threshold mutations]]\n")
            
        list.append("{{ver|0.D}}\n</noinclude>")

        text = "".join(list)
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
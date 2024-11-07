import os
from itertools import pairwise
#python3.12 '.\scripts\!Lite scripts\script_interpreter.py'

ATK_DECLARATIONS: list[str] = ["attack_prepare", "target_expansion", "unstart_campaign", "call"]
#Types of attack declarations to check for
#TODO - sum unit supply in define_maxes

class atk_line:
    def __init__(self, order_from_top, number, unit):
        assert valid_type(int, number) and int(number) < 65, f"Error! Expected int and max 64 units, instead got {type(number)} and {number}" #max 64 units in an attack 
        self.number = number
        self.unit = unit
        self.order_from_top = order_from_top

class block_declaration:
    def __init__(self, order_from_top, block):
        self.blockname = block
        self.order_from_top = order_from_top

class constructed_attack:
    def __init__(self, entry_list, type):
        self.entry_list = entry_list
        self.type = type

def startswith_fromlist(line_to_read, list) -> bool:
    for text in list:
        if line_to_read.startswith(text):
            return True
    return False #If we end iterating without any True, return False; ie there are no lines that start with this

def easy_ask_for_script() -> str:
    scriptname = input("Please input the name of the script: ")
    if scriptname != "":
        print(f"Looking for script {scriptname.upper()}...")
        os.chdir('./scripts/!Lite scripts/')
        for filename in os.listdir('.'):
            if os.path.isfile(filename):
                try:
                    with open(filename, encoding='utf-8') as file:
                        for index, line in enumerate(file):
                            print(f"Looking at {file.name} at index {index+1}...")
                            if scriptname.upper() in line.upper() and index < 6:
                                print(f"in {file.name}, found {scriptname.upper()} in line {index+1}!")
                                return os.path.basename(file.name)
                except FileNotFoundError as e:
                    print(f"ERROR: FILE CANNOT BE FOUND! easy_ask_for_script:  {e}") # Not needed but added regardless:
                except IOError as e:
                    print(f"ERROR: CANNOT OPEN FILE! IO EXCEPTION! easy_ask_for_script:  - {e}")
    else:
        scriptname = "Protoss 1 - Zerg Town.asc3"
        print("WARNING: NO SCRIPT GIVEN: USING DEFAULT: " + scriptname)    
        return scriptname
    
    print("WARNING! CANNOT FIND SCRIPT: ERRORS MAY OCCUR: " + scriptname)
    return scriptname

def valid_type(type_to_check, variable) -> bool:
    '''Checks if a conversion is valid. If yes, return True.'''
    match type_to_check:
        case int:
            try:
                int(variable)
            except Exception as err:
                print(err)
                return False
            return True
        
def read_file(filename: str) -> list[str]:
    try:
        with open(filename, "r") as script:
            lines = script.readlines()
        return lines
    except FileNotFoundError as e:
        print(f"ERROR: FILE CANNOT BE FOUND! read_file:  {e}")
        return []
    except IOError as e:
        print(f"ERROR: CANNOT OPEN FILE! IO EXCEPTION! read_file:  - {e}")
        return []
    
def delete_identified_line(filename, identifier:str):
    lines = read_file(filename)
    if lines != []:
        try:
            with open(filename, "w") as script:
                for line in lines:
                    if identifier not in line:
                        script.write(line)
        except FileNotFoundError as e:
            print(f"ERROR: FILE CANNOT BE FOUND! delete_identified_line:  {e}")
        except IOError as e:
            print(f"ERROR: CANNOT OPEN FILE! IO EXCEPTION! delete_identified_line - {e}")
    else:
        print(f"ERROR: COULD NOT PARSE LINES ARRAY: Exiting delete_identified_line: " + filename)

def find_attacks(filename):
    lines = read_file(filename)
    if lines != []:
        attack_add_list: list = []
        attack_list: list = []
        for (index, line), (next_index, next_line) in pairwise(enumerate(lines)):
            #pairwise - return result for this iteration + peek at next and return that result
            if line.startswith("attack_add"):
                attack_line = line.split(" ")
                local_atkline = atk_line(index, attack_line[1], attack_line[2])
                attack_add_list.append(local_atkline) #0 is discarded
                if startswith_fromlist(next_line, ATK_DECLARATIONS):
                    local_attack = constructed_attack(attack_add_list, next_line)
                    attack_add_list: list = [] #reset list when one full attack is added
                    attack_list.append(local_attack)
            elif line.startswith(":"): #":" is included so that we know which blocks are we in
                current_block = block_declaration(index, line)
                attack_list.append(current_block)
        return attack_list if not len(attack_list) == 0 else attack_add_list
    else:
        print(f"ERROR: COULD NOT PARSE LINES ARRAY: Exiting find_attacks: " + filename)
    return []

def list_attacks_from(filename):
    for attack in find_attacks(scriptname):
        if type(attack) == constructed_attack:
            for attack_entry in attack.entry_list:
                print(attack_entry.number+" "+attack_entry.unit)
            print(attack.type)
        elif type(attack) == block_declaration:
            print(attack.blockname)

#Execution
scriptname = easy_ask_for_script()
list_attacks_from(scriptname)

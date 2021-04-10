# Create the TTS army defintions.

import json
import os
import sys
import subprocess
import re

def read_json(file_name) :
  with open(file_name, "r") as file:
    text = file.read()
    data = json.loads(text)
    return data

def read_army_json(army_id) :
  file_name = os.path.join("armyLists", army_id)
  return read_json(file_name)

def read_army_theme_json(army_id) :
  file_name = os.path.join("armyLists", army_id + "_thematicCategories")
  return read_json(file_name)

def troop_type_to_name(troop_type) :
  if troop_type == "WWG" :
    return "War Wagons"
  if troop_type == "CAT" :
    return "Cataphracts"
  if troop_type == "KNT" :
    return "Knights"
  if troop_type == "PAV" :
    return "Pavisiers"
  if troop_type == "ECV" :
    return "Elite Cavalary"
  if troop_type == "HBW" :
    return "Horse Bow"
  if troop_type == "ART" :
    return "Artillery"
  if troop_type == "JCV" :
    return "Javelin Cavalry"
  if troop_type == "SPR" or troop_type == "Spear" or troop_type == "Spears":
    return "Spears"
  if troop_type == "ELE" :
    return "Elephants"
  if troop_type == "WRR" or troop_type == "Warrior" or troop_type == "Warriors":
    return "Warriors"
  if troop_type == "BTX" :
    return "Battle Taxi"
  if troop_type == "BAD" :
    return "Bad Horse"
  if troop_type == "WBD" or troop_type == "Warband":
    return "Warband"
  if troop_type == "ARC" or troop_type == "Archer" or troop_type == "Archers":
    return "Archers"
  if troop_type == "RDR" or troop_type == "Raider" or troop_type == "Raiders":
    return "Raiders"
  if troop_type == "BLV" :
    return "Bow Levy"
  if troop_type == "RBL" :
    return "Rabble"
  if troop_type == "HRD" :
    return "Horde"
  if troop_type == "SKM" or troop_type == "Skirmisher" or troop_type == "Skirmishers" :
    return "Skirmishers"
  if troop_type == "CHT" :
    return "Chariots"
  if troop_type == "LFT" or troop_type == "Light Foot" :
    return "Light Foot"
  if troop_type == "HFT" or troop_type == "Heavy Foot" :
    return "Heavy Foot"
  if troop_type == "EFT" or troop_type == "Elite Foot" :
    return "Elite Foot"
  if troop_type == "PIK" or troop_type == "Pike" or troop_type == "Pikes":
    return "Pikes"
  if troop_type == "LSP" or troop_type == "Light Spear" or troop_type == "Light Spears" :
    return 'Light Spear'
  if troop_type == "Camp" :
    return 'Camp'
  raise Exception("troop_type not understood: " + troop_type)

def get_points_for_troop_type(troop_type) :
  if troop_type == "WWG" or troop_type == "War Wagons":
    return 3
  if troop_type == "CAT" or troop_type ==  "Cataphracts":
    return 4
  if troop_type == "KNT" or troop_type == "Knights":
    return 4
  if troop_type == "PAV" or troop_type == "Pavisiers" :
    return 4
  if troop_type == "ECV" or troop_type ==  "Elite Cavalary":
    return 4
  if troop_type == "HBW" or troop_type ==  "Horse Bow":
    return 4
  if troop_type == "ART" or troop_type ==  "Artillery":
    return 3
  if troop_type == "JCV" or troop_type ==  "Javelin Cavalry":
    return 4
  if troop_type == "SPR" or troop_type ==  "Spears" or troop_type == "Spear":
    return 4
  if troop_type == "ELE" or troop_type ==  "Elephants":
    return 4
  if troop_type == "WRR" or troop_type ==  "Warriors" or  troop_type ==  "Warrior":
    return 3
  if troop_type == "BTX" or troop_type ==  "Battle Taxi":
    return 3
  if troop_type == "BAD" or troop_type ==  "Bad Horse":
    return 3
  if troop_type == "WBD" or troop_type ==  "Warband":
    return 3
  if troop_type == "ARC" or troop_type ==  "Archers" or troop_type ==  "Archer":
    return 4
  if troop_type == "RDR" or troop_type == "Raiders" or troop_type == "Raider":
    return 4
  if troop_type == "BLV" or troop_type ==  "Bow Levy":
    return 2
  if troop_type == "RBL" or troop_type ==  "Rabble":
    return 2
  if troop_type == "HRD" or troop_type ==  "Horde":
    return 2
  if troop_type == "SKM" or troop_type ==  "Skirmisher" or troop_type ==  "Skirmishers":
    return 3
  if troop_type == "CHT" or troop_type ==  "Chariots":
    return 4
  if troop_type == "LFT" or troop_type ==  "Light Foot":
    return 3
  if troop_type == "HFT" or troop_type ==  "Heavy Foot":
    return 3
  if troop_type == "EFT" or troop_type ==  "Elite Foot":
    return 4
  if troop_type == "PIK" or troop_type ==  "Pikes" or troop_type == "Pike":
    return 3
  if troop_type == "LSP" or troop_type ==  'Light Spear':
    return 3
  raise Exception("troop_type not understood: " + str(troop_type))

def get_dismounting_type(base_definition, battle_card_note) :
  # DD  only 1477 AD: as Elite Foot
  # DD  1328-1515 AD: as Elite Foot
  # DD  1335-1399 AD: as Archer
  # DD  1362-1419 AD: as Elite Foot
  # DD  639-843 AD, as Heavy Foot
  # DD  as Archer
  # DD  as Elite Foot
  # DD  as Heavy Foot
  # DD  as Light Foot
  # DD  as Pike
  # DD  as Raider
  # DD  as Spear
  # DD  as Warrior
  r=re.compile("^(((only )|(\\d*-))\\d* AD[:,] *)?as *(?P<troop_type>.*)")
  m = r.match(battle_card_note)
  if m is not None :
    dismount =  m.group('troop_type')
    if dismount == "Pike" :
      dismount = "Pikes"
    elif dismount == "Spear" :
      dismount = "Spears"
    return dismount
  else:
    print("Unable to decode battle card note ", battle_card_note)
    assert False


def write_deployment_dismounting_as(file, base_definition, dismount_type, battle_card) :
  """
  @return list of base defintions for mounted and dismounted.
  """
  assert dismount_type is not None
  mounted = base_definition.copy()
  dismounted = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    mounted["min"] = battle_card["min"]
    dismounted["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    mounted["max"] = battle_card["max"]
    dismounted["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    mounted["max"] = 1
    dismounted["max"] = 1

  mounted['id'] += "_mounted"
  dismounted['id'] += "_dismounted"

  dismounted['troop_type'] = troop_type_to_name(dismount_type)
  dismounted['name'] = troop_type_to_name(dismount_type)
  if 'general' in dismounted:
    dismounted['name'] = troop_type_to_name(dismounted['name']) + " General"


  # Calculate the points for being able to dismount 
  mounted_points = get_points_for_troop_type(base_definition['troop_type'])
  dismounted_points = get_points_for_troop_type(dismount_type)
  points = max(mounted_points, dismounted_points) + 0.5
  mounted['points'] = points
  dismounted['points'] = points

  if 'description' not in mounted :
    mounted['description'] = ""
  else:   
    mounted['description'] += "\\n"
  
  if 'description' not in dismounted :
    dismounted['description'] = ""
  else:
    dismounted['description'] += "\\n"
  
  mounted['description'] += "Deployment dismounting as " + dismount_type
  dismounted['description'] += "Deployment dismounted from " + mounted['name']

  write_base_definition(file, dismounted) 
  file.write("g_%s=g_base_definitions[g_str_%s]\n" % (dismounted['id'], dismounted['id']))
  mounted['dismount_as'] = ("g_" + dismounted['id'])
  write_base_definition(file, mounted) 

  return (mounted, dismounted)

def write_deployment_dismounting(file, base_definition, battle_card) :
  note = battle_card['note']
  dismount_type = get_dismounting_type(base_definition, note)
  return write_deployment_dismounting_as(file, base_definition, dismount_type, battle_card)

def write_mid_battle_dismounting_as(file, base_definition, dismount_type, battle_card) :
  """
  @return list of base defintions for mounted and dismounted.
  """
  assert dismount_type is not None
  mounted = base_definition.copy()
  dismounted = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    mounted["min"] = battle_card["min"]
    dismounted["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    mounted["max"] = battle_card["max"]
    dismounted["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    mounted["max"] = 1
    dismounted["max"] = 1

  mounted['id'] += "_mounted"
  dismounted['id'] += "_dismounted"

  dismounted['troop_type'] = troop_type_to_name(dismount_type)
  dismounted['name'] = troop_type_to_name(dismount_type)
  if 'general' in dismounted:
    dismounted['name'] = troop_type_to_name(dismounted['name']) + " General"

  if 'description' not in mounted :
    mounted['description'] = ""
  else:   
    mounted['description'] += "\\n"
  
  if 'description' not in dismounted :
    dismounted['description'] = ""
  else:
    dismounted['description'] += "\\n"
  
  mounted['description'] += "Mid-battle dismounting as " + dismount_type
  dismounted['description'] += "Mid-battle dismounted from " + mounted['name']

  write_base_definition(file, dismounted) 
  file.write("g_%s=g_base_definitions[g_str_%s]\n" % (dismounted['id'], dismounted['id']))
  mounted['dismount_as'] = ("g_" + dismounted['id'])
  write_base_definition(file, mounted) 

  return (mounted, dismounted)


def write_mid_battle_dismounting(file, base_definition, battle_card) :
  note = battle_card['note']
  if note is None:
    # Feudal German Kings or Emperors is missing dismount type
    return []
  else:  
    dismount_type = get_dismounting_type(base_definition, note)
    return write_mid_battle_dismounting_as(file, base_definition, dismount_type, battle_card)

def write_mobile_infantry(file, base_definition, battle_card):
  """
     @param file Open file to write the definitions to.
     @param base_definition Defintinition of the base the battle card is being applied to.
     @param battle_card Battle card being applied.
     @return the extra base definitions for the mounted and dismounted infantry.
  """
  mounted = base_definition.copy()
  dismounted = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    mounted["min"] = battle_card["min"]
    dismounted["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    mounted["max"] = battle_card["max"]
    dismounted["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    mounted["max"] = 1
    dismounted["max"] = 1

  mounted['id'] = mounted['id'] + "_mounted_mobile_infantry"
  dismounted['id'] = dismounted['id'] + "_dismounted_mobile_infantry"

  if 'description' not in mounted :
    mounted['description'] = ""
  else:
    mounted['description'] += "\\n"
  if 'description' not in dismounted :
    dismounted['description'] = ""
  else:
    dismounted['description'] += "\\n"
  dismounted['description'] += "Dismounted mobile infantry"
  mounted['description'] += "mounted mobile infantry"

  mounted['dismount_as'] = ("g_" + dismounted['id'])
  mounted['mobile_infantry'] = True


  write_base_definition(file, mounted) 
  write_base_definition(file, dismounted) 
  return [ mounted, dismounted]


def write_armored_camelry(file, base_definition, battle_card) :
  camels = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    camels["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    camels["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    camels["max"] = 1

  camels['id'] = camels['id'] + "_armored_camelry"

  if 'description' not in camels :
    camels['description'] = ""
  else:
    camels['description'] += "\\n"
  camels['description'] += "Armored Camelry"

  camels['armored_camelry'] = True
  write_base_definition(file, camels) 
  return [ camels ]


def write_light_camelry(file, base_definition, battle_card) :
  camels = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    camels["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    camels["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    camels["max"] = 1

  camels['id'] = camels['id'] + "_light_camelry"

  if 'description' not in camels :
    camels['description'] = ""
  else:
    camels['description'] += "\\n"
  camels['description'] += "Light Camelry"

  camels['light_camelry'] = True
  write_base_definition(file, camels) 
  return [ camels ]


def write_charging_camelry(file, base_definition, battle_card) :
  camels = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    camels["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    camels["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    camels["max"] = 1

  camels['id'] = camels['id'] + "_charging_camelry"

  if 'description' not in camels :
    camels['description'] = ""
  else:
    camels['description'] += "\\n"
  camels['description'] += "Charging Camelry"

  camels['charging_camelry'] = True
  write_base_definition(file, camels) 
  return [ camels ]

def write_elephant_screen(file, base_definition, battle_card) :
  elephants = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    elephants["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    elephants["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    elephants["max"] = 1

  elephants['id'] = elephants['id'] + "_elephant_screen"

  if 'description' not in elephants :
    elephants['description'] = ""
  else:
    elephants['description'] += "\\n"
  elephants['description'] += "Elephant Screen"

  elephants['elephant_screen'] = True
  write_base_definition(file, elephants) 
  return [ elephants ]

def write_plaustrella(file, base_definition, battle_card) :
  plaustrella = base_definition.copy()

  if ("min" in battle_card)  and (battle_card["min"] is not None):
    plaustrella["min"] = battle_card["min"]
  if ("max" in battle_card)  and (battle_card["max"] is not None):
    plaustrella["max"] = battle_card["max"]
  if ('general' in base_definition) and (base_definition['general'] == True) :
    plaustrella["max"] = 1

  plaustrella['id'] = plaustrella['id'] + "_plaustrella"

  if 'description' not in plaustrella :
    elephaplaustrellants['description'] = ""
  else:
    plaustrella['description'] += "\\n"
  plaustrella['description'] += "Plaustrella"

  plaustrella['plaustrella'] = True
  write_base_definition(file, plaustrella) 
  return [ plaustrella ]


def write_fortified_camp(file, camp_definition, battle_card) :
  fort = camp_definition.copy()

  fort['id'] = fort['id'] + "_fortified"

  fort['fortified_camp'] = True
  write_base_definition(file, fort) 
  return [ fort ]

def write_pack_train_and_herds(file, camp_definition, battle_card) :
  pack_train = camp_definition.copy()

  pack_train['id'] = pack_train['id'] + "_pack_train"

  pack_train['pack_train'] = True
  pack_train['description'] = "Pack Train"
  write_base_definition(file, pack_train) 
  return [ pack_train ]

def write_standard_wagon(file, camp_definition, battle_card) :
  wagon = camp_definition.copy()

  wagon['id'] = wagon['id'] + "_standard_wagon"

  wagon['standard_wagon'] = True
  wagon['description'] = "Standard Wagon"
  write_base_definition(file, wagon) 
  return [ wagon ]

def create_base_definition(troop_option, troop_entry) :
  min = troop_option['min']
  max = troop_option['max']

  id = troop_entry['_id']
  if id == '5fb1ba37e1af06001770e72d' :
    description = "German or Polish men-at-arms"
  elif id ==  "5fb1ba37e1af06001770e72e" :
    description = "Lithuanian horsemen"
  else :
    description = troop_option['description']
  

  troop_type = troop_entry['troopTypeCode']
  name = troop_type_to_name(troop_type)

  troop_option_id = troop_option['_id']

  base_definition = {
    'id': id, 'name':name, 'troop_type':troop_type, 
    'min':min, 'max':max, 
    'description':description,
    'troop_option_id': troop_option_id }

  return base_definition


def write_base_definition(file, base_definition) :
  if 'description' not in base_definition:
    description = ""
  else:
    #escape quotes
    description = base_definition['description']
    description = description.replace("'", "\\'")

  id = base_definition['id']
  file.write("g_str_%s='%s'\n" % (id,id))

  file.write("g_base_definitions[g_str_%s]={\n" % (id))
  file.write("  id=g_str_%s,\n" % (id))
  file.write("  name='%s',\n" % (base_definition['name']))
  file.write("  min=%d,\n" % (base_definition['min']))
  file.write("  max=%d,\n" % (base_definition['max']))
  file.write("  description='%s',\n" % (description))
  if 'points' in base_definition :
    file.write("  points=%d,\n" % (base_definition['points']))
  if 'dismount_as' in base_definition :
    file.write("  dismount_as=%s,\n" % (base_definition['dismount_as']))
  for k in ['general', 'mobile_infantry', 'armored_camelry', 'light_camelry', 'elephant_screen',
    'plaustrella',
    'fortifed_camp', 'pack_train', 'standard_wagon'] :
    if k in base_definition  and base_definition[k] == True :
      file.write("  %s=true,\n" % (k))
  troop_type_name = troop_type_to_name( base_definition['troop_type'])
  file.write("  troop_type=\"%s\",\n" %(troop_type_name))
  if 'troop_option_id' in base_definition :
    troop_option_id = base_definition['troop_option_id']
    file.write("  troop_option_id=\"%s\",\n" %(troop_option_id))
  file.write("}\n")

def get_general_troop_type_codes(army) :
  codes = {}
  for troop_entry_for_general in army['troopEntriesForGeneral'] :
    for troop_entry in troop_entry_for_general['troopEntries'] :
      troop_type = troop_entry['troopTypeCode']
      codes[troop_type] = 1
  return codes


def write_battle_cards(file, army, troop_option, troop_entry, base_definition)  :
  """Return the base definitions of the bases created due to battle cards."""
  result = []
  write_base_definition(file, base_definition)
  for battle_card in troop_entry['battleCardEntries'] :
    code = battle_card['battleCardCode']
    note = battle_card['note']
    if code == "DD" :        
      id = troop_entry['_id']
      if id == '5fb1ba37e1af06001770e72d' :
        # "German or Polish men-at-arms"
        extra = write_deployment_dismounting_as(file, base_definition, "Elite Foot", battle_card)
        result.extend(extra)
      elif id ==  "5fb1ba37e1af06001770e72e" :
        #"Lithuanian horsemen"
        extra = write_deployment_dismounting_as(file, base_definition, "Archers", battle_card)
        result.extend(extra)
      elif battle_card['_id'] == "5fb1ba34e1af06001770e1a0" :
        extra = write_deployment_dismounting_as(file, base_definition, "Pikes", battle_card)
        result.extend(extra)
      else:
        extra = write_deployment_dismounting(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "MD" :
        extra = write_mid_battle_dismounting(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "MI" :
        extra = write_mobile_infantry(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "AC" :
        extra = write_armored_camelry(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "LC" :
        extra = write_light_camelry(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "CC" :
        extra = write_charging_camelry(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "ET" :
        extra = write_elephant_screen(file, base_definition, battle_card)
        result.extend(extra)
    elif code == "PL" :
        extra = write_plaustrella(file, base_definition, battle_card)
        result.extend(extra)
    else:
      pass
#      print("Unknown battle card ", code)

  return result


def base_definitions(file, army, troop_option) :
  """
    @return List of base definitions
  """
  result = []
  generals = get_general_troop_type_codes(army)

  for troop_entry in troop_option['troopEntries'] :
    # Push down the battle cards 
    troop_entry['battleCardEntries'] = troop_option['battleCardEntries']

    if troop_entry['troopTypeCode'] in generals :
      base_definition = create_base_definition(troop_option, troop_entry)    
      base_definition['max'] = 1
      base_definition['general'] = True
      base_definition['name'] = base_definition['name'] + " General"
      base_definition['id'] = base_definition['id'] + "_general"
      result.append(base_definition)
      extra = write_battle_cards(file, army, troop_option, troop_entry, base_definition)
      result.extend(extra)
    
    base_definition = create_base_definition(troop_option, troop_entry)    
    result.append(base_definition)
    extra = write_battle_cards(file, army, troop_option, troop_entry, base_definition)
    result.extend(extra)


  return result

# Return the ID for the troop entry that matches the troop
# type.  None is returned if there is no existing unit
# that the general can be part of.
def find_troop_entry_for_troop_type(army_json, troop_type) :
  troop_options = army_json['troopOptions']
  for troop_option in  troop_options :
    for troop_entry in troop_option['troopEntries'] :
      if troop_entry['troopTypeCode'] == troop_type :
        return troop_entry['_id']
  return None


# Write out the base definition for a camp
def write_camp(file, army_id) :
  camp_def = {
    'id' : army_id + "_camp",
    'name' : 'Camp',
    'troop_type' : 'Camp',
    'min': 0,
    'max': 1,
    'description': 'Camp'
  }
  write_base_definition(file, camp_def)
  return [camp_def]

# Generate the LUA for an army
# @param army_id Identifier for the army in Meshwesh
def generate_army(army_id) :
  army_json = read_army_json(army_id)
  army_theme_json = read_army_theme_json(army_id)
  file_name = os.path.join("army_data", army_id + ".ttslua")
  with open(file_name, "w") as file :

    army_name =  army_json['derivedData']['extendedName']
    file.write("-- %s %s\n\n" % (army_id, army_name))
    file.write("if g_base_definitions == nil then\n")
    file.write("  g_base_definitions = {}\n")
    file.write("end\n")
    file.write("if army == nil then\n")
    file.write("  army = {}\n")
    file.write("end\n")

    definitions = []

    troop_options = army_json['troopOptions']
    for troop_option in  troop_options :
      defs = base_definitions(file, army_json, troop_option)
      definitions.extend(defs)

    camp_definitions = write_camp(file, army_id)
    definitions.extend(camp_definitions)
    if 'battleCardEntries' in army_json :
      for camp_definition in camp_definitions :
        for battle_card in army_json['battleCardEntries'] :
          if battle_card['battleCardCode'] == "FC" :
            extra = write_fortified_camp(file, camp_definition, battle_card)
            definitions.extend(extra)
          elif battle_card['battleCardCode'] == "PT" :
            extra = write_pack_train_and_herds(file, camp_definition, battle_card)
            definitions.extend(extra)
          elif battle_card['battleCardCode'] == "SW" :
            extra = write_standard_wagon(file, camp_definition, battle_card)
            definitions.extend(extra)


    file.write("army['%s']={\n" % (army_id))
    file.write("  data={\n")
    # TODO Invasion
    # TODO maneuver
    # TODO terrain
    # TODO list

    #escape quotes
    name = army_name.replace("'", "\\'")

    file.write("    name='%s'\n" %(name))
    file.write("  },\n")

    # Bases that make up the army
    for definition in definitions  :
      id = definition['id']
      file.write("  g_base_definitions[g_str_%s],\n" %(id))
    file.write("}\n")

    # Meshwesh is in front so it will be the first entry in the 
    # dialog otherwise it will be the second which just looks weird.
    file.write('if nil == armies[\"Meshwesh id\"] then\n')
    file.write('  armies[\"Meshwesh id\"] ={}\n')
    file.write('end\n')
    file.write('armies[\"Meshwesh id\"][\"%s\"] = army[\"%s\"]\n' % 
      (army_id, army_id))


    for army_theme in army_theme_json :
      theme_name = army_theme["name"]

      file.write('if nil == armies[\"%s\"] then\n' % 
        (theme_name))
      file.write('  armies[\"%s\"] ={}\n' % 
        (theme_name))
      file.write('end\n')
      file.write('armies[\"%s\"][\"%s\"] = army[\"%s\"]\n' % 
        (theme_name, name, army_id))
summary = read_json("armyLists/summary")

with open("army_data/all_armies.ttslua", "w") as all_armies:
  for army_entry in summary :
    army_id = army_entry['id']
    print(army_id)
    try :
      generate_army(army_id)
    except:
      print(army_entry['name'])
      raise
    all_armies.write( "#include %s\n" % (army_id))

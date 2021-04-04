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
  if troop_type == "SPR" :
    return "Spears"
  if troop_type == "ELE" :
    return "Elephants"
  if troop_type == "WRR" :
    return "Warriors"
  if troop_type == "BTX" :
    return "Battle Taxi"
  if troop_type == "BAD" :
    return "Bad Horse"
  if troop_type == "WBD" :
    return "Warband"
  if troop_type == "ARC" :
    return "Archers"
  if troop_type == "RDR" :
    return "Raiders"
  if troop_type == "BLV" :
    return "Bow Levy"
  if troop_type == "RBL" :
    return "Rabble"
  if troop_type == "HRD" :
    return "Horde"
  if troop_type == "SKM" :
    return "Skirmishers"
  if troop_type == "CHT" :
    return "Chariots"
  if troop_type == "LFT" :
    return "Light Foot"
  if troop_type == "HFT" :
    return "Heavy Foot"
  if troop_type == "EFT" :
    return "Elite Foot"
  if troop_type == "PIK" :
    return "Pikes"
  if troop_type == "LSP" :
    return 'Light Spear'
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
  if troop_type == "SKM" or troop_type ==  "Skirmishers":
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
    print("DD Unable to decode battle card note ", battle_card_note)
    assert False


def write_deployment_dismounting_as(file, base_definition, dismount_type) :
  """
  @return list of base defintions for mounted and dismounted.
  """
  assert dismount_type is not None
  mounted = base_definition.copy()
  dismounted = base_definition.copy()

  mounted['id'] += "_mounted"
  dismounted['id'] += "_dismounted"

  dismounted['troop_type'] = dismount_type
  dismounted['name'] = dismount_type

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
  return write_deployment_dismounting_as(file, base_definition, dismount_type)

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

  name = troop_type_to_name(troop_type)
  base_definition = {
    'id': id, 'name':name, 'troop_type':troop_type, 
    'min':min, 'max':max, 
    'description':description }

  return base_definition


def write_base_definition(file, base_definition) :
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
        extra = write_deployment_dismounting_as(file, base_definition, "Elite Foot")
        result.extend(extra)
      elif id ==  "5fb1ba37e1af06001770e72e" :
        #"Lithuanian horsemen"
        extra = write_deployment_dismounting_as(file, base_definition, "Archers")
        result.extend(extra)
      elif note == "General only; as Pike" :
        # TODO
        pass
      else:
        extra = write_deployment_dismounting(file, base_definition, battle_card)
        result.extend(extra)
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
      generals.pop( troop_entry['troopTypeCode'] )
      base_definition = create_base_definition(troop_option, troop_entry)    
      base_definition['max'] = 1
      base_definition['general'] = True
      base_definition['name'] = base_definition['name'] + " General"
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
def camp(file, army_id) :
  var = army_id + "_camp"
  file.write("g_str_%s='%s'\n" % (var,var))
  file.write("g_base_definitions[g_str_%s]={\n" % (var))
  file.write("  name='Camp',\n")
  file.write("  id=g_str_%s,\n" % (var))
  file.write("  min=1,\n")
  file.write("  max=1,\n")
  file.write("}\n")
  return [ var ]

# Generate the LUA for an army
# @param army_id Identifier for the army in Meshwesh
def generate_army(army_id) :
  army_json = read_army_json(army_id)
  army_theme_json = read_army_theme_json(army_id)
  file_name = os.path.join("army_data", army_id + ".ttslua")
  with open(file_name, "w") as army_data :

    army_name =  army_json['derivedData']['extendedName']
    army_data.write("-- %s %s\n\n" % (army_id, army_name))
    army_data.write("if g_base_definitions == nil then\n")
    army_data.write("  g_base_definitions = {}\n")
    army_data.write("end\n")
    army_data.write("if army == nil then\n")
    army_data.write("  army = {}\n")
    army_data.write("end\n")

    definitions = []

    troop_options = army_json['troopOptions']
    for troop_option in  troop_options :
      defs = base_definitions(army_data, army_json, troop_option)
      definitions.extend(defs)
    camp(army_data, army_id)


    army_data.write("army['%s']={\n" % (army_id))
    army_data.write("  data={\n")
    # TODO Invasion
    # TODO maneuver
    # TODO terrain
    # TODO list

    #escape quotes
    name = army_name.replace("'", "\\'")

    army_data.write("    name='%s'\n" %(name))
    army_data.write("  },\n")

    # Bases that make up the army
    army_data.write("  g_base_definitions[g_str_%s_camp],\n" %(army_id))
    for troop_entry_for_general in army_json['troopEntriesForGeneral'] :
      for troop_entry in troop_entry_for_general['troopEntries'] :
        troop_type = troop_entry['troopTypeCode']
        id = troop_entry['_id']
        army_data.write("  g_base_definitions[g_str_%s],\n" %(id))
    for definition in definitions  :
      id = definition['id']
      army_data.write("  g_base_definitions[g_str_%s],\n" %(id))
    army_data.write("}\n")

    # Meshwesh is in front so it will be the first entry in the 
    # dialog otherwise it will be the second which just looks weird.
    army_data.write('if nil == armies[\"Meshwesh id\"] then\n')
    army_data.write('  armies[\"Meshwesh id\"] ={}\n')
    army_data.write('end\n')
    army_data.write('armies[\"Meshwesh id\"][\"%s\"] = army[\"%s\"]\n' % 
      (army_id, army_id))


    for army_theme in army_theme_json :
      theme_name = army_theme["name"]

      army_data.write('if nil == armies[\"%s\"] then\n' % 
        (theme_name))
      army_data.write('  armies[\"%s\"] ={}\n' % 
        (theme_name))
      army_data.write('end\n')
      army_data.write('armies[\"%s\"][\"%s\"] = army[\"%s\"]\n' % 
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

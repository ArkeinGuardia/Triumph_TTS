# Create the TTS army defintions.

import json
import os
import sys
import subprocess

def read_json(file_name) :
  with open(file_name, "r") as file:
    text = file.read()
    data = json.loads(text)
    return data

def read_army_json(army_id) :
  file_name = os.path.join("armyLists", army_id)
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
  
def base_definition(file, troop_option, troop_entry) :
  min = troop_option['min']
  max = troop_option['max']

  description = troop_option['description']
  #escape quotes
  description = description.replace("'", "\\'")

  id = troop_entry['_id']
  file.write("g_str_%s='%s'\n" % (id,id))

  troop_type = troop_entry['troopTypeCode']
  name = troop_type_to_name(troop_type)
  # TODO dismount
  # TODO note

  name = troop_type_to_name(troop_type)
  file.write("g_base_definitions[g_str_%s]={\n" % (id))
  file.write("  id=g_str_%s,\n" % (id))
  file.write("  name='%s',\n" % (name))
  file.write("  min=%d,\n" % (min))
  file.write("  max=%d,\n" % (max))
  file.write("  description='%s',\n" % (description))
  file.write("}\n")

def base_definitions(file, troop_option) :
  for troop_entry in troop_option['troopEntries'] :
    base_definition(file, troop_option, troop_entry)
  pass

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

# Write out the base defintions for the general
# @param file File to write to
# @param army Army we are generating the base definitions for
def generals(file, army) :
  for troop_entry_for_general in army['troopEntriesForGeneral'] :
    for troop_entry in troop_entry_for_general['troopEntries'] :
      troop_type = troop_entry['troopTypeCode']
      name = troop_type_to_name(troop_type) + " General"
      # TODO dismount
      # TODO note
      id = troop_entry['_id']
      file.write("g_str_%s='%s'\n" % (id,id))
      file.write("g_base_definitions[g_str_%s]={\n" % (id))
      file.write("  name='%s',\n" % (name))
      file.write("  id=g_str_%s,\n" % (id))
      file.write("  min=1,\n")
      file.write("  max=1,\n")
      file.write("}\n")

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

    troop_options = army_json['troopOptions']
    for troop_option in  troop_options :
      base_definitions(army_data, troop_option)
    generals(army_data, army_json)
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
    for troop_option in  troop_options :
     for troop_entry in troop_option['troopEntries'] :
      id = troop_entry['_id']
      army_data.write("  g_base_definitions[g_str_%s],\n" %(id))
    army_data.write("}\n")


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

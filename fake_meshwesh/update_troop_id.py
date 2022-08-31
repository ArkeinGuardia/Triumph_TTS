#!/usr/bin/env python3

"""
Create a sed script that will change the troop identifiers when MeshWesh is updated.

1. Rename armyLists to armyLists.old
2. Get new MeshWesh data:
2.1 make clone
2.2 make army_data
3. Run this script to get changes.sed
4. Update the scripts data files
4.1 cd scripts/data
4.2 for f in *; do; sed -i -f ../../changes.sed $f; done
"""
import json
import os
import sqlite3


def is_army(file_name):
    if file_name.endswith(".json") :
        return False
    if file_name.endswith("_thematicCategories") :
        return False
    if file_name.endswith("summary") :
        return False
    return True

def import_files(army_data_dir, data_version):    
    files = os.listdir(army_data_dir)
    for file in files:
        if is_army(file) :
            file_path = os.path.join(army_data_dir, file)
            with open(file_path, "r") as json_file:
                s = json_file.readline()
                j = json.loads(s)
                army_id = file
                troop_options = j["troopOptions"]
                for troop_option in troop_options:
                    troop_option_id = troop_option["_id"]
                    troop_option_description = troop_option['description']
                    troop_entries = troop_option["troopEntries"]
                    for troop_entry in troop_entries:
                        troop_entry_id = troop_entry["_id"]
                        troop_entry_type_code = troop_entry["troopTypeCode"]
                        con.execute("INSERT INTO troops (army_id, troop_option_id, troop_option_description, troop_entry_id, troop_entry_type_code, data_version) VALUES (?,?,?,?,?,?)",
                            (army_id, troop_option_id, troop_option_description, troop_entry_id, troop_entry_type_code, data_version))


if os.path.exists("troops.db"):
    os.unlink("troops.db")
con = sqlite3.connect("troops.db")
con.execute("""create table troops (
    army_id TEXT,
    troop_option_id TEXT,
    troop_option_description TEXT,
    troop_entry_id TEXT,
    troop_entry_type_code TEXT,
    data_version TEXT
    );""")

import_files("c:/Users/marcp/GitHub/Triumph_TTS/fake_meshwesh/armyLists.old", "old")
import_files("c:/Users/marcp/GitHub/Triumph_TTS/fake_meshwesh/armyLists", "new")
changes = open("c:/Users/marcp/GitHub/Triumph_TTS/fake_meshwesh/changes.sed", "w")

cur = con.cursor()
cur.execute("""
    SELECT A.troop_entry_id, B.troop_entry_id 
    FROM troops A, troops B 
    WHERE 
        A.data_version == 'old' AND 
        B.data_version == 'new' AND 
        A.army_id == B.army_id AND 
        A.troop_option_description == B.troop_option_description AND 
        A.troop_entry_type_code == B.troop_entry_type_code""")
while (rec := cur.fetchone()) :
    (old,new) = rec
    line = f"s/{old}/{new}/g\n"
    changes.write(line)
changes.close()


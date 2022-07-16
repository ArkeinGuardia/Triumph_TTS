#!/usr/bin/python3

# Create the Mobile Infrantry tiles

import subprocess

infantry = [
  "archers",
  "bowlevy",
  "elitefoot",
  "heavyfoot",
  "horde",
  "lightfoot",
  "lightspear",
  "pavasiers",
  "pike",
  "plaustrella",
  "rabble",
  "raiders",
  "skirmishers",
  "spear",
  "warband",
  "warriors", ]

for color in ['red', 'blue']:
    for foot in infantry:
        cmd = [ 'convert', f'mi_{color}.png', f"{foot}.png",  '-composite', f"{foot}_mi_{color}.png" ] 
        print(cmd)
        subprocess.check_call(cmd)

#!/usr/bin/python3

# Convert all the production lua files to a single file

import os

def flatten(file) :
  with open(file, "r") as f :
      dir = os.path.dirname(file)
      line = "  "
      while line != "" :
          line = f.readline()
          if line.startswith("#include ") :
              print("-- ", line)
              (command,include) = line.split()              
              flatten(os.path.join(dir,include+".ttslua"))
          else:
              print(line.rstrip())  

flatten("../main.ttslua")
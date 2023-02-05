#!/usr/bin/env python3

import json
import libxml2
import pathlib
import sys


text_bottom_margin = 15 - 13.857281
icon_bottom_margin = 15 - 9.5093451

def get_color_code(color):
    if color == "red":
        return "#b52327"
    if color == "blue":
        return "#235db5"
    raise Exception("Unexpected color")

def change_fill(elem, color:str):
    color_code = get_color_code(color)
    style = elem.prop("style")
    new_style = ""
    for part in style.split(";"):
        name,value = part.split(":")
        if name != "fill":
            new_style = new_style + name + ":" + value + ";"
        else:
            new_style = new_style + name + ":" + color_code + ";"
    new_style = new_style[:-1]
    elem.setProp("style", new_style)

def make_svg(color:str, general: bool, troop_name: str, troop_data: dict):
    if general:
        general_file_name = "_general"
    else:
        general_file_name = ""
    svg_file_name = (f"{color}_{troop_name}{general_file_name}.svg").lower().replace(' ','_')
    icon_file_name = f"../icons/{troop_name.lower().replace(' ','_')}.png"
    icon_path = pathlib.Path(icon_file_name)
    if not icon_path.exists():
        raise Exception("Icon missing: " + icon_file_name)
    doc = libxml2.parseFile("drawing.svg")
    ctxt = doc.xpathNewContext()
    ctxt.xpathRegisterNs("svg", "http://www.w3.org/2000/svg")
    ctxt.xpathRegisterNs("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
    ctxt.xpathRegisterNs("inkscape", "http://www.inkscape.org/namespaces/inkscape")
    ctxt.xpathRegisterNs("xmlns:xlink", "http://www.w3.org/1999/xlink")
    res = ctxt.xpathEval("/svg:svg")
    svg = res[0]
    svg.setProp("height", f"{troop_data['base_depth']}mm")
    svg.setProp("viewBox", f"0 0 40 {troop_data['base_depth']}")
    svg.setProp("sodipodi:docname", svg_file_name)
    
    res = ctxt.xpathEval("//svg:rect[@inkscape:label='background']")
    rect = res[0]
    rect.setProp("height", str(troop_data['base_depth']))
    change_fill(rect, color)

    res = ctxt.xpathEval("//svg:rect[@inkscape:label='general outside']")
    rect = res[0]
    if general:
        rect.setProp("height", str(troop_data['base_depth']))
    else:
        rect.unlinkNode()

    res = ctxt.xpathEval("//svg:rect[@inkscape:label='general inside']")
    rect = res[0]
    if general:
        # 0.5mm width of general decoration
        rect.setProp("height", str(troop_data['base_depth'] - 1))
        change_fill(rect, color)
    else:
        rect.unlinkNode()

    # Replace the text
    text_y = str(troop_data['base_depth'] - text_bottom_margin)
    res = ctxt.xpathEval("//svg:text[@inkscape:label='troop type']")
    text = res[0]
    text.setProp("y", text_y)

    res = ctxt.xpathEval("//svg:text[@inkscape:label='troop type']/svg:tspan")
    tspan = res[0]
    tspan.setContent(troop_name)

    res = ctxt.xpathEval("//svg:text[@inkscape:label='combat factors']")
    text = res[0]
    text.setProp("y", text_y)

    # Set the combat factors text
    res = ctxt.xpathEval("//svg:text[@inkscape:label='combat factors']/svg:tspan/text()")
    text_combat = res[0]
    combat = f" {troop_data['combat_factor_vs_foot']}/{troop_data['combat_factor_vs_mounted']}"
    text_combat.setContent(combat)

    # Set the movement rate
    res = ctxt.xpathEval("//svg:text[@inkscape:label='combat factors']/svg:tspan/svg:tspan")
    tspan_movement = res[0]
    tspan_movement.setContent(f"{troop_data['tactical_move_distance']}MU")
    tspan.setContent(troop_name)

    # Replace the icon
    res = ctxt.xpathEval("//svg:image[@inkscape:label='icon']")
    image = res[0]
    image.setProp("sodipodi:absref", icon_file_name)
    image.setProp("xlink:href", icon_file_name)
    image.setProp("preserveAspectRatio", "xMidYMid")
    image.setProp("height", str(troop_data["base_depth"] - icon_bottom_margin));

    doc.saveFileEnc(svg_file_name, "UTF-8")
    doc.freeDoc()
    ctxt.xpathFreeContext()

def make_svgs(troop_name: str, troop_data: dict):
    for color in ['red', 'blue'] :
        for general in [ True, False]:
            make_svg(color, general, type, data[type])

with open("data.json", "r") as data_file:
    data = json.load(data_file)
    for type in data:
        if type not in ["Camp", 'Elephant Screen Counter']:
            make_svgs(type, data[type])


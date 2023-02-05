#!/usr/bin/env python3

import json
import libxml2
import pathlib
import sys


text_bottom_margin = 15 - 13.857281
icon_bottom_margin = 15 - 9.5093451

def is_foot(troop_data: dict) -> bool:
    if 'open_order_foot' in troop_data:
        return troop_data['open_order_foot']
    if 'close_order_foot' in troop_data:
        return troop_data['close_order_foot']
    return False

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

def make_svg(color:str, general: bool, troop_name: str, troop_data: dict, mobile_infantry: bool):
    if general:
        general_file_name = "_general"
    else:
        general_file_name = ""
    
    name_suffix = ""
    mobile_infantry_file_name = ""
    base_depth = troop_data['base_depth']
    y_adjustment = 0
    movement_rate = troop_data['tactical_move_distance']
    if mobile_infantry:
        mobile_infantry_file_name = "_mi"
        base_depth = 40
        y_adjustment = (troop_data['base_depth'] - base_depth) / 2.0
        movement_rate = 6
        name_suffix = name_suffix + " MI"

    svg_file_name = (f"{color}_{troop_name}{general_file_name}{mobile_infantry_file_name}.svg").lower().replace(' ','_')
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
    svg.setProp("height", f"{base_depth}mm")
    svg.setProp("viewBox", f"0 0 40 {troop_data['base_depth']}")
    svg.setProp("sodipodi:docname", svg_file_name)
    
    res = ctxt.xpathEval("//svg:rect[@inkscape:label='background']")
    rect = res[0]
    rect.setProp("height", str(base_depth))
    change_fill(rect, color)

    res = ctxt.xpathEval("//svg:rect[@inkscape:label='general outside']")
    rect = res[0]
    if not general:
        rect.unlinkNode()
    else:
        rect.setProp("height", str(base_depth))

    res = ctxt.xpathEval("//svg:rect[@inkscape:label='general inside']")
    rect = res[0]
    if not general:
        rect.unlinkNode()
    else:
        # 0.5mm width of general decoration
        rect.setProp("height", str(base_depth - 1))
        change_fill(rect, color)

    # Replace the text
    text_y = str(base_depth - text_bottom_margin)
    res = ctxt.xpathEval("//svg:text[@inkscape:label='troop type']")
    text = res[0]
    text.setProp("y", text_y)

    # Set the troop type
    res = ctxt.xpathEval("//svg:text[@inkscape:label='troop type']/svg:tspan")
    tspan = res[0]
    name = f"{troop_name}{name_suffix}"
    tspan.setContent(name)

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
    tspan_movement.setContent(f"{movement_rate}MU")

    # Replace the icon
    res = ctxt.xpathEval("//svg:image[@inkscape:label='icon']")
    image = res[0]
    image.setProp("sodipodi:absref", icon_file_name)
    image.setProp("xlink:href", icon_file_name)
    image.setProp("preserveAspectRatio", "xMidYMid")
    image_area_height = base_depth - icon_bottom_margin
    image.setProp("height", str(image_area_height));
    if mobile_infantry:
        mi_icon_file_name = "../icons/mobileinf.png"
        mi_image = image.copyNode(True)
        mi_image.setProp("sodipodi:absref", mi_icon_file_name)
        mi_image.setProp("xlink:href", mi_icon_file_name)
        mi_image.setProp("inkscape:label", "mi_icon")
        mi_icon_height = 0.25 * image_area_height
        icon_height = image_area_height - mi_icon_height
        image.setProp("height", str(icon_height));
        old_image_y = float(image.prop('y'))
        new_image_y = str(old_image_y + mi_icon_height)
        image.setProp("y", new_image_y)
        mi_image.setProp("height", str(mi_icon_height));
        image.addNextSibling(mi_image)

    # Adjust the y-position for mobile infrantry
    if mobile_infantry:
        res = ctxt.xpathEval("/svg:svg/svg:g//*['y']")
        for node in res:
            old_y = node.prop('y')
            if old_y is not None:
                new_y = str(float(old_y) + y_adjustment)
                node.setProp('y', new_y)

    doc.saveFileEnc(svg_file_name, "UTF-8")
    doc.freeDoc()
    ctxt.xpathFreeContext()

def make_svgs(troop_name: str, troop_data: dict):
    for color in ['red', 'blue'] :
        for general in [ True, False]:
            make_svg(color, general, type, data[type], mobile_infantry=False)
            if is_foot(troop_data):
                if type not in ["War Wagons"]:
                    make_svg(color, general, type, data[type], mobile_infantry=True)

with open("data.json", "r") as data_file:
    data = json.load(data_file)
    for type in data:
        if type not in ["Camp", 'Elephant Screen Counter']:
            make_svgs(type, data[type])


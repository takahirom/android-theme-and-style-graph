# -*- coding: utf-8 -*-
__author__ = 'takahirom'
import requests, xml.etree.ElementTree as etree
import os
import sys


def clean(value):
    return "\"" + value + "\""


def to_node(value):
    return value.replace(".", "_").replace("@", "at_").replace("/", "_").replace("-", "_").replace(":", "_")


def def_node(value):
    return to_node(value) + "[label=\"" + value + "\"]"


class StyleElement:
    def __init__(self, dirname, name, parent, item_dict):
        isinstance(item_dict, dict)
        self.item_dict = item_dict
        self.dirname = dirname
        self.name = name
        self.parent = parent

    def get_path(self):
        return self.dirname + "/" + self.name

    def to_node(self):
        return to_node(self.get_path())

    def def_node(self, search_item):
        is_define = False
        is_use = False
        if search_item:
            for key in self.item_dict.keys():
                if key[-len(search_item):] == search_item:
                    is_define = True
        if search_item:
            for key in self.item_dict.values():
                if key[-len(search_item):] == search_item:
                    is_use = True
        color = None
        if is_define:
            color = "\"#ffffaa\""
        if is_use:
            color = "\"#aaffaa\""
        if is_use and is_define:
            color = "\"#ffffaa\""
        return self.to_node() + "[label=\"" + self.get_path() + "\";" + ("color=" + color + ";" if color else "") + "]"

    def get_parent(self):
        if self.parent is None:
            return self.name[0:self.name.rfind(".")]
        else:
            return self.parent


class Style:
    def __init__(self, filename):
        self.filename = filename
        self.elements = []

    def add(self, name, parent, item_dict):
        self.elements.append(StyleElement(self.filename, name, parent, item_dict))


styles = []
if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    directory = "platform_frameworks_support"

if len(sys.argv) > 2:
    searchItem = sys.argv[2]
else:
    searchItem = None

if len(sys.argv) > 3:
    withFullPath = True
else:
    withFullPath = False

for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if dirname.find("values") < 0:
            continue
        if filename.find("styles") < 0 and filename.find("themes") < 0:
            continue

        fullPath = os.path.join(dirname, filename)
        text = open(fullPath).read()

        if withFullPath:
            style = Style(os.path.basename(fullPath))
        else:
            style = Style(os.path.basename(dirname) + "/" + filename)

        styles.append(style)
        data = etree.fromstring(text)
        if 0: assert isinstance(data, etree.Element)
        for rawStyle in data.findall("style"):
            item_dict = {}
            for item in rawStyle.findall("item"):
                if 0: assert isinstance(item, dict)
                item_dict.update({item.get("name"): item.text})
            style.add(rawStyle.get("name"), rawStyle.get("parent"), item_dict)

styles.sort()
styles.reverse()
for style in styles:
    print style.filename
sys.stdout = open("output/" + directory + '.dot', 'w')
print "digraph {"

if searchItem:
    print "define[label=\"<item name='..."+searchItem+"'>...</item>\",fillcolor=\"#ffaaaa\",style=filled];"
    print "use[label=\"<item name='...'>..."+searchItem+"</item>\",fillcolor=\"#aaffaa\",style=filled];"
    print "both[label=\"<item name='..."+searchItem+"'>..."+searchItem+"</item>\",fillcolor=\"#ffffaa\",style=filled];"

print " rankdir=LR;"
for style in styles:
    print " subgraph " + to_node(style.filename) + " {"
    print "node [style=filled;];"
    if style.filename.find("themes") > -1:
        print "node [color=\"#aaaaff\"];"

    print "  "
    print "  label = " + clean(style.filename) + ";"

    for element in style.elements:
        print "  " + element.def_node(searchItem) + ";"  # + " -> " + clean(element.parent)
        for parentElement in style.elements:
            if element.get_parent() == parentElement.name:
                print "  " + element.to_node() + " -> " + to_node(style.filename + "/" + element.get_parent()) + ";"
    print " }"
for style in styles:
    for element in style.elements:
        if element.get_parent():
            selfReach = False
            contain = False
            for parentStyle in styles:
                for parentElement in parentStyle.elements:
                    if element.get_parent() == parentElement.name:
                        contain = True
                    if element.get_parent() == parentElement.name and parentStyle != style:
                        print " " + element.to_node() + " -> " + parentElement.to_node() + ";"
                    if parentStyle == style:
                        selfReach = True
                        continue
                if selfReach:
                    continue
            if not contain:
                print " " + def_node(element.get_parent())
                print " " + element.to_node() + " -> " + to_node(element.get_parent()) + ";"

print "}"

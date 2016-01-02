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
    def __init__(self, dirname, name, parent):
        self.dirname = dirname
        self.name = name
        self.parent = parent

    def get_path(self):
        return self.dirname + "/" + self.name

    def to_node(self):
        return to_node(self.get_path())

    def def_node(self):
        return self.to_node() + "[label=\"" + self.get_path() + "\"]"

    def get_parent(self):
        if self.parent is None:
            return self.name[0:self.name.rfind(".")]
        else:
            return self.parent


class Style:
    def __init__(self, dirname):
        self.dirname = dirname
        self.elements = []

    def add(self, name, parent):
        self.elements.append(StyleElement(self.dirname, name, parent))


styles = []
if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    directory = "appcompat"

for dirname in os.listdir(directory):
    if dirname.find("values") < 0:
        continue
    for file in os.listdir(directory + "/" + dirname):
        if file.find("styles") < 0 and file.find("themes") < 0:
            continue
        text = open(directory + "/" + dirname + "/" + file).read()
        style = Style(dirname + "/" + file)
        styles.append(style)
        data = etree.fromstring(text)
        if 0: assert isinstance(data, etree.Element)
        for rawStyle in data.findall("style"):
            style.add(rawStyle.get("name"), rawStyle.get("parent"))

styles.sort()
styles.reverse()
for style in styles:
    print style.dirname
sys.stdout = open("output/" + directory + '.dot', 'w')
print "digraph {"
print " rankdir=LR;"
for style in styles:
    # print " subgraph cluster_"+to_node(style.dirname) +" {"
    print " subgraph " + to_node(style.dirname) + " {"
    if style.dirname.find("themes") > -1:
        print "node [style=filled,color=\"#aaaaff\"];"

    print "  "
    print "  label = " + clean(style.dirname) + ";"
    print """
    style = "dashed";
            """

    for element in style.elements:
        print "  " + element.def_node() + ";"  # + " -> " + clean(element.parent)
        for parentElement in style.elements:
            if element.get_parent() == parentElement.name:
                print "  " + element.to_node() + " -> " + to_node(style.dirname + "/" + element.get_parent()) + ";"
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

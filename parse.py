# -*- coding: utf-8 -*-
__author__ = 'takahirom'
import requests, xml.etree.ElementTree as etree
import os
import sys


class StyleElement:
    def __init__(self,name,parent):
        self.name = name
        self.parent = parent


class Style:
    def __init__(self,dirname):
        self.dirname = dirname
        self.elements = []

    def add(self,name,parent):
        self.elements.append(StyleElement(name,parent))


def clean(value):
    return "\"" + value+"\""

def to_node(value):
    return value.replace(".","_").replace("@","at_").replace("/","_").replace("-","_").replace(":","_")

def def_node(value):
    return to_node(value) +"[label=\"" + value+"\"]"



styles = []
for dirname in os.listdir("list"):
    if dirname.find("values")<0:
        continue
    for file in os.listdir("list/"+dirname):
        if file.find("styles") <0 and file.find("themes") <0:
            continue
        text = open("list/"+dirname+"/"+file).read()
        style = Style(dirname+"/"+file)
        styles.append(style)
        data = etree.fromstring(text)
        if 0: assert isinstance(data, etree.Element)
        for rawStyle in data.findall("style"):
            style.add(rawStyle.get("name"),rawStyle.get("parent"))


styles.reverse()
for style in styles:
    print style.dirname
sys.stdout = open('style.dot', 'w')
print "digraph {"
print " rankdir=LR;"
for style in styles:
    # print " subgraph cluster_"+to_node(style.dirname) +" {"
    print " subgraph "+to_node(style.dirname) +" {"
    print "  label = "+clean(style.dirname)+";"
    print """
    style = "dashed";
            """

    for element in style.elements:
        print "  "+def_node(style.dirname+"/"+element.name)+";"# + " -> " + clean(element.parent)
        for parentElement in style.elements:
            if element.parent == parentElement.name:
                    print "  "+to_node(style.dirname+"/"+element.name) + " -> " + to_node(style.dirname+"/"+element.parent)+";"
    print " }"
for style in styles:
    for element in style.elements:
        if element.parent:
            selfReach = False
            contain = False
            for parentStyle in styles:
                for parentElement in parentStyle.elements:
                    if element.parent == parentElement.name:
                        contain = True
                    if element.parent == parentElement.name and parentStyle != style:
                        print " "+to_node(style.dirname+"/"+element.name) + " -> " + to_node(parentStyle.dirname+"/"+element.parent)+";"
                    if parentStyle == style:
                        selfReach = True
                        continue
                if selfReach:
                    continue
            if not contain:
                print " "+def_node(element.parent)
                print " "+to_node(style.dirname+"/"+element.name) + " -> " + to_node(element.parent)+";"

print "}"


"""
digraph sample {
  subgraph value {
    label = "area 0";
    a->b;
    a->c;
  }
  subgraph values-v21 {
    label = "area 1";
    d->e;
    d->f;
  }
  b->d; // ここを加える
}
"""



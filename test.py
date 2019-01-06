# -*- coding: utf-8 -*-
__author__ = 'takahirom'
import requests, xml.etree.ElementTree as etree
import os
import sys

for dirname, dirnames, filenames in os.walk('material-component-android'):
    for filename in filenames:
        if dirname.find("values") < 0:
            continue
        if filename.find("styles") < 0 and filename.find("themes") < 0:
            continue

        print(os.path.basename(dirname) + "/" + filename)
        # print(os.path.join(dirname, filename))

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    # if '.git' in dirnames:
    #     # don't go into any .git directories.
    #     dirnames.remove('.git')

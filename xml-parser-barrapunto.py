#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import os
import urllib.request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.title = ""
        self.link = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = "<h3> Title: " + self.theContent + ".</h3>"
                fichero = open(sys.argv[2], "a")
                fichero.write(self.title)
                print(self.title)
                self.inContent = False
                self.theContent = ""
                self.title = ""
            elif name == 'link':
                print(" Link: " + self.theContent + ".")
                self.link = "<p>Link: <a href=" + self.theContent + ">" + self.theContent + "</a></p>"
                fichero = open(sys.argv[2], "a")
                fichero.write(self.link + "\n")
                print(self.link)
                self.inContent = False
                self.theContent = ""
                self.link = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)<3:
    print("Usage: python xml-parser-barrapunto.py <document.rss> <document.html>")
    print()
    print(" <document.rss>: file name of the document to parse")
    print(" <document.html>: file name of the html document to save")
    sys.exit(1)

#Creamos un fichero
fichero = open(sys.argv[1], "w")
url = "http://barrapunto.com/barrapunto.rss"
f = urllib.request.urlopen(url)
body = f.read().decode('utf-8')
fichero.write(body)
fichero.close()

if os.path.exists(sys.argv[2]):
	os.remove(sys.argv[2])

# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)

print ("Parse complete")

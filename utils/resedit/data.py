#!/usr/bin/env python

from xml.dom import minidom
import sets

def uniq(alist):    # Fastest order preserving
   s = sets.Set(alist)
   del alist[:]
   for a in s:
      alist.append(a)


def load(xmlfile, tag, has_name=True, do_array=None):
   dom = minidom.parse(xmlfile)
   xmlNodes = dom.getElementsByTagName(tag)

   dictionary = {}
   for xmlNode in xmlNodes:

      mdic = {}
      # name is stored as a property and not a node
      if (has_name):
         name = xmlNode.attributes["name"].value

      # process the nodes
      for bignode in filter(lambda x: x.nodeType==x.ELEMENT_NODE, xmlNode.childNodes):
         # load the nodes
         section = {}
         array = []
         for node in filter(lambda x: x.nodeType==x.ELEMENT_NODE,
               bignode.childNodes):
            if bignode.nodeName in do_array: # big ugly hack to use list instead of array
               array.append(node.firstChild.data)
            else: # normal way (but will overwrite lists)
               section[node.nodeName] = node.firstChild.data

         if len(array) > 0:
            mdic[bignode.nodeName] = array
         else:
            mdic[bignode.nodeName] = section

      # append the element to the dictionary
      dictionary[name] = mdic
   
   dom.unlink()
   return dictionary


def save(xmlfile, data, basetag, tag, has_name=True, do_array=None):
   """
   do_array is a DICTIONARY, not a list here
   """
   xml = minidom.Document()

   base = xml.createElement(basetag)

   for key, value in data.items():

      elem = xml.createElement(tag)
      if has_name:
         elem.setAttribute("name",key)

      for key2, value2 in value.items():
         node = xml.createElement(key2)

         # checks if it needs to parse an array instead of a dictionary
         if do_array != None and key2 in do_array.keys():
            for text in value2:
               node2 = xml.createElement( do_array[key2] )
               txtnode = xml.createTextNode( text )
               node2.appendChild(txtnode)
               node.appendChild(node2)

         # standard dictionary approach
         else:
            for key3, value3 in value2.items():
               node2 = xml.createElement( key3 )
               txtnode = xml.createTextNode( value3 )
               node2.appendChild(txtnode)
               node.appendChild(node2)

         elem.appendChild(node)
      base.appendChild(elem)
   xml.appendChild(base)

   fp = open(xmlfile,"w")
   xml.writexml(fp, "", "", "", "UTF-8")

   xml.unlink()





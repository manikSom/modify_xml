# File:xml_plus_inc_to_mod_xml
# Author: manikSom
# Contact: manickam.som@gmail.com
#
#   This program is free software;  you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY;  without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
#   the GNU General Public License for more details.

import xml.dom.minidom
from xml.dom.minidom import Node

input_ak3_file='input_xml.xml'
input_inc_file='element_3D.inc'
output_ak3_file='modified_xml.xml'

ak3dom = xml.dom.minidom.parse(input_ak3_file)
def remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            remove_blanks(x)

node_group =ak3dom.getElementsByTagName('Nodes')
node_group.item(0).attributes['N'].value =0
node_group1 =node_group.item(0).getElementsByTagName('Node')
for element in node_group1:
    parent = element.parentNode
    parent.removeChild(element)
    
print("Remove all nodes from input ak3 file....")
     
def create_node(j,k,l,m):    
    for node in node_group:
        rating = ak3dom.createElement('Node')
        node_id=ak3dom.createElement('Id')
        node_x=ak3dom.createElement('x')
        node_y=ak3dom.createElement('y')
        node_z=ak3dom.createElement('z')
        text1 = ak3dom.createTextNode(str(j))
        text2 = ak3dom.createTextNode(str(k))
        text3 = ak3dom.createTextNode(str(l))
        text4 = ak3dom.createTextNode(str(m))
        node_id.appendChild(text1)
        node_x.appendChild(text2)
        node_y.appendChild(text3)
        node_z.appendChild(text4)
        rating.appendChild(node_id)
        rating.appendChild(node_x)
        rating.appendChild(node_y)
        rating.appendChild(node_z)
        node.appendChild(rating)
        
ele_group =ak3dom.getElementsByTagName('Elements')
for group_no1 in range(len(ele_group)):
    ele_group1 =ele_group.item(group_no1).getElementsByTagName('Brick8')
    for element in ele_group1:
        parent = element.parentNode
        parent.removeChild(element)
        
print("Removed all elements from input ak3 file....")
        
def create_ele(gid,arr):
    text=[]
    node=[]
    for i in range(9):
        text.append(0)
        node.append(0)
    for group_no1 in range(len(ele_group)):
        if (ele_group.item(group_no1).attributes['GroupId'].value==str(gid)):
            rating = ak3dom.createElement('Brick8') #Change the type of element depending on the output desired
            node_id=ak3dom.createElement('Id')
            text1 = ak3dom.createTextNode(str(arr[0]))
            node_id.appendChild(text1)
            rating.appendChild(node_id)
            for j in range(1,9): #Change the range to range(1,5) for 2D files
                node[j]=ak3dom.createElement('N')
                text[j]=ak3dom.createTextNode(str(arr[j]))
                node[j].appendChild(text[j])
                rating.appendChild(node[j])
            ele_group.item(group_no1).appendChild(rating)

print("Stating readind elements.inc...")
file1 = open(input_inc_file,'r')
filelines = file1.readlines()
node=0
ele1=0
ele2=0
nNode=0
nEle1=0
nEle2=0
for line in filelines:
        if "*NODE" in line:node=1
        if "PRIME_MATERIAL" in line:ele1=1;node=0
        if "NONDESIGN" in line:ele2=1;ele1=0
        if (node==1):
                if "*NODE" not in line:
                        nNode=nNode+1
                        my_list = [int(x) for x in line.split(',')]
                        create_node(my_list[0],my_list[1],my_list[2],my_list[3])
        if (ele1==1):
                if "*ELEMENT" not in line:
                        nEle1=nEle1+1
                        my_list = [int(x) for x in line.split(',')]
                        create_ele(1,my_list)
        if (ele2==1):
                if "*ELEMENT" not in line:
                        nEle2=nEle2+1
                        my_list = [int(x) for x in line.split(',')]
                        create_ele(2,my_list)
print("no of element",nNode, nEle1, nEle2)

ak3dom.getElementsByTagName('Nodes').item(0).setAttribute('N',str(nNode))
ak3dom.getElementsByTagName('Elements').item(0).setAttribute('N',str(nEle1))
ak3dom.getElementsByTagName('Elements').item(1).setAttribute('N',str(nEle2))

ak3dom.writexml(open(output_ak3_file, 'w'), indent="", addindent="", newl='', encoding="utf-8")
xml = xml.dom.minidom.parse(output_ak3_file)
remove_blanks(xml)
xml.normalize()
with open(output_ak3_file, 'w') as result:
    result.write(xml.toprettyxml(indent = '  '))

print("Finished writing out the new .xml file with new set of values from elements.inc ....")
file1.close()

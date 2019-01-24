xml_plus_inc_to_mod_xml.py

is a python script that takes a .xml file and a .inc file as input.
.inc file is a geometry file(meshed) that can be generated with 
Abaqus or ANSA. element_3D.inc and input_xml.xml are the 
inputs. The script reads both the files and replaces the elements in 
the element_3D.inc into the input_xml.xml and creates a new
modified_xml.xml file.
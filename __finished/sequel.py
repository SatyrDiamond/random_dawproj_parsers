# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from _sequel import func
import xml.etree.ElementTree as ET

input_file = "C:\\Program Files (x86)\\Steinberg\\Sequel 3\\Projects\\Sequel 3 Demo - Third Generation\\Sequel 3 Demo - Third Generation.steinberg-project"

class sequel_project:
	def __init__(self):
		self.root_objects = {}
		self.objects = []

	def load_from_file(self, filename):
		x_root = ET.parse(input_file).getroot()
		func.globalids = {}
		root_objects = {}
		for x in x_root:
			if x.tag == 'rootObjects':
				for i in x:
					root_objects[i.get('name')] = int(i.get('ID'))
			else:
				self.objects.append(func.sequel_object(x))

main_obj = sequel_project()
main_obj.load_from_file(input_file)



#in_obj = func.sequel_object(all_obj[0])



#xmldata = ET.Element("SteinbergProject")
#in_obj.write(xmldata, None)
#outfile = ET.ElementTree(xmldata)
#ET.indent(outfile, space="   ")
#outfile.write('out.xml', encoding='utf-8', xml_declaration = True)

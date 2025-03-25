# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET

def strbool(i): return 'true' if i else 'false'

def get_int_comma(i): return [int(x) for x in i.split(',')]

def make_int_comma(i): return ','.join([str(x) for x in i])

def maketxtsub(xmld, name, txt): 
	addx = ET.SubElement(xmld, name)
	if txt is not None: addx.text = txt

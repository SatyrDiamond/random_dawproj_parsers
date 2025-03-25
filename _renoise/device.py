# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET

from _renoise import instrument
from _renoise import func
strbool = func.strbool
maketxtsub = func.maketxtsub
make_int_comma = func.make_int_comma

class renoise_envelope:
	def __init__(self):
		self.PlayMode = 'Lines'
		self.Length = 64
		self.ValueQuantum = 0.0
		self.Polarity = 'Unipolar'
		self.Points = []

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'PlayMode': self.PlayMode = xpart.text
			if xpart.tag == 'Length': self.Length = int(xpart.text)
			if xpart.tag == 'ValueQuantum': self.ValueQuantum = float(xpart.text)
			if xpart.tag == 'Polarity': self.Polarity = xpart.text
			if xpart.tag == 'Points':
				for xinpart in xpart:
					if xinpart.tag == 'Point': self.Points.append(xinpart.text.split(','))

	def write(self, xmldata, tagname):
		tempd = ET.SubElement(xmldata, tagname)
		maketxtsub(tempd, 'PlayMode', str(self.PlayMode))
		maketxtsub(tempd, 'Length', str(self.Length))
		maketxtsub(tempd, 'ValueQuantum', str(self.ValueQuantum))
		maketxtsub(tempd, 'Polarity', str(self.Polarity))
		pointsx = ET.SubElement(tempd, 'Points')
		for Point in self.Points: maketxtsub(pointsx, 'Point', ','.join(Point))

class renoise_devicechain:
	def __init__(self):
		self.SelectedPresetName = ''
		self.SelectedPresetIsModified = False
		self.Name = None
		self.Devices = []
		self.RoutingIndex = None

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.SelectedPresetName = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.SelectedPresetIsModified = xpart.text=='true'
			if xpart.tag == 'Name': self.Name = xpart.text
			if xpart.tag == 'RoutingIndex': self.RoutingIndex = int(xpart.text)
			if xpart.tag == 'Devices':
				for xinpart in xpart:
					device_obj = renoise_device()
					device_obj.read(xinpart)
					self.Devices.append(device_obj)

	def write(self, xmldata):
		self.write_tag(xmldata, 'DeviceChain')

	def write_tag(self, xmldata, tagname):
		tempd = ET.SubElement(xmldata, tagname)
		maketxtsub(tempd, 'SelectedPresetName', str(self.SelectedPresetName))
		maketxtsub(tempd, 'SelectedPresetIsModified', strbool(self.SelectedPresetIsModified))
		xmldevices = ET.SubElement(tempd, 'Devices')
		for device_obj in self.Devices:
			device_obj.write(xmldevices)
		if self.Name is not None: 
			maketxtsub(tempd, 'Name', str(self.Name))
		if self.RoutingIndex is not None: 
			maketxtsub(tempd, 'RoutingIndex', str(self.RoutingIndex))

class renoise_device_param:
	def __init__(self):
		self.Value = 0
		self.Visualization = ''
		self.Name = None
		self.mappings = []

	def read(self, xmldata):
		for x in xmldata:
			val = x.text
			if x.tag == 'Value': self.Value = float(val) if '.' in val else int(val)
			if x.tag == 'Visualization': self.Visualization = x.text
			if x.tag == 'Name': self.Name = x.text
			if x.tag == 'Mappings':
				for xinpart in x:
					if xinpart.tag == 'Mapping':
						map_obj = instrument.renoise_instrument_macro_mappings()
						map_obj.read(xinpart)
						self.mappings.append(map_obj)

	def write(self, xmldata):
		maketxtsub(xmldata, 'Value', str(self.Value))
		maketxtsub(xmldata, 'Visualization', self.Visualization)
		if self.Name is not None: maketxtsub(xmldata, 'Name', str(self.Name))
		if self.mappings:
			xmlmappings = ET.SubElement(xmldata, 'Mappings')
			for map_obj in self.mappings: map_obj.write(xmlmappings)

class renoise_device:
	def __init__(self):
		self.tag = ''
		self.params = {}
		self.data = {}
		self.envelopes = {}
		self.order = []
		self.ext_params = []
		self.CustomEnvelope = None
		self.CustomEnvelopeOneShot = None
		self.UseAdjustedEnvelopeLength = None
		self.DeviceChain = None

	def read(self, xmldata):
		self.tag = xmldata.tag
		for xinpart in xmldata:
			partlist = [x.tag for x in xinpart]

			if xinpart.tag == 'DeviceChain':
				self.DeviceChain = renoise_devicechain()
				self.DeviceChain.read(xinpart)
			elif xinpart.tag == 'CustomEnvelopeOneShot': self.CustomEnvelopeOneShot = xinpart.text=='true'
			elif xinpart.tag == 'UseAdjustedEnvelopeLength': self.UseAdjustedEnvelopeLength = xinpart.text=='true'
			elif xinpart.tag == 'Parameters' and all([x=='Parameter' for x in partlist]): 
				for x in xinpart:
					param_obj = renoise_device_param()
					param_obj.read(x)
					self.ext_params.append(param_obj)
			else:
	
				if 'Value' in partlist and 'Visualization' in partlist:
					param_obj = renoise_device_param()
					param_obj.read(xinpart)
					self.params[xinpart.tag] = param_obj
					self.order.append(xinpart.tag)

				elif all([(x in partlist) for x in ['PlayMode', 'Length', 'ValueQuantum', 'Polarity', 'Points']]):
					param_obj = renoise_envelope()
					param_obj.read(xinpart)
					self.envelopes[xinpart.tag] = param_obj
					self.order.append(xinpart.tag)
	
				elif not partlist:
					self.data[xinpart.tag] = xinpart.text
					self.order.append(xinpart.tag)
	
				else:
					print(    xinpart.tag,  partlist   )

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, self.tag)
		tempd.set('type', self.tag)
		for name in self.order:
			if name in self.params:
				param_obj = self.params[name]
				pxml = ET.SubElement(tempd, name)
				param_obj.write(pxml)
			if name in self.data:
				maketxtsub(tempd, name, str(self.data[name]))
			if name in self.envelopes:
				self.envelopes[name].write(tempd, name)
		if self.CustomEnvelopeOneShot is not None: 
			maketxtsub(tempd, 'CustomEnvelopeOneShot', strbool(self.CustomEnvelopeOneShot))
		if self.DeviceChain is not None: 
			self.DeviceChain.write(tempd)
		if self.UseAdjustedEnvelopeLength is not None: 
			maketxtsub(tempd, 'UseAdjustedEnvelopeLength', strbool(self.UseAdjustedEnvelopeLength))
		if self.ext_params:
			paramsv = ET.SubElement(tempd, 'Parameters')
			for x in self.ext_params:
				paramv = ET.SubElement(paramsv, 'Parameter')
				x.write(paramv)

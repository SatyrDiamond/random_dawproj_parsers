# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
from objects.binary_fmt import juce_binaryxml
import logging
import zlib
from lxml import etree as ET

class soundbug_song:
	def load(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'SNDR')

		compdata = zlib.decompress(byr_stream.raw(byr_stream.uint32()))
		decompdata = bytereader.bytereader(compdata)

		compdata = zlib.decompress(decompdata.rest())
		byr_stream = bytereader.bytereader(compdata)

		self.root = juce_binaryxml.juce_binaryxml_element()
		self.root.read_byr(byr_stream)

	def save(self, output_file):
		self.root.output_file(output_file)

apeinst_obj = soundbug_song()
apeinst_obj.load("C:\\Program Files\\SoundBug\\Examples\\青花瓷完整版.sndt")
apeinst_obj.save('outs.xml')

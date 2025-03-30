# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET
import logging
import io

readparts = {
	'N': 3,
	'0': 3,
	'1': 1,
	'2': 2,
}

class onetracker_patternrow:
	def __init__(self):
		self.marker = False
		self.data = []
		self.label = ''

class onetracker_song:
	def __init__(self):
		self.Engine = ''
		self.Title = ''
		self.Author = ''
		self.Speed = 20
		self.LoopStart = 0
		self.LoopEnd = 0
		self.Measure = 4
		self.PatternFormat = ''
		self.Instruments = {}
		self.pattern = {}

	def load_from_file(self, input_file):
		f = open(input_file, 'r')

		scat = None
		songnum = 0

		for line in f.readlines():
			line = line.strip()
			if line:
				if line[0] == '[': 
					scat = line[1:-1]
				else:
					if scat == '1tracker module':
						if '=' in line:
							splitl = line.split('=', 1)
							if len(splitl) == 2:
								k_name, k_data = splitl
								if k_name == 'Engine': self.Engine = k_data
					if scat == 'Settings':
						if '=' in line:
							splitl = line.split('=', 1)
							if len(splitl) == 2:
								k_name, k_data = splitl
								if k_name == 'Title': self.Title = k_data
								if k_name == 'Author': self.Author = k_data
								if k_name == 'Speed': self.Speed = int(k_data)
								if k_name == 'LoopStart': self.LoopStart = int(k_data)
								if k_name == 'LoopEnd': self.LoopEnd = int(k_data)
								if k_name == 'Measure': self.Measure = int(k_data)
								if k_name == 'PatternFormat': self.PatternFormat = k_data.split('_')
					if scat == 'Instruments':
						if '=' in line:
							splitl = line.split('=', 1)
							if len(splitl) == 2:
								k_name, k_data = splitl
								if k_name.startswith('Instrument'):
									self.Instruments[k_name[10:]] = k_data
					if scat == 'Song':
						siline = io.StringIO(line)
						pat_pos = siline.read(4)
						pr = onetracker_patternrow()
						pr.marker = siline.read(1)=='*'
						pr.data = []
						for n, p in enumerate(self.PatternFormat):
							pr.data.append([siline.read(readparts[x]).replace('.', '') for x in p])
							if n!=len(self.PatternFormat)-1: siline.read(1)
						pr.label = siline.read()
						self.pattern[int(pat_pos)] = pr

apeinst_obj = onetracker_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\tracker_lessknown\\1Tracker\\examples\\freezing_point.1tm")

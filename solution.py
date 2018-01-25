"""
	solution for cda5155 from andrew berg spring 2017 whalley
"""

"""
	class to read in the config and store the information
"""

import sys
import math

class Config:
	def __init__(self, file_name):

		self.file_name = file_name
		
		"""data tlb config"""

		num_sets = 0
		set_size = 0

		"""page table config"""

		num_virtual_pages = 0
		num_physical_pages = 0
		page_size = 0

		"""data cache config"""

		num_sets_data = 0
		set_size_data = 0
		line_size = 0

		"""victim cache config"""

		set_size_victim = 0

		"""flags for turning stuff on """

		virtual_add = False
		tlb = False
		victim_cache = False

		self.read_config()

		# calculate index and offsets for perspective values
		
		self.calculate_values()

		# print the header

		self.print_config()
		self.print_header()

	def read_config(self):
		
		# counter value to know where to put what
		i = 0

		for line in open(self.file_name):
			if ":" not in line:
				continue

			value = line.strip().split(":")[1].strip()

			if i is 0:
				self.num_sets = value
			elif i is 1:
				self.set_size = value
			elif i is 2:
				self.num_virtual_pages = value
			elif i is 3:
				self.num_physical_pages = value
			elif i is 4:
				self.page_size = value
			elif i is 5:
				self.num_sets_data = value
			elif i is 6:
				self.set_size_data = value
			elif i is 7:
				self.line_size = value
			elif i is 8:
				self.set_size_victim = value
			elif i is 9:
				if value is "n":
					self.virtual_add = False
				else:
					self.virtual_add = True
			elif i is 10:
				if value is "n":
					self.tlb = False
				else:
					self.tlb = True
			elif i is 11:
				if value is "n":
					self.victim_cache = False
				else:
					self.victim_cache = True

			# increment everytime a line is read
			
			i += 1
			

	def calculate_values(self):

		# d-cache calculations
		
		self.d_cache_index = int(math.log(float(self.num_sets_data), 2))
		self.d_cache_offset = int(math.log(float(self.line_size), 2))

		# data-tlb calculations

		self.tlb_index = int(math.log(float(self.num_sets), 2))
		
		# page-table calculations

		self.pt_index = int(math.log(float(self.num_virtual_pages), 2))
		self.pt_offset = int(math.log(float(self.page_size), 2))

	"""prints each entry into the config file"""

	def print_config(self):

		# data tlb info
		
		print("Data TLB contains " + self.num_sets + " sets.")
		print("Each set contains " + self.set_size + " entries.")
		"""TODO:"""
		print("Number of bits used for the index is " + str(self.tlb_index) + ". \n")

		# page table info
		
		print("Number of virtual pages is " + self.num_virtual_pages + ".")
		print("Number of physical pages is " + self.num_physical_pages + ".")
		print("Each page contains " + self.page_size + " bytes.")
		print("Number of bits used for the page table index is " + str(self.pt_index) + ".")
		print("Number of bits used for the page offset is " + str(self.pt_offset) + ".")
		print("")

		# data cache info
		
		print("D-cache contains " + self.num_sets_data + " sets.")
		print("Each set contains " + self.set_size_data + " entries.")
		print("Each line is " + self.line_size + " sets.")
		print("Number of bits used for the index is "+ str(self.d_cache_index) + ".")
		print("Number of bits used for the offset is " + str(self.d_cache_offset) + ".")
		print("")

		# v-cache config

		print("Each V-cache set contains " + self.set_size_victim + " entries.")
		print("")

		# virtual addresses
		
		if self.virtual_add:
			print("The addresses read in are virtual addresses.")
		else:
			print("The addresses read in are physical addresses.")

		if not self.tlb:
			print("TLB is disabled in this configuration.")

		if not self.victim_cache:
			print("VC is disabled in this configuration.")

		print("\n")

	def print_header(self):
		if self.virtual_add:
			print("Virtual  Virt.\tPage TLB    TLB TLB  PT   Phys\t      DC  DC\t      VC")
		else:
			print("Physical Virt.\tPage TLB    TLB TLB  PT   Phys\t      DC  DC\t      VC")
		print("Address  Page #\tOff  Tag    Ind Res. Res. Pg # DC Tag Ind Res. VC Tag Res.")
		print("-------- ------ ---- ------ --- ---- ---- ---- ------ --- ---- ------ ----")

		#print('{:08x} {:6x} {:4x} {:6x}{:4x} {:>4} {:>4} {:4x} {:6x} {:3x} {:>4} {:6x} {:>4}'.format(0xc84, 0xc, 0x84, 0x6, 0x0, "miss", "miss", 0x0, 0x2, 0x0, "miss", 0x8, "miss"))
	
"""
	Class for taking in the trace data and running functions on this data
"""

class TraceData:

	def __init__(self, config):
		self.data = list()

		"""config to know how many bits for each"""

		self.config = config

		"""takes all data from trace_data file and stores it"""

		self.take_trace()

		"""does all necessary calculations for output"""

		self.calculate_all()

	"""function to take trace data and create trace data objects"""

	def take_trace(self):
		
		for line in sys.stdin.readlines():
			value = line.strip().split(":")
			dum = TraceLine(value[0], value[1])
			
			self.data.append(dum)

	"""function to calculate different values based on shifts"""

	def calculate_all(self):
		for val in self.data:

			self.calc_vp_num(val)

			self.calc_p_offset(val)
			
			# dc
			self.calc_dc_index(val)
			self.calc_dc_tag(val)

			self.print_line(val.add, val.vp_num, val.p_offset, -1 ,-1, "none", "none", -1, val.dc_tag, val.dc_index, "none", -1, "none")

	"""function for printing all data (-1 for values not done yet)"""

	def print_line(self, add, vp_num, p_offset, tlb_tag, tlb_ind, tlb_res, pt_res, p_num, dc_tag, dc_ind, dc_res, vc_tag, vc_res):
		print('{:08x}'.format(add)),

		if self.config.virtual_add:
			print('{:6x}'.format(vp_num)),
		else:
			print('{:>6}'.format("")),

		print('{:4x}'.format(p_offset)),

		if self.config.tlb:
			print('{:6x}{:4x} {:>4} {:>4}'.format(tlb_tag, tlb_ind, tlb_res, pt_res)),
		else:
			print('{:>6}{:>4} {:>4} {:>4}'.format("", "", "", "")),

		print('{:4x} {:6x} {:3x} {:>4}'.format(p_num, dc_tag, dc_ind, dc_res)),

		if self.config.victim_cache:
			print('{:6x} {:>4}'.format(vc_tag, vc_res))
		else:
			print("")


		#print('{:08x} {:6x} {:4x} {:6x}{:4x} {:>4} {:>4} {:4x} {:6x} {:3x} {:>4} {:6x} {:>4}'
			#.format(add, vp_num, p_offset, tlb_tag, tlb_ind, tlb_res, pt_res, p_num, dc_tag, dc_ind, dc_res, vc_tag, vs_res))

	"""calculate the virtual address to physical address"""

	def add_conversion(self):
		pass

	"""calculate virtual page #"""

	def v_calc_p_num(self):
		pass

	"""physical page offset calculation"""

	def calc_p_offset(self, val):
		offset = config.pt_offset

		mask = 2 ** offset - 1
		val.p_offset = val.add & mask

	"""physical page number calculation"""

	def calc_vp_num(self, val):
		# calculate size of the p_num
		size = config.pt_offset
		
		mask = 2 ** 32 - 1
		mask = mask << size
		
		res = val.add & mask
		
		val.vp_num = res >> size

	"""offset for data cache"""

	def calc_dc_offset(self, val):

		mask = 2 ** config.d_cache_offset - 1

		res = val.add & mask

		val.dc_offset = res

	def calc_dc_index(self, val):

		shift = config.d_cache_offset
		mask = 2 ** config.d_cache_index - 1

		mask = mask << shift
		res = val.add & mask
		
		res = res >> shift

		val.dc_index = res
		
	"""tag for data cache calculation"""

	def calc_dc_tag(self, val):
		shift = config.d_cache_offset + config.d_cache_index

		mask = sys.maxint
		mask = mask << shift

		res = val.add & mask

		res = res >> shift

		val.dc_tag = res

"""
	class for storing each trace data entry
"""

class TraceLine:

	def __init__(self, t, add):
		self.type = t
		self.add = int(add, 16)

		self.vp_num = -1
		self.p_offset = -1

		self.dc_tag = -1
		self.dc_index = -1
		self.dc_offset = -1

"""
	Data cache for computing hits/misses
"""

class DataCache:

	def __init__(self):
		pass

if __name__ == "__main__":
	config = Config("trace.config")

	data = TraceData(config)
	data.take_trace()

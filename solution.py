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

		self.num_sets = 0
		self.set_size = 0

		"""page table config"""

		self.num_virtual_pages = 0
		self.num_physical_pages = 0
		self.page_size = 0

		self.d_cache_index = 0


		"""data cache config"""

		self.num_sets_data = 0
		self.set_size_data = 0
		self.line_size = 0

		"""victim cache config"""

		self.set_size_victim = 0

		"""flags for turning stuff on """

		self.virtual_add = False
		self.tlb = False
		self.victim_cache = False

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
				self.num_sets_data = int(value)
			elif i is 6:
				self.set_size_data = int(value)
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
		
		self.d_cache_index = int(math.log(float(self.num_sets_data))/math.log(2))

		self.d_cache_offset = int(math.log10(float(self.line_size))/math.log10(2))

		# data-tlb calculations

		self.tlb_index = int(math.log10(float(self.num_sets))/math.log10(2))
		
		# page-table calculations

		self.pt_index = int(math.log10(float(self.num_virtual_pages))/math.log10(2))
		self.pt_offset = int(math.log10(float(self.page_size))/math.log10(2))

	"""prints each entry into the config file"""

	def print_config(self):

		# data tlb info
		
		print("Data TLB contains " + self.num_sets + " sets.")
		print("Each set contains " + self.set_size + " entries.")
		"""TODO:"""
		print("Number of bits used for the index is " + str(self.tlb_index) + ".\n")

		# page table info
		
		print("Number of virtual pages is " + self.num_virtual_pages + ".")
		print("Number of physical pages is " + self.num_physical_pages + ".")
		print("Each page contains " + self.page_size + " bytes.")
		print("Number of bits used for the page table index is " + str(self.pt_index) + ".")
		print("Number of bits used for the page offset is " + str(self.pt_offset) + ".")
		print("")

		# data cache info
		
		print("D-cache contains " + str(self.num_sets_data) + " sets.")
		print("Each set contains " + str(self.set_size_data) + " entries.")
		print("Each line is " + self.line_size + " bytes.")
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
			print("Virtual  Virt.  Page TLB    TLB TLB  PT   Phys          DC  DC        VC")
		else:
			print("Physical Virt.  Page TLB    TLB TLB  PT   Phys        DC  DC          VC")
		print("Address  Page # Off  Tag    Ind Res. Res. Pg # DC Tag Ind Res. VC Tag Res.")
		print("-------- ------ ---- ------ --- ---- ---- ---- ------ --- ---- ------ ----")

		#print('{:08x} {:6x} {:4x} {:6x}{:4x} {:>4} {:>4} {:4x} {:6x} {:3x} {:>4} {:6x} {:>4}'.format(0xc84, 0xc, 0x84, 0x6, 0x0, "miss", "miss", 0x0, 0x2, 0x0, "miss", 0x8, "miss"))
	
"""
	Class for taking in the trace data and running functions on this data
"""

class TraceData:

	def __init__(self, config, pt, tlb):
		self.data = list()

		"""config to know how many bits for each"""

		self.config = config

		"""page table for physical conversion"""

		self.pt = pt

		self.tlb = tlb

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

	"""function to print all of the values in the given results"""

	def print_all(self):
		for val in self.data:
			self.print_line(val.v_add, val.vp_num, val.p_offset, val.tlb_tag, val.tlb_ind, val.tlb_res, val.pt_res, val.physical_page, val.dc_tag, val.dc_index, val.dc_res, val.victim_tag, val.victim_res)

	"""function to calculate different values based on shifts"""

	def calculate_all(self):
		for val in self.data:

			self.calc_vp_num(val)

			self.calc_p_offset(val)

			# tlb calculations

			self.calc_tlb_index(val)
			self.calc_tlb_tag(val)

			if self.config.tlb:

				# if hit then don't go to pagetable

				val.add = self.tlb.check_tlb(val)

			if self.config.virtual_add:
				# need to do virtual to physical address conversion
		
				val.add = self.pt.convert_to_phy(val)
			
			# dc

			self.calc_dc_index(val)
			self.calc_dc_tag(val)

			self.calc_phys_page(val)

			# victim cache

			self.calc_victim_tag(val)


	"""function for printing all data (-1 for values not done yet)"""

	def print_line(self, add, vp_num, p_offset, tlb_tag, tlb_ind, tlb_res, pt_res, p_num, dc_tag, dc_ind, dc_res, vc_tag, vc_res):
		print('%08x' % add),

		if self.config.virtual_add:
			print('%6x' % vp_num),
		else:
			print('%6s' % ("")),

		print('%4x' % p_offset),

		if self.config.tlb:
			print('%6x%4x %4s' % (tlb_tag, tlb_ind, tlb_res)),
		else:
			print('%6s%4s %4s' % ("", "", "")),


		if tlb_res == "hit ":
			print('%4s' % ""),
		elif self.config.virtual_add:
			print('%4s' % pt_res),
		else:
			print('    '),


		print('%4x %6x %3x %4s' % (p_num, dc_tag, dc_ind, dc_res)),

		if self.config.victim_cache:
			print('%6x %4s' % (vc_tag, vc_res))
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

	def calc_tlb_tag(self, val):
		shift = config.tlb_index

		mask = sys.maxint
		mask = mask << shift

		res = val.vp_num & mask

		res = res >> shift

		val.tlb_tag = res

	def calc_tlb_index(self, val):

		mask = 2 ** config.tlb_index - 1
		res = val.vp_num & mask

		val.tlb_ind = res
		
	"""tag for data cache calculation"""

	def calc_dc_tag(self, val):
		shift = config.d_cache_offset + config.d_cache_index

		mask = sys.maxint
		mask = mask << shift

		res = val.add & mask

		res = res >> shift

		val.dc_tag = res


	"""calculates the physical page number based on physical address"""

	def calc_phys_page(self, val):
		size = config.pt_offset
		
		mask = 2 ** 32 - 1
		mask = mask << size
		
		res = val.add & mask
		
		val.physical_page = res >> size

	"""calculate the victim cache tag"""

	def calc_victim_tag(self, val):

		# calculate size of the p_num
		size = config.d_cache_offset
		
		mask = 2 ** 32 - 1
		mask = mask << size
		
		res = val.add & mask

		
		val.victim_tag = res >> size


"""
	class for storing each trace data entry
"""

class TraceLine:

	def __init__(self, t, add):
		self.type = t
		self.add = int(add, 16)

		self.v_add = self.add

		self.vp_num = -1
		self.p_offset = -1

		self.dc_tag = -1
		self.dc_index = -1
		self.dc_offset = -1

		self.dc_res = "none"

		self.physical_page = -1

		self.victim_tag = -1

		self.victim_res = "miss"

		self.pt_res = "miss"

		self.tlb_tag = -1
		self.tlb_ind = -1
		self.tlb_res = "miss"

"""
	class for data cache entries
"""

class DataCacheEntry:

	def __init__(self, v, tag, vc_tag):
		self.v = v
		self.tag = tag

		self.lru = 0

		self.vc_tag = vc_tag

	def __str__(self):
		return str(str(self.v) + " " + str(self.tag))

"""
	Data cache for computing hits/misses
"""

class DataCache:

	def __init__(self, stats, config, data, victim):
		self.config = config
		self.data = data

		self.stats = stats

		self.victim = victim

		self.assoc = config.set_size_data
		self.size = config.num_sets_data

		self.entries = []

		self.init_cache()

		self.do_cache()

	def init_cache(self):
		
		for i in xrange(self.size):
			dum = list()
			
			for j in xrange(self.assoc):
				dum.append(DataCacheEntry(0, -1, -1))

			self.entries.append(dum)

	def print_cache(self):
		for i in xrange(self.size):
			print(i),

			for j in xrange(self.assoc):
				print(self.entries[i][j]),

			print("")

	def do_cache(self):
		# for each address go through and see if in cache
		# if not in cache then add in and add to phys page table

		for i in self.data:

			res = self.find_in_cache(i)

			if i.type == "W":
				self.stats.total_writes += 1
			else:
				self.stats.total_reads += 1

			if res:
				i.dc_res = "hit "
			else:
				i.dc_res = "miss"


	"""given an address goes to the index and sees if tag matches"""

	def find_in_cache(self, entry):
		
		cur = entry

		d_set = self.entries[cur.dc_index]

		# checks to see if in the victim cache because it was not in data cache

		in_victim_cache = self.victim.find_in_cache(cur)

		for i in d_set:
			if i.v is 1 and cur.dc_tag == i.tag:

				self.reset_and_inc(d_set, cur.dc_tag)

				stats.dc_hit += 1

				return True

		# if replacing a value in data cache must make the value True

		replace_index, evicted = self.find_index_replace(d_set)

		save = d_set[replace_index]

		stats.dc_miss += 1

		# add evicted number into the victim cache

		if evicted:
			victim.add_evicted(save.vc_tag)

		if not in_victim_cache:
			self.stats.main_mem_ref += 1

		# found place to replace, must get dc_tag and make sure lru is 0 and v is 1

		d_set[replace_index].v = 1
		d_set[replace_index].lru = 0
		d_set[replace_index].tag = cur.dc_tag
		d_set[replace_index].vc_tag = cur.victim_tag

		# if a block was evicted, store this value in the victim cache

		return False

	"""function to increment all lru values and reset the one that was just used"""

	def reset_and_inc(self, d_set, reset):

		for i in d_set:
			if i.v is 1:
				if i.tag is reset:
					i.lru = 0
				else:
					i.lru = i.lru + 1


	"""function to find index of replaceable value in the set"""

	def find_index_replace(self, d_set):

		ind = 0

		# look for a spot that is not valid

		for i in d_set:
			if i.v is 0:
				
				i.v = 1

				return ind, False

			ind += 1

		# find greatest LRU value and return the index of it in the d_set

		max_val = d_set[0]
		max_ind = 0

		ind = 0

		for i in d_set:
			if i.lru > max_val.lru:
				max_val = i
				max_ind = ind

			ind += 1

		return max_ind, True

"""
	Physical page table class
"""

class PhysicalPageTable:
	def __init__(self, config):
		self.config = config

		self.size = self.config.num_physical_pages
		self.pages = list()

		self.init_table()

	
	def init_table(self):
		for i in xrange(int(self.size)):
			self.pages.append(PhysicalPage())

	# find a page and return the page number

	def find_page(self):

		replace_page, evicted = self.find_index_replace()

		return replace_page, evicted

	"""function to increment all lru values and reset the one that was just used"""

	def inc(self):

		for i in self.pages:
			if i.v is 1:
				i.lru = i.lru + 1


	"""function to find index of replaceable value in the set"""

	def find_index_replace(self):

		ind = 0

		# look for a spot that is not valid

		for i in self.pages:
			if i.v is 0:
				
				i.v = 1

				return ind, False

			ind += 1

		# find greatest LRU value and return the index of it in the d_set

		max_val = self.pages[0]
		max_ind = 0

		ind = 0

		for i in self.pages:
			if i.lru > max_val.lru:
				max_val = i
				max_ind = ind

			ind += 1

		return max_ind, True


"""
	Physical page table entries class
	done in a round robin fashion
	LRU replacement
"""

class PhysicalPage:
	def __init__(self):
		self.v = 0
		self.lru = 0
		self.init_accesses = 0

"""
	Victim Cache entry class
"""

class VictimCacheEntry:

	def __init__(self, v, tag):
		self.v = v
		self.tag = tag

		self.lru = 0

	def __str__(self):
		return str(str(self.v) + " " + str(self.tag))

"""
	victim cache similar to data cache
"""

class VictimCache:

	def __init__(self, stats, config, data):
		self.stats = stats

		self.config = config
		self.data = data

		self.assoc = int(config.set_size_victim)
		self.size = 1

		self.entries = []

		self.init_cache()


	def init_cache(self):
		
		for i in xrange(self.size):
			dum = list()
			
			for j in xrange(self.assoc):
				dum.append(VictimCacheEntry(0, -1))

			self.entries.append(dum)

	def print_cache(self):
		for i in xrange(self.size):
			print(i),

			for j in xrange(self.assoc):
				print(self.entries[i][j]),

			print("")

	"""given an address goes to the index and sees if tag matches"""

	def find_in_cache(self, entry):
		
		cur = entry

		d_set = self.entries[0]

		for i in d_set:
			if i.v is 1 and cur.victim_tag == i.tag:
				self.reset_and_inc(d_set, cur.victim_tag)

				cur.victim_res = "hit "

				self.stats.v_hit += 1

				return True

		# miss so must find a place to add in the value

		cur.victim_res = "miss"

		self.reset_and_inc(d_set, -5)

		self.stats.v_miss += 1

		return False

	"""function to increment all lru values and reset the one that was just used"""

	def reset_and_inc(self, d_set, reset):

		for i in d_set:
			if i.v is 1:
				if i.tag == reset:
					#i.lru = 0
					i.v = 0
					i.tag = -1
				else:
					i.lru = i.lru + 1



	"""function to find index of replaceable value in the set"""

	def find_index_replace(self, d_set):

		ind = 0

		# look for a spot that is not valid

		for i in d_set:
			if i.v is 0:
				
				i.v = 1

				return ind

			ind += 1

		# find greatest LRU value and return the index of it in the d_set

		max_val = d_set[0]
		max_ind = 0

		ind = 0

		for i in d_set:
			if i.lru > max_val.lru:
				max_val = i
				max_ind = ind

			ind += 1

		return max_ind

	"""function to add the value that you evicted from the data cache"""

	def add_evicted(self, tag):
		
		replace_ind = self.find_index_replace(self.entries[0])

		self.entries[0][replace_ind].v = 1
		self.entries[0][replace_ind].lru = 0
		self.entries[0][replace_ind].tag = tag

class Statistics:

	def __init__(self, config):

		self.config = config

		self.v_miss = 0
		self.v_hit = 0

		self.pt_hit = 0
		self.pt_fault = 0

		self.tlb_hit = 0
		self.tlb_miss = 0

		self.dc_hit = 0
		self.dc_miss = 0

		self.l1_hit = 0
		self.l1_miss = 0

		self.total_reads = 0
		self.total_writes = 0

		self.main_mem_ref = 0
		self.pt_refs = 0
		self.disk_refs = 0

	def print_stats(self):

		total = self.dc_hit + self.dc_miss

		self.l1_hit = self.v_hit + self.dc_hit
		self.l1_miss = total - self.l1_hit

		print("\n\nSimulation statistics\n")

		print('dtlb hits        : ' + str(self.tlb_hit))
		print('dtlb misses      : ' + str(self.tlb_miss))
		if config.tlb:
			print('dtlb hit ratio   : %6.6f\n' % (float(self.tlb_hit)/total))
		else:
			print('dtlb hit ratio   : N/A\n')



		print('pt hits          : ' + str(self.pt_hit))
		print('pt faults        : ' + str(self.pt_fault))
		if config.virtual_add:
			print('pt hit ratio     : %6.6f\n' % (float(self.pt_hit)/total))
		else:
			print('pt hit ratio     : N/A\n')

		print('dc hits          : ' + str(self.dc_hit))
		print('dc misses        : ' + str(self.dc_miss))
		print('dc hit ratio     : %6.6f\n' % (float(self.dc_hit)/total))

		print('vc hits          : ' + str(self.v_hit))
		print('vc misses        : ' + str(self.v_miss))
		if config.victim_cache:
			print('vc hit ratio     : %6.6f\n' % (float(self.v_hit)/total))
		else:
			print('vc hit ratio     : N/A\n')

		print('L1 hits          : ' + str(self.l1_hit))
		print('L1 misses        : ' + str(self.l1_miss))
		print('L1 hit ratio     : %6.6f\n' % (float(self.l1_hit)/total))

		print('Total reads      : ' + str(self.total_reads))
		print('Total writes     : ' + str(self.total_writes))
		print('Ratio of reads   : %6.6f\n' % (float(self.total_reads)/total))

		print('main memory refs : ' + str(self.main_mem_ref))
		print('page table refs  : ' + str(self.pt_refs))
		print('disk refs        : ' + str(self.disk_refs))

"""
	virtual page table implementation
	will take a virtual address and convert it to a physical address
	with a member funciton
"""

class PageTable:

	def __init__(self, stats, config, dc, vc):

		self.stats = stats

		self.dc = dc

		self.vc = vc

		self.config = config

		self.size = int(self.config.num_virtual_pages)

		self.entries = list()

		# physical page table

		self.phys_table = PhysicalPageTable(self.config)

		self.init_table()

	def init_table(self):

		for i in xrange(self.size):
			self.entries.append(PageTableEntry())

	# take the virtual address then see if it has a page table value,
	# if it doesn't have a value then go to page table and use find a page
	# to assign to it

	def convert_to_phy(self, add):

		# check if valid entry in vpt

		# store the indexed value

		if add.tlb_res == "miss":
			self.stats.pt_refs += 1

		entry = self.entries[add.vp_num]

		# entry is valid, convert with the physical page instead of the virtual page #

		if entry.v:

			self.phys_table.inc()

			# reset lru for this page number

			self.phys_table.pages[entry.phys_page].lru = 0

			add.pt_res = "hit "

			if add.tlb_res == "miss":
				self.stats.pt_hit += 1

			return self.replace_virtual_num(entry.phys_page, add)


		else:

			entry.phys_page, evicted = self.phys_table.find_page()

			# find all virtual pages that have this phys_page and invalidate them

			if evicted:
				self.invalidate_pages(entry.phys_page)

			entry.v = 1

			self.stats.pt_fault += 1

			self.stats.disk_refs += 1

			return self.replace_virtual_num(entry.phys_page, add)

	"""
		takes in page and shifts that and XOR's with the address space pertaining to the num
	"""

	def replace_virtual_num(self, page, add):
		
		shift = config.pt_offset

		offset = add.p_offset

		new_add = (page << shift) | offset

		return new_add

	"""
		takes in phys page number and goes through all pages and invalidates them
	"""

	def invalidate_pages(self, page_num):

		for i in self.entries:
			if i.phys_page == page_num:
				i.v = 0



"""
	virtual page table entry
"""

class PageTableEntry:

	def __init__(self):

		self.phys_page = -1
		self.v = 0

"""
	TLB for address conversion
	valid - v
	virtual page number
	physical page number
"""

class TLB:

	def __init__(self, stats, config):
		self.config = config

		self.assoc = int(config.set_size)
		self.size = int(config.num_sets)

		self.entries = []

		self.init_cache()

	def init_cache(self):
		
		for i in xrange(self.size):
			dum = list()
			
			for j in xrange(self.assoc):
				dum.append(TLBEntry())

			self.entries.append(dum)

	"""given an address goes to the index and sees if tag matches"""

	def check_tlb(self, entry):
		
		cur = entry

		line = self.entries[cur.tlb_ind]

		for i in line:
			if i.v is 1 and cur.tlb_tag == i.tag:

				# if is valid and tag matches, reset and inc other lru's

				cur.tlb_res = "hit "

				stats.tlb_hit += 1
				
				self.reset_and_inc(line, cur.tlb_tag)

				return True

		# if not TLB bring it in and remove other value

		cur.tlb_res = "miss"

		stats.tlb_miss += 1

		replace_index, evicted = self.find_index_replace(line)

		line[replace_index].v = 1
		line[replace_index].lru = 0
		line[replace_index].tag = cur.tlb_tag
		line[replace_index].v_page = cur.vp_num

		return False

	"""function to increment all lru values and reset the one that was just used"""

	def reset_and_inc(self, d_set, reset):

		for i in d_set:
			if i.v is 1:
				if i.tag is reset:
					i.lru = 0
				else:
					i.lru = i.lru + 1


	"""function to find index of replaceable value in the set"""

	def find_index_replace(self, d_set):

		ind = 0

		# look for a spot that is not valid

		for i in d_set:
			if i.v is 0:
				
				i.v = 1

				return ind, False

			ind += 1

		# find greatest LRU value and return the index of it in the d_set

		max_val = d_set[0]
		max_ind = 0

		ind = 0

		for i in d_set:
			if i.lru > max_val.lru:
				max_val = i
				max_ind = ind

			ind += 1

		return max_ind, True

"""
	class for TLBEntry
"""

class TLBEntry:

	def __init__(self):

		self.v = 0
		self.tag = -1
		self.v_page = -1
		self.phys_page = -1


if __name__ == "__main__":
	config = Config("trace.config")

	stats = Statistics(config)

	pagetable = PageTable(stats, config)

	tlb = TLB(stats, config)

	data = TraceData(config, pagetable, tlb)
	data.take_trace()

	victim = VictimCache(stats, config, data.data)

	dcache = DataCache(stats, config, data.data, victim)


	data.print_all()

	stats.print_stats()





"""
	solution for cda5155 from andrew berg spring 2017 whalley
"""

"""
	class to read in the config and store the information
"""

import sys

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

	"""prints each entry into the config file"""

	def print_config(self):

		# data tlb info
		
		print("Data TLB contains " + self.num_sets + " sets.")
		print("Each set contains " + self.set_size + " entries.")
		"""TODO:"""
		print("Number of bits used for the index is " + "TODO. \n")

		# page table info
		
		print("Number of virtual pages is " + self.num_virtual_pages + ".")
		print("Number of physical pages is " + self.num_physical_pages + ".")
		print("Each page contains " + self.page_size + "bytes.")
		print("Number of bits used for the page table index is " + "TODO.")
		print("Number of bits used for the page offset is " + "TODO.")
		print("")

		# data cache info
		
		print("D-cache contains " + self.num_sets_data + " sets.")
		print("Each set contains " + self.set_size_data + " entries.")
		print("Each line is " + self.line_size + " sets.")
		print("Number of bits used for the index is " + "TODO.")
		print("Number of bits used for the offset is " + "TODO.")
		print("")

		# v-cache config

		print("Each V-cache set contains " + self.set_size_victim + " entries.")
		print("")

		# virtual addresses
		
		if self.virtual_add:
			print("The addresses read in are virtual addresses.")
		else:
			print("The addresses read in are physical addresses.")

		print("")


if __name__ == "__main__":
	config = Config("trace.config")

	config.print_config()
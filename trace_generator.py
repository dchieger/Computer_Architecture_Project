#!/usr/bin/env python3

import random

def generate_trace_file(filename, num_entries=1000, sequential_ratio=0.7):
	"""
	Generate a trace file with memory access patterns.
	
	Args:
		filename: Name of the trace file to create
		num_entries: Number of memory accesses to generate
		sequential_ratio: Ratio of sequential vs random accesses
	"""
	with open(filename, 'w') as f:
		base_addr = 0x1000  # Starting address
		
		for i in range(num_entries):
			# Decide if this will be a sequential or random access
			if random.random() < sequential_ratio:
				# Sequential access - increment base address
				addr = base_addr + (i * 4)  # 4 bytes per word
			else:
				# Random access within 1MB range
				addr = random.randint(0x1000, 0x100000)
				
			# Randomly choose between read (80%) and write (20%)
			operation = 'R' if random.random() < 0.8 else 'W'
			
			# Write the trace entry
			f.write(f"{hex(addr)[2:]} {operation}\n")
			
def generate_example_traces():
	"""Generate three different example trace files."""
	# Sequential memory access pattern (program code execution)
	generate_trace_file('trace_files/trace1_sequential.trc', num_entries=1000, sequential_ratio=0.9)
	
	# Random memory access pattern (data structure traversal)
	generate_trace_file('trace_files/trace2_random.trc', num_entries=1000, sequential_ratio=0.3)
	
	# Mixed memory access pattern
	generate_trace_file('trace_files/trace3_mixed.trc', num_entries=1000, sequential_ratio=0.6)
	
if __name__ == "__main__":
	generate_example_traces()
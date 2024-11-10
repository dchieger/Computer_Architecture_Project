import argparse
from dataclasses import dataclass
from typing import List, Optional
import random
import math

@dataclass
class CacheEntry:
    valid: bool = False
    dirty: bool = False
    tag: int = 0
    last_used: int = 0
    data: List[int] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = []

class CacheSet:
    def __init__(self, associativity: int, block_size: int):
        self.entries = [CacheEntry(data=[0] * block_size) for _ in range(associativity)]
        self.next_rr = 0  # For round-robin replacement
    
    def find_entry(self, tag: int) -> Optional[CacheEntry]:
        """Find an entry with the given tag in the set."""
        for entry in self.entries:
            if entry.valid and entry.tag == tag:
                return entry
        return None
    
    def get_replacement_entry(self, round_robin: bool) -> CacheEntry:
        """Get an entry for replacement using the specified policy."""
        if round_robin:
            entry = self.entries[self.next_rr]
            self.next_rr = (self.next_rr + 1) % len(self.entries)
            return entry
        else:
            # Random replacement
            return random.choice(self.entries)

class Cache:
    def __init__(self, config):
        self.block_size = config.block_size
        self.associativity = config.associativity
        self.round_robin = config.replacement_policy == 'rr'
        
        # Calculate number of sets
        self.num_sets = (config.cache_size * 1024) // (self.block_size * self.associativity)
        self.sets = [CacheSet(self.associativity, self.block_size) for _ in range(self.num_sets)]
        
        # Statistics
        self.reads = 0
        self.writes = 0
        self.hits = 0
        self.misses = 0
        
        # Calculate address bits
        self.offset_bits = int(math.log2(self.block_size))
        self.index_bits = int(math.log2(self.num_sets))
        self.tag_bits = 32 - self.offset_bits - self.index_bits
    
    def get_address_components(self, address: int) -> tuple:
        """Extract tag, index, and offset from address."""
        offset = address & ((1 << self.offset_bits) - 1)
        index = (address >> self.offset_bits) & ((1 << self.index_bits) - 1)
        tag = address >> (self.offset_bits + self.index_bits)
        return tag, index, offset
    
    def access(self, address: int, is_write: bool) -> bool:
        """Process a cache access. Returns True for hit, False for miss."""
        tag, index, _ = self.get_address_components(address)
        
        if is_write:
            self.writes += 1
        else:
            self.reads += 1
        
        entry = self.sets[index].find_entry(tag)
        if entry is not None:
            self.hits += 1
            if is_write:
                entry.dirty = True
            return True
        
        self.misses += 1
        entry = self.sets[index].get_replacement_entry(self.round_robin)
        entry.valid = True
        entry.tag = tag
        entry.dirty = is_write
        return False
    
    def print_stats(self):
        """Print cache statistics."""
        total_accesses = self.reads + self.writes
        hit_rate = (self.hits / total_accesses * 100) if total_accesses > 0 else 0
        
        print("\nCache Statistics:")
        print(f"Total Accesses: {total_accesses}")
        print(f"Reads: {self.reads}")
        print(f"Writes: {self.writes}")
        print(f"Hits: {self.hits}")
        print(f"Misses: {self.misses}")
        print(f"Hit Rate: {hit_rate:.2f}%")
        print(f"Miss Rate: {100-hit_rate:.2f}%")

class PageTable:
    def __init__(self, phys_mem_size: int):
        self.page_size = 4096  # 4KB pages
        self.num_pages = phys_mem_size * 1024 * 1024 // self.page_size
        self.page_table = {}
        self.next_frame = 0
    
    def translate(self, virtual_addr: int) -> Optional[int]:
        """Translate virtual address to physical address."""
        page_number = virtual_addr // self.page_size
        offset = virtual_addr % self.page_size
        
        if page_number not in self.page_table:
            if self.next_frame >= self.num_pages:
                return None  # Out of physical memory
            self.page_table[page_number] = self.next_frame
            self.next_frame += 1
        
        frame_number = self.page_table[page_number]
        return (frame_number * self.page_size) + offset

class ProcessManager:
    def __init__(self, config):
        self.processes = {}
        self.time_slice = config.time_slice
        self.phys_mem = PageTable(config.phys_mem)
    
    def add_process(self, pid: int):
        """Add a new process with its own page table."""
        self.processes[pid] = PageTable(self.phys_mem.num_pages)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Cache Simulator')
    parser.add_argument('-s', '--cache-size', type=int, required=True,
                      help='Cache size in KB (8 to 8192)')
    parser.add_argument('-b', '--block-size', type=int, required=True,
                      help='Block size in bytes (8 to 64)')
    parser.add_argument('-a', '--associativity', type=int, required=True,
                      help='Associativity (1, 2, 4, 8, or 16)')
    parser.add_argument('-r', '--replacement-policy', choices=['rr', 'rnd'], required=True,
                      help='Replacement policy (rr=Round Robin, rnd=Random)')
    parser.add_argument('-p', '--phys-mem', type=int, required=True,
                      help='Physical memory size in MB (1 to 4096)')
    parser.add_argument('-u', '--mem-used', type=int, required=True,
                      help='Percentage of physical memory used (0 to 100)')
    parser.add_argument('-n', '--time-slice', type=int, required=True,
                      help='Instructions per time slice (-1 for max)')
    parser.add_argument('-f', '--trace-files', nargs='+', required=True,
                      help='Trace files (1 to 3 files)')
    return parser.parse_args()

def process_trace_file(filename: str, cache: Cache, page_table: PageTable):
    """Process a single trace file."""
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Assuming trace format is: "address operation"
                # Modify this based on your actual trace file format
                parts = line.strip().split()
                if len(parts) >= 2:
                    address = int(parts[0], 16)  # Assuming hex address
                    operation = parts[1].upper()
                    
                    # Translate virtual to physical address
                    phys_addr = page_table.translate(address)
                    if phys_addr is None:
                        print(f"Page fault at address {hex(address)}")
                        continue
                    
                    # Access cache
                    cache.access(phys_addr, operation == 'W')
    except FileNotFoundError:
        print(f"Error: Could not open trace file {filename}")
    except Exception as e:
        print(f"Error processing trace file {filename}: {str(e)}")

def main():
    args = parse_arguments()
    
    # Validate arguments
    if not (8 <= args.cache_size <= 8192):
        raise ValueError("Cache size must be between 8 and 8192 KB")
    if not (8 <= args.block_size <= 64):
        raise ValueError("Block size must be between 8 and 64 bytes")
    if args.associativity not in [1, 2, 4, 8, 16]:
        raise ValueError("Associativity must be 1, 2, 4, 8, or 16")
    if not (1 <= args.phys_mem <= 4096):
        raise ValueError("Physical memory must be between 1 and 4096 MB")
    if not (0 <= args.mem_used <= 100):
        raise ValueError("Memory used percentage must be between 0 and 100")
    if len(args.trace_files) > 3:
        raise ValueError("Maximum of 3 trace files allowed")
    
    # Create cache and process manager
    cache = Cache(args)
    process_manager = ProcessManager(args)
    
    # Process each trace file
    for i, trace_file in enumerate(args.trace_files):
        print(f"\nProcessing trace file {i+1}: {trace_file}")
        process_manager.add_process(i)
        process_trace_file(trace_file, cache, process_manager.processes[i])
    
    # Print final statistics
    cache.print_stats()

if __name__ == "__main__":
    main()
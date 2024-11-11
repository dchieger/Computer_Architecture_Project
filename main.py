import argparse
import math


class CacheSimulator:
    def __init__(self, args):
        # Cache input parameters
        self.cache_size = args.cache_size * 1024  # Convert to bytes
        self.block_size = args.block_size
        self.associativity = args.associativity
        self.replacement_policy = args.replacement_policy
        self.phys_mem = args.phys_mem * 1024 * 1024  # Convert to bytes
        self.mem_used_percent = args.mem_used
        self.time_slice = args.time_slice

        # Calculate cache values
        self.total_blocks = self.cache_size // self.block_size
        self.total_rows = self.total_blocks // self.associativity

        # Calculate address bits
        self.offset_bits = int(math.log2(self.block_size))
        self.index_bits = int(math.log2(self.total_rows))
        self.tag_bits = 32 - self.offset_bits - self.index_bits

        # Calculate overhead
        self.valid_bit = 1
        self.dirty_bit = 1
        self.overhead_per_block = self.valid_bit + self.dirty_bit + self.tag_bits
        self.total_overhead = (
            self.overhead_per_block * self.total_blocks
        ) // 8  # Convert to bytes

        # Calculate implementation memory size
        self.implementation_memory = self.cache_size + self.total_overhead

        # Calculate physical memory values
        self.page_size = 4096  # 4KB pages
        self.num_physical_pages = self.phys_mem // self.page_size
        self.num_system_pages = (self.num_physical_pages * self.mem_used_percent) // 100
        self.page_table_entry_size = 4  # 32 bits = 4 bytes
        self.total_page_table_size = (
            self.num_physical_pages * self.page_table_entry_size
        )

    def print_cache_input_parameters(self):
        print("\n\n***** Cache Input Parameters *****\n\n")
        print(f"Cache Size: {self.cache_size // 1024}KB")
        print(f"Block Size: {self.block_size} bytes")
        print(f"Associativity: {self.associativity}")
        print(f"Replacement Policy: {self.replacement_policy.upper()}")
        print(f"Physical Memory: {self.phys_mem // (1024 * 1024)}MB")
        print(f"Percent Memory Used by System: {self.mem_used_percent}%")
        print(f"Instructions / Time Slice: {self.time_slice}")

    def print_cache_calculated_values(self):
        print("\n\n***** Cache Calculated Values *****\n\n")
        print(f"Total # Blocks: {self.total_blocks}")
        print(f"Tag Size: {self.tag_bits} bits")
        print(f"Index Size: {self.index_bits} bits")
        print(f"Total # Rows: {self.total_rows}")
        print(f"Overhead Size: {self.total_overhead} bytes")
        print(f"Implementation Memory Size: {self.implementation_memory} bytes")

        cost = self.implementation_memory * 0.15
        print(f"Cost: ${cost}")

    def print_physical_memory_calculated_values(self):
        print("\n\n***** Physical Memory Calculated Values ***** \n\n")
        print(f"Number of Physical Pages: {self.num_physical_pages}")
        print(f"Number of Pages for System: {self.num_system_pages}")
        print(f"Size of Page Table Entry: {self.page_table_entry_size} bytes")
        print(f"Total RAM for Page Table(s): {self.total_page_table_size} bytes")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Cache Simulator")
    parser.add_argument(
        "-s",
        "--cache-size",
        type=int,
        required=True,
        help="Cache size in KB (8 to 8192)",
    )
    parser.add_argument(
        "-b",
        "--block-size",
        type=int,
        required=True,
        help="Block size in bytes (8 to 64)",
    )
    parser.add_argument(
        "-a",
        "--associativity",
        type=int,
        required=True,
        help="Associativity (1, 2, 4, 8, or 16)",
    )
    parser.add_argument(
        "-r",
        "--replacement-policy",
        choices=["rr", "rnd"],
        required=True,
        help="Replacement policy (rr=Round Robin, rnd=Random)",
    )
    parser.add_argument(
        "-p",
        "--phys-mem",
        type=int,
        required=True,
        help="Physical memory size in MB (1 to 4096)",
    )
    parser.add_argument(
        "-u",
        "--mem-used",
        type=int,
        required=True,
        help="Percentage of physical memory used (0 to 100)",
    )
    parser.add_argument(
        "-n",
        "--time-slice",
        type=int,
        required=True,
        help="Instructions per time slice (-1 for max)",
    )
    parser.add_argument(
        "-f",
        "--trace-files",
        nargs="+",
        required=True,
        help="Trace files (1 to 3 files)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

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

    print("\nCache Simulator CS 3853 Fall 2024 – Group #06\n")

    simulator = CacheSimulator(args)
    simulator.print_cache_input_parameters()
    simulator.print_cache_calculated_values()
    simulator.print_physical_memory_calculated_values()


if __name__ == "__main__":
    main()

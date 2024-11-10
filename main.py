def print_cache_input_parameters():
    print('\n\n***** Cache Input Parameters *****\n\n')

    print('Cache Size:')
    print('Block Size:')
    print('Associativity:')
    print('Replacement Policy:')
    print('Physical Memory:')
    print('Percent Memory Used by System:')
    print('Instructions / Time Slice:')

def print_cache_calculated_values():
    print('\n\n***** Cache Calculated Values *****\n\n')

    print('Total # Blocks:')
    print('Tag Size:')
    print('Index Size:')
    print('Total # Rows:')
    print('Overhead Size:')
    print('Implementation Memory Size:')
    print('Cost')

def print_physical_memeory_calculated_values():
    print('\n\n***** Physical Memory Calculated Values ***** \n\n')
    print('Number of Physical Pages:')
    print('Number of Pages for System:')
    print('Size of Page Table Entry:')
    print('Total RAM for Page Table(s):')

def main():
    print('Cache Simulator CS 3853 Fall 2024 – Group #??\n')
    print_cache_input_parameters()
    print_cache_calculated_values()
    print_physical_memeory_calculated_values()

if __name__ == "__main__":
    main()
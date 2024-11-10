import sys


def main():
    a = sys.argv[1:]
    print(a)
    counter = 0
    trace_file = []
    size = ""
    block_size = ""
    associativity = ""
    replacement_policy = ""
    pyshical_mem = ""
    pyshical_mem_used = ""
    Time_slice = ""

    while counter < len(a) - 1:
        command = a[counter]
        print(command)
        match command:
            case "-s":
                print("Cache Size: ", a[counter + 1])
                size = a[counter + 1]
            case "-b":
                print("Block Size: ", a[counter + 1])
                block_size = a[counter + 1]
            case "-a":
                print("Associativity: ", a[counter + 1])
                associativity = a[counter + 1]
            case "-r":
                print("Replacement Policy: ", a[counter + 1])
                replacement_policy = a[counter + 1]
            case "-p":
                print("Physical Memory: ", a[counter + 1])
                pyshical_mem = a[counter + 1]
            case "-u":
                print("Physical Memory Used By System: ", a[counter + 1])
                pyshical_mem_used = a[counter + 1]
            case "-n":
                print("Instructions / Time Slice: ", a[counter + 1])
                Time_slice = a[counter + 1]
            case "-f":
                print("Trace File: ", a[counter + 1])
                trace_file.append(a[counter + 1])
            case _:
                print("Invalid command")
        counter += 2

    print("Cache Simulator - CS 3853 - Instructor Version: 2.11 \n")
    print(f"Trace Files: {trace_file} \n")
    print("***** Cache Input Parameters *****\n")
    print(f"Cache Size: {size} KB\n")
    print(f"Block Size: {block_size} bytes\n")
    print(f"Associativity: {associativity} \n")
    print(f"Replacement Policy: {replacement_policy} \n")
    print(f"Physical Memory: {pyshical_mem} \n")
    print(f"Physical Memory Used By System: {pyshical_mem_used} \n")
    print(f"Instructions / Time Slice: {Time_slice}\n")


main()

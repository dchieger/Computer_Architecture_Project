import sys


def main():
    a = sys.argv[1:]
    print(a)
    counter = 1
    while counter < len(a - 1):
        command = a[counter]
        match command:
            case "-s":
                size = a[counter + 1]
            case "-b":
                block_size = a[counter + 1]
            case "-a":
                associativity = a[counter + 1]
            case "-r":
                replacement_policy = a[counter + 1]
            case "-p":
                pyshical_mem = a[counter + 1]
            case "-u":
                pyshical_mem_used = a[counter + 1]
            case "n":
                Time_slice = a[counter + 1]
            case "-f":
                trace_file = a[counter + 1]
            case _:
                print("Invalid command")
        counter += 2
    print("Cache Simulator - CS 3853 - Instructor Version: 2.11 \n")
    print("Trace Files:/n " + trace_file)
    print("***** Cache Input Parameters *****/n")
    print("Cache Size: " + size + "KB/n")
    print("Block Size: " + block_size + "bytes/n")
    print("Associativity: " + associativity + "/n")
    print("Replacement Policy: " + replacement_policy + "/n")
    print("Physical Memory:" + pyshical_mem + "/n")
    print("Physical Memory Used By System: " + pyshical_mem_used + "/n")
    print("Instructions / Time Slice: " + Time_slice + "/n")

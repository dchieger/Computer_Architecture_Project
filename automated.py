import xlsxwriter
import subprocess
import re
import glob


def writeSheet(lines, worksheet, row):
    col = 0
    #  get the variables from the output of the cache simulator
    for line in lines:
        cacheSize = re.search(cacheSizeRGX, line)
        blockSize = re.search(blockSizeRGX, line)
        associativity = re.search(associativityRGX, line)
        replacementPolicy = re.search(replacementPolicyRGX, line)
        physicalMemory = re.search(physicalMemoryRGX, line)
        percentMemoryUsed = re.search(percentMemoryUsedRGX, line)
        timeSlice = re.search(timeSliceRGX, line)
        totalBlocks = re.search(totalBlocksRGX, line)
        tagSize = re.search(tagSizeRGX, line)
        indexSize = re.search(indexSizeRGX, line)
        totalNumberOfRows = re.search(totalNumberRowsRGX, line)
        overheadSize = re.search(overheadSizeRGX, line)
        implementationMemory = re.search(implementationMemoryRGX, line)
        cost = re.search(costRGX, line)
        physicalPages = re.search(physicalPagesRGX, line)
        systemPages = re.search(systemPagesRGX, line)
        pageTableEntrySize = re.search(pageTableEntrySizeRGX, line)
        totalRam = re.search(totalRamRGX, line)
        totalCahceAccess = re.search(totalCahceAccessRGX, line)
        intstructionBytes = re.search(intstructionBytesRGX, line)
        srcDstBytes = re.search(srcDstBytesRGX, line)
        cacheHit = re.search(cacheHitRGX, line)
        cacheMiss = re.search(cacheMissRGX, line)
        compulsoryMiss = re.search(compulsoryMissRGX, line)
        conflictMiss = re.search(conflictMissRGX, line)
        hitRate = re.search(hitRateRGX, line)
        missRate = re.search(missRateRGX, line)
        cpi = re.search(cpiRGX, line)
        unusedCacheSpace = re.search(unusedCacheSpaceRGX, line)
        unusedCacheBlocks = re.search(unusedCacheBlocksRGX, line)
        physicalPagesUsed = re.search(physicalPagesUsedRGX, line)
        pagesAvailable = re.search(pagesAvailableRGX, line)
        virtualPagesMapped = re.search(virtualPagesMappedRGX, line)
        pageTableHits = re.search(pageTableHitsRGX, line)
        pagesFromFree = re.search(pagesFromFreeRGX, line)
        pageTableFaults = re.search(pageTableFaultsRGX, line)
        usedPageTableEntries = re.search(usedPageTableEntriesRGX, line)
        pageTableWasted = re.search(pageTableWastedRGX, line)
        # write the variables to the excel sheet
        variables = {
            "Cache Size": cacheSize,
            "Block Size": blockSize,
            "Associativity": associativity,
            "Replacement Policy": replacementPolicy,
            "Physical Memory": physicalMemory,
            "Percent Memory Used by System": percentMemoryUsed,
            "Instructions / Time Slice": timeSlice,
            "Total # Blocks": totalBlocks,
            "Tag Size": tagSize,
            "Index Size": indexSize,
            "Total # Rows": totalNumberOfRows,
            "Overhead Size": overheadSize,
            "Implementation Memory Size": implementationMemory,
            "Cost": cost,
            "Number of Physical Pages": physicalPages,
            "Number of Pages for System": systemPages,
            "Size of Page Table Entry": pageTableEntrySize,
            "Total RAM for Page Table(s)": totalRam,
            "Total Cache Accesses": totalCahceAccess,
            "Instruction Bytes": intstructionBytes,
            "SrcDst Bytes": srcDstBytes,
            "Cache Hits": cacheHit,
            "Cache Misses": cacheMiss,
            "Compulsory Misses": compulsoryMiss,
            "Conflict Misses": conflictMiss,
            "Hit Rate": hitRate,
            "Miss Rate": missRate,
            "CPI": cpi,
            "Unused Cache Space": unusedCacheSpace,
            "Unused Cache Blocks": unusedCacheBlocks,
            "Physical Pages Used By SYSTEM": physicalPagesUsed,
            "Pages Available to User": pagesAvailable,
            "Virtual Pages Mapped": virtualPagesMapped,
            "Page Table Hits": pageTableHits,
            "Pages from Free": pagesFromFree,
            "Page Table Faults": pageTableFaults,
            "Used Page Table Entries": usedPageTableEntries,
            "Page Table Wasted": pageTableWasted,
        }
        # get the values of the variables and write them to the excel sheet
        for var in variables:
            if variables[var]:
                worksheet.write(row, col, variables[var].group(1))
                col += 1


# create the excel workbook
workbook = xlsxwriter.Workbook("automated.xlsx")
# that will be ran for each file
cacheSizes = [
    "8",
    "64",
    "256",
    "1024",
]
blockSizes = ["8", "16", "64"]
replacementPolicies = ["rr", "rnd"]
associativity = "4"
physicalMemories = "1024"
pysicalMemUses = "75"
timeSlices = "100"
files = glob.glob("*.trc")
# columns for the excel sheet
columns = [
    "Cache Size",
    "Block Size",
    "Associativity",
    "Replacement Policy",
    "Physical Memory",
    "Percent Memory Used by System",
    "Instructions / Time Slice",
    "Total # Blocks",
    "Tag Size",
    "Index Size",
    "Total # Rows",
    "Overhead Size",
    "Implementation Memory Size",
    "Cost",
    "Number of Physical Pages",
    "Number of Pages for System",
    "Size of Page Table Entry",
    "Total RAM for Page Table(s)",
    "Total Cache Accesses",
    "Instruction Bytes",
    "SrcDst Bytes",
    "Cache Hits",
    "Cache Misses",
    "Compulsory Misses",
    "Conflict Misses",
    "Hit Rate",
    "Miss Rate",
    "CPI",
    "Unused Cache Space",
    "Unused Cache Blocks",
    "Physical Pages Used By SYSTEM",
    "Pages Available to User",
    "Virtual Pages Mapped",
    "Page Table Hits",
    "Pages from Free",
    "Page Table Faults",
    "Used Page Table Entries",
    "Page Table Wasted",
]
# regex for the variables
cacheSizeRGX = r"Cache Size:\s([0-9]+)KB"
blockSizeRGX = r"Block Size:\s([0-9]+)"
associativityRGX = r"Associativity:\s([0-9]+)"
replacementPolicyRGX = r"Replacement Policy:\s([a-zA-Z]+)"
physicalMemoryRGX = r"Physical Memory:\s([0-9]+)MB"
percentMemoryUsedRGX = r"Percent Memory Used by System:\s([0-9]+)%"
timeSliceRGX = r"Instructions \/ Time Slice:\s([0-9]+)"
totalBlocksRGX = r"Total # Blocks:\s([0-9]+)"
tagSizeRGX = r"Tag Size:\s([0-9]+)\sbits"
indexSizeRGX = r"Index Size:\s([0-9]+)\sbits"
totalNumberRowsRGX = r"Total # Rows:\s([0-9]+)"
overheadSizeRGX = r"Overhead Size:\s([0-9]+)\sbytes"
implementationMemoryRGX = r"Implementation Memory Size:\s([0-9]+)\sbytes"
costRGX = r"Cost:\s\$([0-9]+\.[0-9]+)"
physicalPagesRGX = r"Number of Physical Pages:\s([0-9]+)"
systemPagesRGX = r"Number of Pages for System:\s([0-9]+)"
pageTableEntrySizeRGX = r"Size of Page Table Entry:\s([0-9]+)\sbytes"
totalRamRGX = r"Total RAM for Page Table\(s\):\s([0-9]+\.[0-9]+)\sbytes"
totalCahceAccessRGX = r"Total Cache Accesses:\s+([0-9]+)"
intstructionBytesRGX = r"Instruction Bytes:\s+([0-9]+)"
srcDstBytesRGX = r"SrcDst Bytes:\s+([0-9]+)"
cacheHitRGX = r"Cache Hits:\s+([0-9]+)"
cacheMissRGX = r"Cahce Misses:\s+([0-9]+)"
compulsoryMissRGX = r"Compulsory Misses:\s+([0-9]+)"
conflictMissRGX = r"Conflict Misses:\s+([0-9]+)"
hitRateRGX = r"Hit Rate:\s+([0-9]+\.[0-9]+)%"
missRateRGX = r"Miss Rate:\s+([0-9]+\.[0-9]+)%"
cpiRGX = r"CPI:\s+(.*)"
unusedCacheSpaceRGX = r"Unused Cache Space:\s+(.*)"
unusedCacheBlocksRGX = r"Unused Cache Blocks:\s+(.*)"
physicalPagesUsedRGX = r"Physical Pages Used By SYSTEM:\s+([0-9]+)"
pagesAvailableRGX = r"Pages Available to User:\s+([0-9]+)"
virtualPagesMappedRGX = r"Virtual Pages Mapped:\s+([0-9]+)"
pageTableHitsRGX = r"Page Table Hits:\s+([0-9]+)"
pagesFromFreeRGX = r"Pages from Free:\s+([0-9]+)"
pageTableFaultsRGX = r"Page Table Faults:\s+([0-9]+)"
usedPageTableEntriesRGX = r"Used Page Table Entries:\s+([0-9]+)"
pageTableWastedRGX = r"Page Table Wasted:\s+([0-9]+)"
# automate the cache simulator
for i in range(len(files)):
    row = 0
    col = 0

    worksheet = workbook.add_worksheet(files[i])
    for column in columns:
        worksheet.write(row, col, column)
        col += 1
    col = 0
    row += 1

    for rp in replacementPolicies:
        for blkSz in blockSizes:
            for cz in cacheSizes:
                proc = subprocess.run(
                    [
                        "python3",
                        "cache_simulator.py",
                        "-s",
                        cz,
                        "-b",
                        blkSz,
                        "-a",
                        associativity,
                        "-r",
                        rp,
                        "-p",
                        physicalMemories,
                        "-u",
                        pysicalMemUses,
                        "-n",
                        timeSlices,
                        "-f",
                        files[i],
                    ],
                    stdout=subprocess.PIPE,
                )

                writeSheet(proc.stdout.decode("utf-8").splitlines(), worksheet, row)

                row += 1
workbook.close()

Arguments
`-s 512 -b 16 -a 4 -r rr -p 1024 -u 75 -n 100 -f trace1_sequential.trc trace2_random.trc trace3_mixed.trc`

MileStone2 RUN COMMAND

python3 cache_simulator.py -s 512 -b 16 -a 4 -r rr -p 1024 -u 75 -n 100 -f TestTrace.trc

MileStone 3 / run the cache simulator once run command:
python3 cache_simulator.py -s 512 -b 16 -a 4 -r rr -p 1024 -u 75 -n 100 -f TestTrace.trc -f TinyTrace.trc -f Trace1.trc

To run automation script that looks for any trace files and runs in multiple cache configurations and export them to a excel sheet run command:

python3 automated.py

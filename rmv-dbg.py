import fileinput
import sys
import os

# script to remove debugging symbols from ga.py

for line in fileinput.input('G0GA.py', inplace=True):
	if 'debugging-symbol' in line:
		line = ''
	sys.stdout.write(line)

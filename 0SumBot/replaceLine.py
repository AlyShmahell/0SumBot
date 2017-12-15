import sys
import fileinput
for line in fileinput.input('test.txt', inplace=True):
    if 'hey' in line:
        line = 'foo: pee\n'
    sys.stdout.write(line)

#!/usr/bin/env python3.5

### This script will create a file for use in backtracking sequences to organs
### from which those sequences were isolated. Outputs a tab delineated file 
### with sequence names and organs.
###
### Run in command line by <script name> <output file name> 
### Recommended to run in directory with fastas to avoid confusion in indicating
### fastas, will also allow for tab complete (not in other directories).
###
### For issues with this script contact Alex Wixom at awixom18@gmail.com

from sys import argv as args
import readline
import glob

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
#readline.parse_and_bind("tab: complete")

script, output = args

dict = {}

start = input('Do you have a fasta to add (yes/no): ')
while start != 'yes' or 'no':
    if start == 'yes':
        fasta = input('What is the name of the fasta file? ')
        organ = input('From which organ did these sequences originate? ')
        with open(fasta, 'r') as fa:
            for line in fa:
                if line.startswith('>'):
                    dict[line.split()[0].translate(str.maketrans('','','>'))] = organ
        start = input('Do you have another fasta to add (yes/no): ')
    elif start == 'no':
        print('Finished dictionary!')
        with open(output, 'w') as out:
            for key in dict.keys():
                print('%s\t%s' % (key, dict[key]), file=out)
        break
    else:
        print('I think you are confused. Type yes or no')
        start = input('Do you have a fasta to add (yes/no): ')

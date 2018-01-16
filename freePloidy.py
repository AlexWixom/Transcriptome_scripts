#!/usr/bin/env python3.5

### This script will parse output from freebayes to help determine ploidy
### of an organism using a transcriptome and short read sequences to find
### allelic specific SNPs.
### For issues contact Alex Wixom at awixom18@gmail.com

import pandas as pd
import numpy as np
import sys
from sys import argv as args

##################################
#Modules
def searchDict(myDict, wanted):
	found = set()
	for key in myDict:
		for value in myDict[key]:
			for item in wanted:
				if item in value:
					found.add(key)
	return found
##################################

script, vcf, output = args

data = pd.read_table(vcf, comment='#', header=None, )

expand = data[9].str.split(':', expand=True)
expand.columns = data[8][1].split(':')

combined = pd.concat([data[:], expand[:]], axis=1)

genotype = combined[[0, 'GT']]

gts = genotype['GT'].unique().tolist()
print('\nFound genotypes (within quotations and separated by a comma):\n')
print(gts)

gt = [x for x in input('\nIf genotype(s) listed above is/are of interest, type each separated by a space: ').split()]

ids = genotype[0].unique().tolist()

print('\nMaking file with all sequences and genotypes.')
genoDict = {}
for seqID in ids:
    count = genotype.loc[genotype[0].isin([seqID])]['GT'].value_counts().to_dict()
    genoDict[seqID] = count

with open(output, 'w') as f:
    for key in genoDict.keys():
        print('%s\n%s' % (key, genoDict[key]), file=f)

print('\nMaking separate file including just %s genotype' % ([x for x in gt]))
want = searchDict(genoDict, gt)
with open('wantedGenotype.txt', 'w') as f:
    for id in want:
        print('%s\n%s' % (id, genoDict[id]), file=f)


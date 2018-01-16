#!/usr/bin/env python3.5

### This script will output a heatmap of sequences that have been clustered 
### and subsequentely backtracked to the organs they were sequenced from. 
### Suggest performing searches for wanted sequences using the file created by 
### createHeatmapFile.py and then inputing the lines with wanted information into this script. 
### Contact Alex Wixom: awixom18@gmail.com for issues with script

from sys import argv as args
from matplotlib import pyplot as plt
from matplotlib import figure
import numpy as np
import seaborn as sns
import pandas as pd

### Requires the file created from createHeatmapFile.py, a name for the CSV file created, 
### and the name for the file heatmap that it will output.
script, masterfile, output = args

organs= ['Leaf', 'Roots', 'Stems', 'Buds', ]

### Parses master file to a dictionary that has counts for each cluster that has been 
### backtracked to its organ tied to each sequence ID
with open(masterfile, 'r' ) as master:
    heatmapdict = {}
    for line in master:
        ID, organ, bin, annotation, cluster = line.rstrip().split('\t')
        organCounts = [organ.count(x) for x in organs ]
        heatmapdict[ID] = organCounts
    #print("%s" % (heatmapdict.items(), ))

### Creates a pandas DataFrame from the dictionary, says sequence IDs are the index
backtrackDF = pd.DataFrame.from_dict(data = heatmapdict, orient = 'index', )
backtrackDF.columns = organs
backtrackDF.index.name = 'Sequence ID'


### Uses Seaborn to plot a heatmap using the array
fig, ax = plt.subplots(figsize=(4,2.5))
ax.set_aspect('auto')
#heatmap = sns.heatmap(backtrackDF, annot=False, yticklabels=False, ax=ax )
heatmap = sns.heatmap(backtrackDF, annot=False, annot_kws={"size":5}, fmt="d", linewidths=0)
### Rotates the labels to horizontal
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation='horizontal', fontsize=5)


### Moves the adjusted labels figure to a new object for saving
heatmapfig = heatmap.get_figure()

### Saves the figure using supplied output naming
heatmapfig.savefig(output, bbox_inches='tight', dpi=600)
heatmapfig.clf()

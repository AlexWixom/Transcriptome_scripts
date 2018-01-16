#!/usr/bin/env python3
### Create master file for heatmap.
### For issues contact Alex Wixom at awixom18@gmail.com

from sys import argv as args

script, backtrack, Annotations, output = args

### REWRITE FOR NEW OUTPUT
with open(backtrack, 'r' ) as back:
    clusterBack = {}
    for line in back:
        cluster, organ = line.rstrip().split('\t')
        #print(organ, )
        clusterBack[cluster] = organ.split(', ')
        
#print(information)
                
with open(Annotations, 'r') as mercator:
    annotations = {}
    information = []
    for eachLine in mercator:
        eachLine = eachLine.translate({ord(c): None for c in "'"})
        bincode, bin, identity, annotation, type = eachLine.rstrip('\n').split('\t')
        if identity[0:1].isalpha() == True and identity[1:2].isnumeric() == True:
            #print(identity[1:2])
            annotations[identity] = {'bin':bin, 'annotation':annotation, }
        else:
            continue
    #print(annotations, )
    for ident in annotations.keys(): 
        #REDO TO TAKE ONLY ONE INPUT DICT #print( "%s\t%s\t%s\t%s\t%s\n" % (ident, (archCluster[ident]), clusterBack[archCluster[ident]], annotations[ident]['bin'], annotations[ident]['annotation'], ))
        information.append('\t'.join([ident, ', '.join(x for x in clusterBack[ident]), annotations[ident]['bin'], annotations[ident]['annotation'], ]))
    #print(information)
            
with open(output, 'w') as masterfile:
    for line in information:
        print("%s" % (line), file=masterfile)
masterfile.close()

### CHECK FOR NO SCREW UPS
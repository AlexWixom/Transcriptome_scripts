#!/usr/bin/env python3.5

### Uses CD-HIT-EST clust files and seqByOrgans output to 
### backtrack sequences to organs. 

from sys import argv as args

script, cluster90, cluster100, seqByOrgansOutput, output = args

def read_cluster(clust_list):
    name, seq = None, []
    for line in clust_list:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line + ' ')
    if name: yield (name, ''.join(seq))

def clustToSeq(cluster_file):
    list = []
    with open(cluster_file, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                list.append(line)
            else: 
                line = line.translate(str.maketrans('','', '>.'))
                column = line.split()
                trueLengths = column[1][:-3]
                ID, reads, length = column[2].split('/')
                if column[3].startswith('*'):
                    list.append('/'.join([ID, reads, trueLengths]))
    keptSeqDict = {}
    for clust, seq in read_cluster(list):
        kept = clust, seq 
        keptSeqDict[kept[0].translate(str.maketrans('','','>'))] = seq.rstrip()
    return keptSeqDict

def cdhitClustToDict(cluster_file, clustToSeqDict):
    list = []
    with open(cluster_file, 'r') as clust:
        for line in clust:
            if line.startswith('>'):
                list.append(line.rstrip())
            else:
                line = line.translate(str.maketrans('','','>.*'))
                column = line.split()
                trueLengths = column[1][:-3]
                ID, reads, length = column[2].split('/')
                list.append('/'.join([ID, reads, trueLengths]))
    finalDict = {}       
    for clust, seq in read_cluster(list):
        cluster = clust.translate(str.maketrans('','','>')), seq
        #print('%s\t%s' % (cluster[0], cluster[1]))
        finalDict[clustToSeqDict[cluster[0]]] = set(cluster[1].split())
    return finalDict

print('Opening seqByOrgansOutput file.\n')
with open(seqByOrgansOutput, 'r') as sbo:
    sboDict = {}
    for line in sbo:
        seq, organ = line.split('\t')
        sboDict[seq] = organ

print('Opening CD-HIT-EST file.\n')
cts90 = clustToSeq(cluster90)

print('Opening CD-HIT-EST file.\n')
cts100 = clustToSeq(cluster100)

print('Creating dictionaries.\n')
clust90 = cdhitClustToDict(cluster90, cts90)

clust100 = cdhitClustToDict(cluster100, cts100)

print('Backtracking through dictionaries.\n')
with open(output, 'w') as out:
    for x in clust90.keys():
        list = []
        for y in clust90[x]:
            for value in clust100[y]:
                list.append(sboDict[value].rstrip())
        print('%s\t%s' % (x, ', '.join(z for z in list)), file=out)



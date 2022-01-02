#!/usr/bin/env python
#################################################################################
#
#
################################################################################# 

from scapy.all import *
import numpy as np
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='output path')
parser.add_argument('-c', required=True, help='classification')
args = parser.parse_args()

# extract argument value
inputfile = args.i
outputfile = args.o
classification =int(args.c)


#read the pcap file and extract the features for each packet
results = []
all_packets = rdpcap(inputfile)
for packet in all_packets:
    size =  len(packet)
    try:
        proto = packet.proto
    except AttributeError:
        proto = 0
    try:
        sport = packet.sport
        dport = packet.dport
    except AttributeError:
        sport = 0
        dport = 0

    proto = int(proto)
    sport = int(sport)
    dport = int(dport)

    metric = [proto,sport,dport,classification]
    results.append(metric)
results = (np.array(results)).T

# store the features in the dataframe
dataframe = pd.DataFrame({'protocl':results[0],'src':results[1],'dst':results[2],'classfication':results[3]})
columns = ['protocl','src','dst','classfication']

# save the dataframe to the csv file, if not exsit, create one.
if os.path.exists(outputfile):
    dataframe.to_csv(outputfile,index=False,sep=',',mode='a',columns = columns, header=False)
else:
    dataframe.to_csv(outputfile,index=False,sep=',',columns = columns)



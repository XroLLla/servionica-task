#!/usr/bin/env python

import numpy as np
import pylab
import matplotlib.pyplot as plt
import json

WATCH_DIR = '/home/parallels/Desktop/task2015/'
WATCH_FILE = 'test_data.json'


def viz():
    with open(WATCH_DIR + WATCH_FILE) as data_file:
        data = json.load(data_file)
    iter_count = len(data)
    # column width
    width = 0.7
    # For each state of the system take static of RAM and CPU
    for index, iteration in enumerate(data):
        RAM = []
        CPU = []
        c_nodes = len(iteration)
        node_n_list = np.arange(c_nodes)
        # Append information to the lists
        for node in iteration:
            RAM.append(iteration[node]['mem'])
            CPU.append(iteration[node]['cpu'])
        # create windows for graphics
        pylab.subplot(1, iter_count, index+1)
        # Set a place for statistics CPU and RAM
        place_holder1 = np.arange(1, len(data[index])*2, 2)
        place_holder2 = np.arange(0, len(data[index])*2, 2)
        # Create a columnar Diagram to iterate
        ram_stat = plt.bar(place_holder1, RAM, width, color='red')
        cpu_stat = plt.bar(place_holder2, CPU, width, color='blue')
        # Title of each graphics
        # plt.title('22/02/2014\n15:'+str(num_iter)+"0:00")
        plt.title('Iteration '+str(index))
        # marks on the x-axis
        plt.xticks((width+(1-width)/2)+2*node_n_list,
                   [node for node in iteration],
                   rotation='vertical')
        # marks on the x-axis
        plt.ylim(0, 0.5)
        # Setting the display window graphics
        plt.subplots_adjust(left=0.06,
                            bottom=0.3,
                            right=0.97,
                            top=0.93,
                            wspace=0.3)
        # Legend for graphics
        plt.legend((ram_stat[0], cpu_stat[0]), ('RAM', 'CPU'), loc=9)
    plt.show()

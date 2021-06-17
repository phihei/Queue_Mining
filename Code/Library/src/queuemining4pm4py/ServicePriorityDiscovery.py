import random

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
# import networkx as nx
import pm4py.objects.dfg.utils.dfg_utils as pm4pydfg
import pm4py

# import xes_to_nx_utilities
import statistics_logs
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.objects.log.util import interval_lifecycle
from pm4py.statistics.passed_time.log import algorithm
from pm4py.util import exec_utils, constants
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY
from datetime import datetime, timedelta
from pm4py.objects.log.exporter.xes import exporter as xes_expoter
from enum import Enum

from pm4py.algo.discovery.performance_spectrum.variants import dataframe, log, dataframe_disconnected, log_disconnected
from pm4py.util import exec_utils
import pkgutil
from enum import Enum
from pm4py.util import constants
from pm4py.algo.discovery.performance_spectrum import algorithm as performance_spectrum



def ServicePriorityDiscovery(log, activities):

    if log is None:
        raise TypeError("A PM4PY Event Log is required.")
    if type(log) != pm4py.objects.log.obj.EventLog:
        raise TypeError("A PM4PY Event Log is required.")


    dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    df_activities = dfg.keys()

    if(len(activities)>1):
        for i in end_activities:
            if(i==activities[0]):
                raise TypeError("First activity can not be the end activity of the log")

        for i in start_activities:
            if(i==activities[1]):
                raise TypeError("Second activity can not be the first activity of the log")




    if(len(activities)==1):

        for i in start_activities:
            if(i==activities[0]):
                raise TypeError("Single activity can not be the first activity of the log")



        # print("1")
        df_activities_list=[]

        # activity= "examine casually"
        for i,j in df_activities:
            # print(j,activities)
            if(j==activities[0]):
                df_activities_list.append(i)
                # print(df_activities_list)

        for i in  range(len(df_activities_list)):
            new_activity=[]
            new_activity.append(df_activities_list[i])
            new_activity.append(activities[0])
            # print(new_activity)
            Perf(log,new_activity)

    else:
        Perf(log,activities)





def Perf(log, activities):


    perf_spectrum = performance_spectrum.apply(log, activities)

    Negative = 0
    Positive = 0
    for i in range(0, len(perf_spectrum['points']) - 1):
        value = perf_spectrum["points"][i + 1][1] - perf_spectrum["points"][i][1]
        # print(value)
        if (value > 0):
            Positive = Positive + 1
        else:
            Negative = Negative + 1

    # print(Negative)
    # print(Positive)
    print(activities)
    if Negative == 0 and Positive > 0:
        print("Fifo")

    elif Negative > 0 and Positive == 0:
        print("Lifo")

    else:
        print("Random")





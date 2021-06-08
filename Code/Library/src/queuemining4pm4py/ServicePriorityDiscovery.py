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

    if Negative == 0 and Positive > 0:
        print("Fifo")

    elif Negative > 0 and Positive == 0:
        print("Lifo")

    else:
        print("Random")




# print(perf_spectrum)
# print(perf_spectrum['points'][0][1])
# pm4py.view_performance_spectrum(log,activities, format="svg")

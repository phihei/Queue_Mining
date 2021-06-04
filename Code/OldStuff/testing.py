import random

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import pm4py.objects.dfg.utils.dfg_utils as pm4pydfg
import pm4py.stats

from Code.Library.src.queuemining4pm4py.statistics_logs import *
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
from pathlib import Path
from pm4py import view_performance_spectrum

from Code.Library.src.queuemining4pm4py import xes_to_nx_utilities


class Parameters(Enum):
    ATTRIBUTE_KEY = constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY


variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('../../logs/HospitalBillingEventLog_lifecycle.xes', variant=variant, parameters=parameters)
activities = []
seen = set()

#['NEW', 'CHANGE DIAGN', 'FIN', 'RELEASE', 'CODE OK', 'BILLED', 'DELETE', 'MANUAL', 'REOPEN', 'STORNO', 'REJECT', 'SET STATUS', 'CODE NOK', 'CHANGE END', 'JOIN-PAT', 'CODE ERROR', 'ZDBC_BEHAN', 'EMPTY']
#view_performance_spectrum(log, ['CHANGE DIAGN', 'RELEASE', 'CODE OK'], format="svg")
""""
Test xes_to_nx_utilities
"""
# G = xes_to_nx_utilities.transform_xes_log_to_nxDiGraph(log, variant='inductive')
# #
# nx.draw(G, with_labels=True)
# plt.show()
""""
Test statistics_logs
"""
#case_duration_statistics(log,1, name='test')
#test
#case_duration_statistics_batch(False, '/home/heisenB/PycharmProjects/Queue_Mining/logs/', 'test_test')
#activity_duration_statistics(log, '/home/heisenB/PycharmProjects/Queue_Mining/logs/')

""""
Add lifecycle transitions if not contained and add random service times following a normal distribution
"""
# log = interval_lifecycle.to_interval(log)
#
# for trace in log:
#     for event in trace:
#         event['time:timestamp'] = event['start_timestamp'] + timedelta(seconds=random.uniform(3,1500))
# xes_expoter.apply(log, '../../../../logs/running-example.xes')
""""
Quick overview on log
"""
attributes = pm4py.stats.get_attributes(log)
# attribute_values = {}
# trace_values = {}
#     attribute_values[attr] = pm4py.stats.get_attribute_values(log, attr)
# case_arival_avg = pm4py.stats.get_case_arrival_average(log)

# case_start_time = [(trace[0]['concept:name'], trace[0]['start_timestamp']) for trace in log if trace and 'start_timestamp' in trace[0]]
# case_start_time = sorted(case_start_time)
# case_end_time = [(trace[-1]['time:timestamp'] for trace in log if trace and 'time:timestamp' in trace[-1]]
#
# case_diff_start_time = []
# case_diff_waiting_time = []
# for i in range(len(case_start_time)-1):
#     case_diff_start_time.append((case_start_time[1][i+1]-case_start_time[1][i]).total_seconds())
#     case_diff_waiting_time.append(())

#
# print(attribute_values)
print(attributes)
# print(trace_values)
# print(case_arival_avg)
# print(case_start_time)
# print(case_diff_start_time)


# activities = []
# seen = set()
# activities_times = {}
# for trace in log:
#     for event in trace:
#         if event['concept:name'] not in seen:
#             seen.add(event['concept:name'])
#             activities.append(event['concept:name'])
#             activities_times[event['concept:name']] = []
#         if isinstance(activities_times[event['concept:name']], list):
#             activities_times[event['concept:name']].append((event['start_timestamp'], event['time:timestamp'], (event['time:timestamp']-event['start_timestamp']).total_seconds()))
#         else:
#             activities_times[event['concept:name']] = []
#             activities_times[event['concept:name']].append((event['start_timestamp'], event['time:timestamp'], (event['time:timestamp']-event['start_timestamp']).total_seconds()))
#
# #activities_times = dict.fromkeys(activities, [])
#
# for activity in activities_times:
#     deltas = [x for triple in activities_times[activity] for x in triple[-1:]]
#     mean = np.mean(deltas)
#     min = np.min(deltas)
#     max = np.max(deltas)
#     std = np.std(deltas)
#
#     fig, ax = plt.subplots()
#     mu = mean
#     sigma = std
#
#     # the histogram of the data
#     n, bins, patches = ax.hist(deltas, bins=30, density=True)
#
#     # add a 'best fit' line
#     y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
#          np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
#     ax.plot(bins, y, '--')
#     ax.set_xticks(range(int(min), int(max), 5))  # need to be adjusted to be readable
#     ax.set_xlabel('Duration in min')
#     ax.set_ylabel('Probability density')
#     ax.set_title(r'Time Distribution for activity: ' + activity)
#
#     # Tweak spacing to prevent clipping of ylabel
#     fig.tight_layout()
#     plt.show()
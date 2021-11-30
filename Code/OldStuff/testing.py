import operator
import pprint
import random

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import pm4py.objects.dfg.utils.dfg_utils as pm4pydfg
import pm4py.stats
import scipy
import ast
import timeit

from Code.Library.src.queuemining4pm4py.statistics_logs import *
from Code.Library.src.queuemining4pm4py.queueDiscovery import *
from Code.Library.src.queuemining4pm4py.delayPrediction import *
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
from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery
from Code.Library.src.queuemining4pm4py import xes_to_nx_utilities
from fitter import Fitter
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.filtering.log.variants import variants_filter


class Parameters(Enum):
    ATTRIBUTE_KEY = constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY
"""
convert .csv to XES
"""
# log_csv = pd.read_csv('../../logs/queues_restricted.csv', sep=',')
# log_csv = log_csv.rename(columns={'case': 'case:concept:name', 'event': 'concept:name', 'startTime': 'start_timestamp', 'completeTime': 'time:timestamp'})
# log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
# log_csv = log_csv.sort_values('start_timestamp')
# event_log = log_converter.apply(log_csv)
# xes_expoter.apply(event_log, '../../logs/queues_restricted.xes')

#
variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('../../logs/BPI_Challenge_2019.xes', variant=variant, parameters=parameters)


#['NEW', 'CHANGE DIAGN', 'FIN', 'RELEASE', 'CODE OK', 'BILLED', 'DELETE', 'MANUAL', 'REOPEN', 'STORNO', 'REJECT', 'SET STATUS', 'CODE NOK', 'CHANGE END', 'JOIN-PAT', 'CODE ERROR', 'ZDBC_BEHAN', 'EMPTY']
#view_performance_spectrum(log, ['CHANGE DIAGN', 'RELEASE', 'CODE OK'], format="svg")

""""
Add lifecycle transitions if not contained and add random service times following a normal distribution
"""
# log = interval_lifecycle.to_interval(log)
#
# for trace in log:
#     for event in trace:
#         event['time:timestamp'] = event['start_timestamp'] + timedelta(seconds=random.triangular(3, 1500))
# xes_expoter.apply(log, '../../../../logs/running-example.xes')
""""
Preprocessing BPI2019
"""

sortedlog = sorting.sort_timestamp(log)

for trace in sortedlog:
    for event in trace:
        if event.get('org:resource', "default").startswith('batch'):
            event['org:resource'] = 'batch'

xes_export_factory.export_log(sortedlog, "Batch_user_ModelB_Log.xes")

# sortedlog = sorting.sort_timestamp(log)
# activities = attributes_filter.get_attribute_values(sortedlog, "concept:name")
# print(activities)
# tmp = activities.keys()
# filterlist = []
#
# def comp(s1):
#     if s1[:4] == "SRM:":
#         return True
#     else:
#         return False
#
# for key in tmp:
#     if comp(key):
#         filterlist.append(key)
#
# print(filterlist)
#tracefilter_log = attributes_filter.apply(sortedlog, filterlist, parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: "concept:name", "positive": True})
#filteredLog = timestamp_filter.filter_traces_contained(sortedlog, "2017-12-31 00:00:00", "2019-01-18 00:00:00")
#xes_export_factory.export_log(tracefilter_log, "Only_SRM_2018_Log.xes")
""""
Filter variants
"""
#auto_filtered_log = variants_filter.apply_auto_filter(log, parameters={variants_filter.Parameters.DECREASING_FACTOR: 0.9})
# filtered_log = variants_filter.filter_log_variants_percentage(log, percentage=0.4)
# xes_expoter.apply(filtered_log, '../../logs/Hospital_lifecycle_filter_40.xes')

""""
Quick overview on log
"""
attributes = pm4py.stats.get_attributes(log)
attributes2 = pm4py.get_attributes(log)
print("attributes", attributes)
print("attributes2", attributes2)

attribute_values_res = pm4py.stats.get_attribute_values(log, 'org:resource')
attribute_values_user = pm4py.stats.get_attribute_values(log, 'User')
print("attribute_values_res", attribute_values_res)
print("attribute_values_user", attribute_values_user)
print("equal" if attribute_values_res == attribute_values_user else "unequal")

attribute_values_act = pm4py.stats.get_attribute_values(log, 'concept:name')
print("attribute_values_act", attribute_values_act)

trace_attributes = pm4py.stats.get_trace_attributes(log)
print("trace_attributes", trace_attributes)

# case_start_time = [(trace[0]['concept:name'], trace[0]['start_timestamp']) for trace in log if trace and 'start_timestamp' in trace[0]]
# case_start_time = sorted(case_start_time)
# case_end_time = [(trace[-1]['time:timestamp'] for trace in log if trace and 'time:timestamp' in trace[-1]]


#dfg = dfg_discovery.apply(log) #contains activity pairs that directly-follow, use them to calculate waiting times
#df_activities = list(dfg.keys()) # list of tuples
# print(df_activities)

#scheduled_times = {} #earliest possible execution time

#clms = ['case:concept:name'] + (pm4py.stats.get_attributes(log))
#clms = ['case:concept:name', 'concept:name', 'start_timestamp', 'time:timestamp', 'scheduled_timestamp', 'org:resource']

#schedules_times_df = pd.DataFrame(columns=clms)

# for trace in log:
#     for i in range(len(trace)-1):
        # if trace[i+1]['concept:name'] not in seen:
        #     seen.add(trace[i+1]['concept:name'])
        #     scheduled_times[trace[i+1]['concept:name']] = []
      #  if (trace[i]['concept:name'], trace[i+1]['concept:name']) in df_activities:
            #scheduled_times[trace[i+1]['concept:name']].append(trace[i]['time:timestamp'])
            # finish-start dependency, earliest start is latest finish of (all) preceding activities (if AND join)
        #     schedules_times_df.loc[len(schedules_times_df)] = [trace.attributes['concept:name'], trace[i+1]['concept:name'],
        #                                trace[i+1]['start_timestamp'], trace[i+1]['time:timestamp'], trace[i]['time:timestamp'], trace[i+1]['org:resource']]
        # if trace[i]['concept:name'] == trace[0]['concept:name']:
        #     schedules_times_df.loc[len(schedules_times_df)] = [trace.attributes['concept:name'], trace[i]['concept:name'],
        #                                trace[i]['start_timestamp'], trace[i]['time:timestamp'], trace[i]['start_timestamp'], trace[i]['org:resource']]
#sorted(schedules_times_list, key=operator.itemgetter(0))
#eventually directly build dataframe from log without

# schedules_times_df = schedules_times_df.sort_values(['scheduled_timestamp', 'case:concept:name'])
# schedules_times_df.reset_index(drop=True, inplace=True)
#schedules_times_df.to_csv('../../logs/running_example_schedule_asc.csv')

# seen = set()
# activities_times_intervals = {}
# for trace in log:
#     for event in trace:
#         if event['concept:name'] not in seen:
#             seen.add(event['concept:name'])
#             activities_times_intervals[event['concept:name']] = []
#         if isinstance(activities_times_intervals[event['concept:name']], list):
#             activities_times_intervals[event['concept:name']].append((trace.attributes['concept:name'], event['start_timestamp'], event['time:timestamp']))
#
#
# activities = list(set(schedules_times_df['concept:name']))
#
#
# queues = dict.fromkeys(activities)
# for a in activities:
#     queues[a] = []
# latest_TimePoint = schedules_times_df.at[len(schedules_times_df)-1, 'time:timestamp']
# for row in range(len(schedules_times_df)):
#     curr_Time = schedules_times_df.at[row, 'scheduled_timestamp']
#     print(curr_Time)
#     curr_TimeWindow = [curr_Time, latest_TimePoint]
#
#     if (schedules_times_df.at[row, 'start_timestamp'] - curr_Time).total_seconds() > 0:
#         queues[schedules_times_df.at[row, 'concept:name']].append((schedules_times_df.at[row, 'case:concept:name'],
#                                                                    schedules_times_df.at[row, 'start_timestamp']))
#
#     for que in queues.values():
#         if len(que) > 0:
#             for position in que:
#                 if position[1] <= curr_Time:
#                     que.remove(position)
#     print("Current queue: ", queues)
#     print("Number of cases currently: ", sum(map(len, queues.values())))
#print('empty?', queues)


#queues, stats = queue(add_scheduledTimestamps_single(log), lifecycle=False, only_cases=True, plt_bar=True)


#queues.to_csv('../../logs/hospital_queues.csv')
#stats.to_csv('../../logs/hospitalstats.csv')
#
# delayPredictor = DelayPredictor(log, "SRM: Created", "Vendor creates invoice': 219919", "Create Purchase Order Item")
# waitPrediction1 = delayPredictor.getPTSPrediction(60, datetime.datetime(2021, 6, 18, 10))
# print(f"Wait Prediction, Method: PTS {waitPrediction1}")
# waitPrediction2 = delayPredictor.getQLPPrediction(60, 2, datetime.timedelta(seconds=300))
# print(f"Wait Prediction, Method: QLP {waitPrediction2}")
# waitPrediction3 = delayPredictor.getQLMPPrediction(60, 2, datetime.timedelta(seconds=300), 0.0001)
# print(f"Wait Prediction, Method: QLMP {waitPrediction3}")
# waitPrediction4 = delayPredictor.getLESPrediction(60, datetime.datetime(2021, 6, 18, 10))
# print(f"Wait Prediction, Method: LES {waitPrediction4}")
# waitPrediction5 = delayPredictor.getHOLPrediction(60)
# print(f"Wait Prediction, Method: HOL {waitPrediction5}")

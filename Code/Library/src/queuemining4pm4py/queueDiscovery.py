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
from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery
from Code.Library.src.queuemining4pm4py import xes_to_nx_utilities
from fitter import Fitter
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter


def add_finishStart_scheduleTimestamps(log, columns: list =['case:concept:name', 'concept:name', 'start_timestamp',
                                                      'time:timestamp', 'scheduled_timestamp', 'org:resource']) -> pd.DataFrame:
    """
    TODO
    :param log:
    :param columns:
    :return:
    """
    dfg = dfg_discovery.apply(log)  # contains activity pairs that directly-follow, use them to calculate waiting times
    df_activities = list(dfg.keys())  # list of tuples

    # clms = ['case:concept:name'] + (pm4py.stats.get_attributes(log))
    schedules_times_df = pd.DataFrame(columns=columns)

    for trace in log:
        for i in range(len(trace) - 1):
            if (trace[i]['concept:name'], trace[i + 1]['concept:name']) in df_activities:
                # finish-start dependency, earliest start is latest finish of (all) preceding activities (if AND join)
                schedules_times_df.loc[len(schedules_times_df)] = [trace.attributes['concept:name'],
                                                                   trace[i + 1]['concept:name'],
                                                                   trace[i + 1]['start_timestamp'],
                                                                   trace[i + 1]['time:timestamp'],
                                                                   trace[i]['time:timestamp'],
                                                                   trace[i + 1]['org:resource']]
            if trace[i]['concept:name'] == trace[0]['concept:name']:
                schedules_times_df.loc[len(schedules_times_df)] = [trace.attributes['concept:name'],
                                                                   trace[i]['concept:name'],
                                                                   trace[i]['start_timestamp'],
                                                                   trace[i]['time:timestamp'],
                                                                   trace[i]['start_timestamp'],
                                                                   trace[i]['org:resource']]

    schedules_times_df = schedules_times_df.sort_values(['start_timestamp', 'case:concept:name']) # natural event sequence
    schedules_times_df.reset_index(drop=True, inplace=True)

    return schedules_times_df

def getPrecedingActivites(log, activities):
    """

    :return:
    """
    df_activities = list(dfg_discovery.apply(log).keys())
    #get all preceding activities = dependencies
    preceding_activities = dict.fromkeys(activities)
    print(preceding_activities)
    for acti in activities:
        preceding_activities[acti] = []
        for tuple in df_activities:
            if tuple[1] == acti:
                if tuple[0] not in preceding_activities[tuple[1]]:
                    preceding_activities[tuple[1]].append(tuple[0])

    return preceding_activities

def queue(df_log, ):
    """

    :param df_log:
    :return:
    """

def possibleTimeSavings():
    """

    :return:
    """
    #last time:timestamp - (last scheduled timestamp +  serviceTime last activity) || starttime- scheduled time
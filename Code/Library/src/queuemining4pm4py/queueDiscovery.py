import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pm4py.objects.dfg.utils.dfg_utils as pm4pydfg
import pm4py.stats
import ast

from Code.Library.src.queuemining4pm4py.statistics_logs import *
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY
from datetime import datetime, timedelta
from pm4py.objects.log.util import dataframe_utils


def add_scheduledTimestamps(log, columns: list= None) -> pd.DataFrame:
    """
    This function takes an PM4Py event log and a optional list of column headers as input and transforms the event log
    into a dataframe while calculating the actual  scheduled time for each event. In this case we assume a finish-start
    dependency between all directly following activities. Additionally, we take the late finish of the preceding activity
    as earliest start. Currently this function implies that the input event log has the following attributes:
    ['case:concept:name', 'concept:name', 'start_timestamp', 'time:timestamp', 'scheduled_timestamp', 'org:resource']
    :param log: PM4Py event log
    :param columns: list of event log attributes, including the case attribute, that form the column headers.
    :return: pamdas DataFrame, sorted by new 'scheduled_timestamp'
    """
    if columns is None:
        columns = ['case:concept:name', 'concept:name', 'start_timestamp', 'time:timestamp', 'scheduled_timestamp',
                   'org:resource']
    resource = True
    if 'org:resource' not in set(pm4py.get_attributes(log)):
        resource = False

    dfg = dfg_discovery.apply(log)  # contains activity pairs that directly-follow, use them to calculate waiting times
    df_activities = list(dfg.keys())  # list of tuples

    schedules_times = []

    print('Computing scheduled timestamps and creating Dataframe. This may take a while...')
    if resource:
        for trace in log:
            for i in range(len(trace) - 1):
                if (trace[i]['concept:name'], trace[i + 1]['concept:name']) in df_activities:
                    # finish-start dependency, earliest start is latest finish of (all) preceding activities (if AND join)
                    schedules_times.append((trace.attributes['concept:name'],
                                               trace[i + 1]['concept:name'],
                                               trace[i + 1]['start_timestamp'],
                                               trace[i + 1]['time:timestamp'],
                                               trace[i]['time:timestamp'],
                                               trace[i + 1]['org:resource']))

                if trace[i]['concept:name'] == trace[0]['concept:name']:
                    schedules_times.append((trace.attributes['concept:name'],
                                               trace[i]['concept:name'],
                                               trace[i]['start_timestamp'],
                                               trace[i]['time:timestamp'],
                                               trace[i]['start_timestamp'],
                                               trace[i]['org:resource']))
    else:
        columns = ['case:concept:name', 'concept:name', 'start_timestamp', 'time:timestamp', 'scheduled_timestamp']
        for trace in log:
            for i in range(len(trace) - 1):
                if (trace[i]['concept:name'], trace[i + 1]['concept:name']) in df_activities:
                    # finish-start dependency, earliest start is latest finish of (all) preceding activities (if AND join)
                    schedules_times.append((trace.attributes['concept:name'],
                                               trace[i + 1]['concept:name'],
                                               trace[i + 1]['start_timestamp'],
                                               trace[i + 1]['time:timestamp'],
                                               trace[i]['time:timestamp']))

                if trace[i]['concept:name'] == trace[0]['concept:name']:
                    schedules_times.append((trace.attributes['concept:name'],
                                               trace[i]['concept:name'],
                                               trace[i]['start_timestamp'],
                                               trace[i]['time:timestamp'],
                                               trace[i]['start_timestamp']))

    df = pd.DataFrame(schedules_times, columns=columns)
    df = df.sort_values(['scheduled_timestamp', 'case:concept:name']) # natural event sequence
    df.reset_index(drop=True, inplace=True)
    return df


def getPrecedingActivites(log, activities=None):
    """
    This function just returns a Dictionary where each activity is associated with it's preceding activities. This can
    be used in future computations where the whole set of preceding activties is used to infer an underlying schedule,
    priority or any other kind of scheduling related characteristic.
    :return: Dict with activities as keys and set of preceding activites as values
    """
    df_activities = list(dfg_discovery.apply(log).keys())
    if activities is None:
        activities = set([item for t in df_activities for item in t])
    #get all preceding activities = dependencies
    preceding_activities = dict.fromkeys(activities)

    for acti in activities:
        preceding_activities[acti] = []
        for tp in df_activities:
            if tp[1] == acti:
                if tp[0] not in preceding_activities[tp[1]]:
                    preceding_activities[tp[1]].append(tp[0])

    return preceding_activities


def queue(df_log, only_cases:bool=False, len_queues:bool=False, plt_bar:bool=False, print_n_cases:bool=False):
    """
    This function uses a preprocessed pandas Dataframe (output of add_scheduledTimestamps) containing an
    event log with start and complete timestamps for each event as well as a timestamp defining the scheduled time for
    each event. The return is two dataframes, the first one containing queued cases at the given moment in time and the
    second one providing the total number of cases queued at the respective moment in time. Using the plt_bar parameter
    the second dataframe can be plotted as bar chart, giving an overview of the queued cases over time. The parameters
    only_cases and len_queues can be used to reduce the size of the returned dataframes by aggregating first only by
    case_id (instead of case_id and start_timestamp) and second by total number of cases per queue, using the length of
    the list.
    :param df_log: event log as Dataframe preprocessed with scheduled_timestamps
    :param len_queues: Boolean, if True the queues_stats Dataframe only contains the amount of waiting cases at this
    moment in time, not the list with the explicit cases
    :param plt_bar: Boolean, if True a bar chart is plotted
    :param print_n_cases: Boolean, if True prints the current amount of waiting cases
    :param only_cases: Boolean, if True
    :return queues_stats, stats_df: two pandas Dataframes
    """
    #if dataframe has no scheduled timestamp -> error
    #
    activities = list(set(df_log['concept:name']))
    statistic_values = {'time Points': [], 'number of Cases': []}
    queues = dict.fromkeys(activities)
    for a in activities:
        queues[a] = []
    queues_stats = pd.DataFrame([queues.copy()])
    #latest_TimePoint = df_log.at[len(df_log) - 1, 'time:timestamp']
    for row in range(len(df_log)):
        curr_Time = df_log.at[row, 'scheduled_timestamp']

        if (df_log.at[row, 'start_timestamp'] - curr_Time).total_seconds() > 0:
            activity = df_log.at[row, 'concept:name']
            case_id = df_log.at[row, 'case:concept:name']
            case_start = df_log.at[row, 'start_timestamp']
            queues[activity].append((case_id, case_start))

        for que in queues.values():
            if len(que) > 0:
                for position in que:
                    if position[1] <= curr_Time:
                        que.remove(position)
        queues_deepcopy = {}
        for key in queues:
            queues_deepcopy[key] = queues[key].copy()

        tmp_df = pd.DataFrame([queues_deepcopy], index=[curr_Time])
        queues_stats = queues_stats.append(tmp_df)
        n_cases = sum(map(len, queues.values()))
        #for loop calculation n_nases for each queue, then appending it to queues_stats
        if print_n_cases:
            print("Number of cases currently in all queues: ", n_cases)
        statistic_values['time Points'].append(curr_Time)
        statistic_values['number of Cases'].append(n_cases)
    max_cases = max(statistic_values['number of Cases'])
    mean_cases = np.mean(statistic_values['number of Cases'])
    std_cases = np.std(statistic_values['number of Cases'])
    print('Maximal Number of Queued Cases: ', max_cases)
    print('Mean Number of queued cases: ', mean_cases)
    print('Std Number if queued cases: ', std_cases)
    stats_df = pd.DataFrame(statistic_values)
    if plt_bar:
        stats_df.plot.bar(x='time Points', xticks=[], xlabel='Timestamps', y='number of Cases')
        plt.show()
    if only_cases:
        queues_stats = queues_stats.applymap(lambda x: [i[0] for i in x])
    if len_queues:
        queues_stats = queues_stats.applymap(lambda x: len(x))

    return queues_stats, stats_df

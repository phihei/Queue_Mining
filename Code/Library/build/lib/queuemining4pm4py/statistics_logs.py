""""
from pm4py.stats get_case_arrival_average(log: Union[EventLog, pd.DataFrame])
/home/heisenB/miniconda3/envs/Queue_Mining/lib/python3.7/site-packages/pm4py/statistics/attributes/log/get.py
/home/heisenB/miniconda3/envs/Queue_Mining/lib/python3.7/site-packages/pm4py/statistics/passed_time/log
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics


def case_duration_statistics_batch( hist: bool, directory: str, vt: str):
    """
    directory format "/home/myproject/"
    vt =  Provide a suitable name for the output file
    hist = 'Enter 0, if you want general duration statistics about all event logs , Enter 1 if you want a time'
                     'distribution for each event log'
    """

    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".xes"):
            files.append(filename)
        else:
            continue
    files.sort()

    all_means_log = {}
    all_mins_log = {}
    all_maxs_log = {}
    all_stds_log = {}
    all_durations = {}
    for file in files:
        all_case_durations_in_min = []
        log = xes_importer.apply(
             directory + file)
        all_case_durations = case_statistics.get_all_casedurations(log, parameters={
            case_statistics.Parameters.TIMESTAMP_KEY: 'time:timestamp'})
        #add calculation of total duration from start to end -> differs a lot depending on markov chain

        for duration in all_case_durations:
            all_case_durations_in_min.append(duration/60)

        mean = np.mean(all_case_durations_in_min)
        min = np.min(all_case_durations_in_min)
        max = np.max(all_case_durations_in_min)
        std = np.std(all_case_durations_in_min)
        all_means_log[file] = mean
        all_mins_log[file] = min
        all_maxs_log[file] = max
        all_stds_log[file] = std
        all_durations[file] = all_case_durations_in_min
    # all_means_log = dict(sorted(all_means_log.items()))
    # all_mins_log = dict(sorted(all_mins_log.items()))
    # all_maxs_log = dict(sorted(all_maxs_log.items()))
    if not os.path.exists(directory + 'statistics/'):
        os.makedirs(directory + 'statistics/')

    if hist == 0:
        fig = plt.figure(figsize=(10,10))
        plt.bar(range(len(all_means_log)), list(all_means_log.values()), align='center')
        plt.xticks(range(len(all_means_log)), list(all_means_log.keys()), rotation=90)
        plt.title('Mean Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_means_log.values())):
            plt.text(i - 0.25, np.max(list(all_means_log.values()))*0.1, str(round(v, 2)), color='white', rotation='vertical')

        #plt.show()
        plt.savefig(directory + 'statistics/' + vt + 'mean_service_time.png', dpi= fig.dpi, bbox_inches='tight')

        fig = plt.figure(figsize=(10,10))
        plt.bar(range(len(all_mins_log)), list(all_mins_log.values()), align='center')
        plt.xticks(range(len(all_mins_log)), list(all_mins_log.keys()), rotation=90)
        plt.title('Min Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_mins_log.values())):
            plt.text(i - 0.25 , np.max(list(all_mins_log.values()))*0.1, str(round(v, 2)), color='white', rotation='vertical')

        #plt.show()
        plt.savefig(directory + 'statistics/' + vt + 'min_service_time.png', dpi= fig.dpi, bbox_inches='tight')

        fig = plt.figure(figsize=(10,10))
        plt.bar(range(len(all_maxs_log)), list(all_maxs_log.values()), align='center')
        plt.xticks(range(len(all_maxs_log)), list(all_maxs_log.keys()), rotation=90)
        plt.title('Max Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_maxs_log.values())):
            plt.text(i - 0.25, np.max(list(all_maxs_log.values()))*0.1, str(round(v, 2)), color='white', rotation='vertical')

        #plt.show()
        plt.savefig(directory + 'statistics/' + vt + 'max_service_time.png', dpi= fig.dpi, bbox_inches='tight')
    if hist == 1:
        for file in files:
            fig, ax = plt.subplots()
            mu = all_means_log[file]
            sigma = all_stds_log[file]

            # the histogram of the data
            n, bins, patches = ax.hist(all_durations[file], bins=30, density=True)

            # add a 'best fit' line
            y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
                 np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
            ax.plot(bins, y, '--')
            ax.set_xticks(range(int(all_mins_log[file]), int(all_maxs_log[file]), 5))
            ax.set_xlabel('Duration in min')
            ax.set_ylabel('Probability density')
            ax.set_title(r'Time Distribution of ' + file)

            # Tweak spacing to prevent clipping of ylabel
            fig.tight_layout()
            plt.show()
            fig.savefig(directory + 'statistics/timeDist_' + vt + file + '.png')


def case_duration_statistics(log, hist: bool, directory=None, vt=None):
    all_case_durations_in_min = []
    all_case_durations = case_statistics.get_all_casedurations(log, parameters={
        case_statistics.Parameters.TIMESTAMP_KEY: 'time:timestamp'})
    for duration in all_case_durations:
        all_case_durations_in_min.append(duration / 60)

    mean = np.mean(all_case_durations_in_min)
    min = np.min(all_case_durations_in_min)
    max = np.max(all_case_durations_in_min)
    std = np.std(all_case_durations_in_min)

    values = {'mean': mean, 'min': min, 'max': max, 'std': std}
    df = pd.DataFrame(values, index=[0])
    print(df)

    if hist == 1:
        #plot all case duration distribution

        fig, ax = plt.subplots()
        mu = mean
        sigma = std

        # the histogram of the data
        n, bins, patches = ax.hist(all_case_durations_in_min, bins=30, density=True)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
        ax.plot(bins, y, '--')
        ax.set_xticks(range(int(min), int(max), 5)) #need to be adjusted to be readable
        ax.set_xlabel('Duration in min')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Time Distribution ' + vt)

        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()
        if directory is not None:
            fig.savefig(directory + '/statistics/' + vt + '.png')
        else:
            fig.savefig(vt + '.png')


def activity_duration_statistics(log, variant=None):
    """
    time distribution per activity
    min, max, mean (service or waiting times) per activity
    choose between waiting time(using the time passed functions from pm4py, see at the top) and service time (from pm4py.statistics.sojourn_time.log import get as soj_time_get

soj_time = soj_time_get.apply(log, parameters={soj_time_get.Parameters.TIMESTAMP_KEY: "time:timestamp", soj_time_get.Parameters.START_TIMESTAMP_KEY: "start_timestamp"})
print(soj_time)
    activity_times: dict with unique activity names as keys and triple (start, end, service time in seconds) as value
    x axis: activity name
    y axis: min, max, mean or std duration,

    :return:
    """

    # if variant == 'service':
    #     delta =(event['time:timestamp'] - event['start_timestamp']).total_seconds())
    # elif variant == 'waiting':
    #     delta = 0 #calculating waiting time will be added later
    #

    activities = []
    seen = set()
    activities_times = {}
    for trace in log:
        for event in trace:
            if event['concept:name'] not in seen:
                seen.add(event['concept:name'])
                activities.append(event['concept:name'])
                activities_times[event['concept:name']] = []
            if isinstance(activities_times[event['concept:name']], list):
                activities_times[event['concept:name']].append((event['start_timestamp'], event['time:timestamp'], (
                            event['time:timestamp'] - event['start_timestamp']).total_seconds()))
            else:
                activities_times[event['concept:name']] = []
                activities_times[event['concept:name']].append((event['start_timestamp'], event['time:timestamp'], (
                            event['time:timestamp'] - event['start_timestamp']).total_seconds()))

    for activity in activities_times:
        deltas = [x for triple in activities_times[activity] for x in triple[-1:]]
        mean = np.mean(deltas)
        min = np.min(deltas)
        max = np.max(deltas)
        std = np.std(deltas)

        fig, ax = plt.subplots()
        mu = mean
        sigma = std

        # the histogram of the data
        n, bins, patches = ax.hist(deltas, bins=30, density=True)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
        ax.plot(bins, y, '--')
        ax.set_xticks(range(int(min), int(max), 5))  # need to be adjusted to be readable
        ax.set_xlabel('Duration in min')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Time Distribution for activity: ' + activity)

        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()


# from pm4py.stats get_case_arrival_average(log: Union[EventLog, pd.DataFrame])
# /home/heisenB/miniconda3/envs/Queue_Mining/lib/python3.7/site-packages/pm4py/statistics/attributes/log/get.py
# /home/heisenB/miniconda3/envs/Queue_Mining/lib/python3.7/site-packages/pm4py/statistics/passed_time/log
import pkgutil

import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from fitter import Fitter
import pm4py.stats
from pathlib import Path
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

def case_duration_statistics_batch(time_distribution: bool, directory: str, name: str):
    """
    This function is able to handle multiple event logs in a folder specified by the directory parameter. For each event
    log basic statistics (min, max, mean and std) on end-to-end service time are computed. If time_distribution is set to
    True, a histogram of the service time distribution is computed for each event log. All figures are then saved as
    .png in a (new) subfolder called "statistics" under the given directory.

    :param time_distribution:  Bool: if True a end-to-end service time distribution histogram with best fit line will be computed and plotted
             for each event log, if False general statistical values will be computed and plotted in one figure comparing
             all event event logs
    :param directory: String: providing the path to the folder where the event logs are located and where plots will be saved in
            the subfolder /statistics
    :param name: String: prefix in the filename for the generated figures
    :return: Nothing
        Generates figures and saves them to disk.
    """
    directory = Path(directory)

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
             directory / file)
        all_case_durations = case_statistics.get_all_casedurations(log, parameters={
            case_statistics.Parameters.TIMESTAMP_KEY: 'time:timestamp'})

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
    if not os.path.exists(directory / 'statistics/'):
        os.makedirs(directory / 'statistics/')

    if time_distribution == 0:
        fig = plt.figure(figsize=(10,10))
        plt.bar(range(len(all_means_log)), list(all_means_log.values()), align='center')
        plt.xticks(range(len(all_means_log)), list(all_means_log.keys()), rotation=90)
        plt.title('Mean Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_means_log.values())):
            plt.text(i - 0.25, np.max(list(all_means_log.values()))*0.1, str(round(v, 2)), color='white', rotation='vertical')

        #plt.show()
        plt.savefig(directory / 'statistics' / (name + 'mean_service_time.png'), dpi=fig.dpi, bbox_inches='tight')

        fig = plt.figure(figsize=(10,10))
        plt.bar(range(len(all_mins_log)), list(all_mins_log.values()), align='center')
        plt.xticks(range(len(all_mins_log)), list(all_mins_log.keys()), rotation=90)
        plt.title('Min Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_mins_log.values())):
            plt.text(i - 0.25 , np.max(list(all_mins_log.values()))*0.1, str(round(v, 2)), color='white', rotation='vertical')

        #plt.show()
        plt.savefig(directory / 'statistics' / (name + 'min_service_time.png'), dpi=fig.dpi, bbox_inches='tight')

        fig = plt.figure(figsize=(10,10))
        plt.bar(range(len(all_maxs_log)), list(all_maxs_log.values()), align='center')
        plt.xticks(range(len(all_maxs_log)), list(all_maxs_log.keys()), rotation=90)
        plt.title('Max Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_maxs_log.values())):
            plt.text(i - 0.25, np.max(list(all_maxs_log.values()))*0.1, str(round(v, 2)), color='white', rotation='vertical')

        #plt.show()
        plt.savefig(directory / 'statistics' / (name + 'max_service_time.png'), dpi=fig.dpi, bbox_inches='tight')

        fig = plt.figure(figsize=(10, 10))
        plt.bar(range(len(all_stds_log)), list(all_stds_log.values()), align='center')
        plt.xticks(range(len(all_stds_log)), list(all_stds_log.keys()), rotation=90)
        plt.title('Standard Deviation Service Time')
        plt.ylabel('Service Time in Minutes')
        for i, v in enumerate(list(all_stds_log.values())):
            plt.text(i - 0.25, np.max(list(all_stds_log.values())) * 0.1, str(round(v, 2)), color='white',
                     rotation='vertical')

        # plt.show()
        plt.savefig(directory / 'statistics' / (name + 'std_service_time.png'), dpi=fig.dpi, bbox_inches='tight')


    if time_distribution == 1:
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
            fig.savefig(directory / 'statistics' / ('timeDist_' + name + file + '.png'))


def case_duration_statistics(log, time_distribution: bool, directory=None, name=None):
    """
    This function is able to handle multiple event logs in a folder specified by the directory parameter. For each event
    log basic statistics on end-to-end service time are computed. If time_distribution is set to True, a histogram of
    the service time distribution is computed for each event log.

    :param log: PM4PY oevent log object
    :param time_distribution: Bool: if True a end-to-end service time distribution histogram with best fit line will be computed and plotted
             for each event log, if False general statistical values will be computed and plotted in one figure comparing
             all event event logs
    :param directory: String: providing the path to the folder where the event logs are located and where plots will be saved in
            the subfolder /statistics
    :param name:  String: prefix in the filename for the generated figures
    :return: Nothing
        Generates and stores figures with statistics
    """
    if log is None or time_distribution is None:
        print('We need an event log and a boolean value!')
        return -1
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

    if time_distribution == 1:
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
        ax.set_xticks(bins) #need to be adjusted to be readable
        ax[0].tick_params(rotation=45)
        ax.set_xlabel('Duration in min')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Time Distribution ' + name)

        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()
        if directory is not None:
            directory = Path(directory)
            fig.savefig(directory / 'statistics' / (name + '.png'))
        else:
            fig.savefig(name + '.png')


def activity_duration_statistics(log, directory: str, timestamp_attribute=None, name=None):
    """
    This function takes an event log, directory path and an optional name as input. For each activity in the event log all service times are
    gathered, this means for all instances of the activity. Then basic statistics per activity are calculated and a
    resulting histogram showing the distribution of service times for each activity is computed and shown as a figure.

    :param log: PM4PY oevent log object
    :param directory: String: providing the path to the folder where the event logs are located and where plots will be saved in
            the subfolder /statistics
    :param timestamp_attribute: String that defines the attribute name of the start timestamp
    :param name: String: prefix in the filename for the generated figures
    :return: Dict with activities as keys and their service times as list
        Generates and stores figures with statistics
    """
    if log is None:
        print('We need an event log.')
        return -1
    if name is None:
        name = ""
    if 'start_timestamp' not in pm4py.stats.get_attributes(log) and timestamp_attribute is None:
        print('Event log has no attribute start_timestamp, can not compute service time. Provide timestamp_attribute '
              'parameter value as string or convert event log to lifecycle format.')
    elif timestamp_attribute is not None:
        start_service = timestamp_attribute

    else:
        start_service = 'start_timestamp'
        end_service = 'time:timestamp'
    # if variant == 'service':
    #     delta =(event['time:timestamp'] - event['start_timestamp']).total_seconds())
    # elif variant == 'waiting':
    #     delta = 0 #calculating waiting time will be added later
    #
    directory = Path(directory)
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
                            event['time:timestamp'] - event['start_timestamp']).total_seconds()/60))

    for activity in activities_times:
        deltas = [x for triple in activities_times[activity] for x in triple[-1:]]
        mean = np.mean(deltas)
        min = np.min(deltas)
        max = np.max(deltas)
        std = np.std(deltas)

        fig, ax = plt.subplots(2,1)
        mu = mean
        sigma = std

        # the histogram of the data
        n, bins, patches = ax[0].hist(deltas, bins=30, density=True)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
        ax[0].plot(bins, y, '--')
        ax[0].set_xticks(bins)  # need to be adjusted to be readable
        ax[0].tick_params(rotation=45)
        ax[0].set_xlabel('Duration in min')
        ax[0].set_ylabel('Probability density')
        ax[0].set_title(r'Service Time Distribution for activity: ' + activity)
        ax[1].axis('tight')
        ax[1].axis('off')
        ax[1].table(cellText=[[mean], [min], [max], [std]], colLabels=['Values'], rowLabels=['mean', 'min', 'max', 'std'],
                 loc='center')
        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()
        fig.savefig(directory / 'statistics' / ('timeDist_' + activity + name + '.png'))
    return activities_times

def activity_waiting_time(log, statistics=False, timestamp_attribute: str =None):
    """
       This function takes an event log and a boolean parameter as input. For each activity in the event log all waiting
       times are gathered, this means for all instances of the respective activity. The waiting time is calculated as
       difference between the end timestamp of preceeding activites and the start timestamp of the corresponding activity.
       Then basic statistics per activity are calculated and a resulting histogram showing the distribution of watiting
       times for each activity is computed and shown as a figure, if statistics parameter set to True.

       :param log: PM4PY oevent log object
       :param statistics: Bool, if True plots the waiting time distribution per activity queue
       :return: Dict with activities as keys and corresponding waiting times as list
           Generates and stores figures with statistics
       """
    if log is None:
        print('We need an event log.')
        return -1
    if 'start_timestamp' not in pm4py.stats.get_attributes(log) and timestamp_attribute is None:
        start_waiting, end_waiting = 'time:timestamp'
    elif timestamp_attribute is not None:
        start_waiting = 'time:timestamp'
        end_waiting = timestamp_attribute
    else:
        start_waiting = 'time:timestamp'
        end_waiting = 'start_timestamp'

    dfg = dfg_discovery.apply(log)  # contains activity pairs that directly-follow, use them to calculate waiting times
    df_activities = dfg.keys()
    waiting_times = {}
    seen = set()
    for trace in log:
        for i in range(len(trace) - 2):
            if trace[i + 1]['concept:name'] not in seen:
                seen.add(trace[i + 1]['concept:name'])
                waiting_times[trace[i + 1]['concept:name']] = []
            if (trace[i]['concept:name'], trace[i + 1]['concept:name']) in df_activities and (
                    (trace[i + 1][end_waiting] - trace[i][start_waiting]).total_seconds() > 0):
                waiting_times[trace[i + 1]['concept:name']].append(
                    ((trace[i + 1][end_waiting] - trace[i][start_waiting]).total_seconds())/60)

    if not statistics:
        return waiting_times
    else:
        for activity in waiting_times:
            deltas = waiting_times[activity]
            mean = np.mean(deltas)
            min = np.min(deltas)
            max = np.max(deltas)
            std = np.std(deltas)

            fig, ax = plt.subplots(2, 1)
            mu = mean
            sigma = std

            # the histogram of the data
            n, bins, patches = ax[0].hist(deltas, bins=30, density=True)

            # add a 'best fit' line
            y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
            ax[0].plot(bins, y, '--')
            ax[0].set_xticks(bins)  # need to be adjusted to be readable
            ax[0].tick_params(rotation=45)
            ax[0].set_xlabel('Waiting Time in min')
            ax[0].set_ylabel('Probability density')
            ax[0].set_title(r'Waiting Time Distribution for activity: ' + activity)
            ax[1].axis('tight')
            ax[1].axis('off')
            ax[1].table(cellText=[[mean], [min], [max], [std]], colLabels=['Values'], rowLabels=['mean', 'min', 'max', 'std'],
                        loc='center')
            # Tweak spacing to prevent clipping of ylabel
            fig.tight_layout()
            plt.show()
            #fig.savefig(directory / 'statistics' / ('timeDist_' + activity + name + '.png'))
        return waiting_times


def time_distribution_classification(data, distributions: list= None):
    """
    TODO
    aic stands for the Akaike information criterion, bic for the Bayesian information criterion, kl_div for the Kullback-Leibler divergence from scipy.special

    :param data: dict or array with time values for activities
    :param distributions: , if True plots the waiting time distribution per activity queue
    :return: Dict with activities as keys and corresponding waiting times as list
          Generates and stores figures with statistics
    """

    if isinstance(data, dict):
        #columns = ['Activity', 'Best Fit', ]
        for activity in data:
            deltas = data[activity]
            if len(deltas) <= 1:
                print('Not enough values for', activity, '. Will continue.')
                continue
            f = Fitter(deltas)
            if distributions is not None:
                f.distributions = distributions
            else:
                f.distributions = ['cauchy', 'chi2', 'expon', 'exponpow', 'gamma',
                                   'lognorm', 'norm', 'powerlaw', 'rayleigh', 'uniform']

            f.fit()
            summary = f.summary()
            best_fit = list(f.get_best().keys())[0]
            # dataframe: activity as key, distribution and it's values as columns - goal would be to return a dataframe
            # if needed
            print("activity:", activity, "| best fit distribution:", best_fit, "\n", summary)
            print("__________________________________________________________")
            #df[activity]
            #f.hist()
            #f.plot_pdf()
    elif isinstance(data, list):
        deltas = data
        if len(deltas) <= 1:
            print('Not enough values for fitting distributions.')
            return -1
        f = Fitter(deltas)
        if distributions is not None:
            f.distributions = distributions
        else:
            f.distributions = ['cauchy', 'chi2', 'expon', 'exponpow', 'gamma',
                               'lognorm', 'norm', 'powerlaw', 'rayleigh', 'uniform']

        f.fit()
        f.summary()
        # dataframe: activity as key, distribution and it's values as columns - goal would be to return a dataframe
        # if needed
        print("best fit distribution:", list(f.get_best().keys())[0], "\n", f.summary())
        f.hist()
        f.plot_pdf()
    else:
        print('Valid datatypes for data are dicts with activities as keys and corresponding timings as values or lists '
              'of timing values.')
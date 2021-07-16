from Code.Library.src.queuemining4pm4py.queueDiscovery import *
from pm4py.objects.log.importer.xes import importer as xes_importer
import os
import time
from pathlib import Path
import pandas as pd
from memory_profiler import profile
from datetime import datetime


def multi_time_profile():

    directory = Path('logs/queues_scheduling')
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".xes"):
            files.append(filename)
        else:
            continue
    files.sort()

    schedule_times = {}
    queues_times = {}

    for file in files:

        log = xes_importer.apply(str(directory / file))
        start_time_schedule = time.time()
        schedule = add_scheduledTimestamps(log)
        end_time_schedule = time.time()
        start_start_time_queues = time.time()
        queues, stats = queue(schedule, only_cases=True, len_queues=True, plt_bar=True)
        end_time_queues = time.time()

        schedule_times[file] = end_time_schedule - start_time_schedule
        queues_times[file] = end_time_queues - start_start_time_queues

    print(schedule_times)
    print(queues_times)
    schedule_times_df = pd.DataFrame(schedule_times, index=[0])
    queues_times_df = pd.DataFrame(queues_times, index=[0])
    schedule_times_df.to_csv('scheduled_times.csv')
    queues_times_df.to_csv('queues_times.csv')


def single_time_profile():
    log_name = "running-example_lifecycle.xes"
    variant = xes_importer.Variants.ITERPARSE
    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    log = xes_importer.apply('logs/queues_scheduling/' + log_name, variant=variant, parameters=parameters)

    schedule_times = {}
    queues_times = {}

    start_time_schedule = time.time()
    schedule = add_scheduledTimestamps(log)
    end_time_schedule = time.time()
    start_start_time_queues = time.time()
    queues, stats = queue(schedule, only_cases=True, len_queues=True, plt_bar=True)
    end_time_queues = time.time()

    schedule_times[log_name] = end_time_schedule - start_time_schedule
    queues_times[log_name] = end_time_queues - start_start_time_queues

    print(schedule_times)
    print(queues_times)


report = open('memory_report_simple.txt', 'w+')
@profile(stream=report)
def memory_profile():
    directory = Path('logs/queues_scheduling')
    file = 'simple_lifecycle.xes'

    log = xes_importer.apply(str(directory / file))
    schedule = add_scheduledTimestamps(log)
    _, _ = queue(schedule, only_cases=False, len_queues=False, plt_bar=False)


if __name__ == '__main__':
    #single_time_profile()
    #multi_time_profile()
    memory_profile()

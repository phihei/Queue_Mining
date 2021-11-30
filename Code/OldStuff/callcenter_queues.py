import os
import numpy as np
import pandas as pd
from pathlib import Path
import datetime as dt
directory = Path('/home/heisenB/PycharmProjects/Queue_Mining/logs/AnonymousBank')

df = pd.read_csv(directory/"all1999_datetime_negative_q_.csv")

def clm_to_datetime(df):
    for col in df.columns[:6]:
        df[col] = pd.to_datetime(df[col])

    df = df.sort_values(by='date_vru_entry').reset_index(drop=True)

    return df

def queue_analysis(df, filename:str, HOL:bool=False):

    activities = ['vru', 'queued', 'service']
    statistic_values = {'time Points': [], 'number of Cases': []}
    queues = dict.fromkeys(activities)
    for a in activities:
        queues[a] = []
    queues_stats = pd.DataFrame([queues.copy()])
    # for index, row in tmp.iterrows():
    #     curr_Time = row['date_vru_entry']  # if str(row['date_q_exit'])[-8:] != '00:00:00' else -1
    for row in range(len(df)):
        curr_Time = df.at[row, 'date_vru_entry']

        # if (df.at[row, 'date_vru_exit'] - curr_Time).total_seconds() > 0 and not HOL:
        #     activity = activities[0]
        #     call_id = df.at[row, 'call_id_']
        #     queue_exit = df.at[row, 'date_vru_exit']
        #     queues[activity].append([call_id, queue_exit])

        if (df.at[row, 'date_q_start'] - curr_Time).total_seconds() > 0 and not HOL:
            activity = activities[1]
            call_id = df.at[row, 'call_id_']
            queue_exit = df.at[row, 'date_q_exit']
            queues[activity].append([call_id, queue_exit])

        if (df.at[row, 'date_q_start'] - curr_Time).total_seconds() > 0 and HOL:
            activity = activities[1]
            call_id = df.at[row, 'call_id_']
            queue_exit = df.at[row, 'date_q_exit']
            queue_entry = df.at[row, 'date_q_start']
            queues[activity].append([call_id, queue_exit, queue_entry])

        # if (df.at[row, 'date_ser_start'] - curr_Time).total_seconds() > 0 and not HOL:
        #     activity = activities[2]
        #     call_id = df.at[row, 'call_id_']
        #     queue_exit = df.at[row, 'date_ser_exit']
        #     queues[activity].append([call_id, queue_exit])
        #
        if row == 100000 or row == 200000 or row == 300000 or row == 400000:
            print(row)

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

        statistic_values['time Points'].append(curr_Time)
        statistic_values['number of Cases'].append(n_cases)
    max_cases = max(statistic_values['number of Cases'])
    mean_cases = np.mean(statistic_values['number of Cases'])
    std_cases = np.std(statistic_values['number of Cases'])
    print('Maximal Number of Queued Cases: ', max_cases)
    print('Mean for Number of queued cases: ', mean_cases)
    print('Standard Deviation for Number of queued cases: ', std_cases)
    stats_df = pd.DataFrame(statistic_values)
    queues_stats.drop(index=df.index[0], axis=0, inplace=True)
    queues_stats.to_csv(directory / ('queues_stats_' + filename + '.csv'))
    stats_df.to_csv(directory / ('stats_df_call_' + filename + '.csv'))
    return queues_stats, stats_df


def customer_counter(df):
    st_queued = {}
    st_queued_service = {}
    st_queued_service_end = {}

    for index, row in df.iterrows():
        st_queued[row['call_id_']] = row['q_time'] if str(row['date_q_exit'])[-8:] != '00:00:00' else -1
        st_queued_service[row['call_id_']] = row['ser_time'] if str(row['date_ser_exit'])[-8:] != '00:00:00' and str(
            row['date_q_exit'])[-8:] != '00:00:00' else -1
        st_queued_service_end[row['call_id_']] = [
            (pd.to_datetime(row['date_ser_exit']) - pd.to_datetime(row['date_vru_entry'])).total_seconds(),
            sum([row['vru_time'], row['q_time'], row['ser_time']])] if str(row['date_ser_exit'])[
                                                                       -8:] != '00:00:00' else [-1, -1]

    st_queued_clean = {key: val for key, val in st_queued.items() if val > -1}
    st_queued_service_clean = {key: val for key, val in st_queued_service.items() if val > -1}

    len_queue = len(st_queued_clean)
    len_service = len(st_queued_service_clean)
    total_time_queue = sum(st_queued_clean.values())
    total_time_service = sum(st_queued_service_clean.values())
    pts_queued = total_time_queue / len_queue
    pts_queued_std = np.std(list(st_queued_clean.values()))
    pts_service = total_time_service / len_service
    pts_service_std = np.std(list(st_queued_service_clean.values()))

    print('Number of customers that entered the queue', len_queue, 'Total time customers spend in the queue', total_time_queue, 'Average time a customer spend in the queue', pts_queued, 'Standard Deviation of queued time', pts_queued_std)
    print('Number of customers that entered service', len_service, 'Total time customers spend in service', total_time_service, 'Average service time', pts_service, 'Standard Deviation of service time', pts_service_std)
    print('Customers that abandoned the queue', (len_queue-len_service))
    return [len_queue, total_time_queue, pts_queued, (len_queue-len_service), len_service, total_time_service, pts_service]

#-- PTS (Plain Transition System) Predictor
def pts_predictor(df):
    st_queued = {}
    for index, row in df.iterrows():
        st_queued[row['call_id_']] = row['q_time'] if str(row['date_q_exit'])[-8:] != '00:00:00' else -1
    st_queued_clean = {key: val for key, val in st_queued.items() if val > -1}
    len_queue = len(st_queued_clean)
    total_time_queue = sum(st_queued_clean.values())
    return [total_time_queue / len_queue]


#-- KTS (k-loads Transition System) Predictor

def kts_predictor(df, stats_df):
    df['number of Cases'] = stats_df['number of Cases']
    st_queued_norm = {}
    st_queued_high = {}
    for index, row in df.iterrows():
        st_queued_norm[row['call_id_']] = row['q_time'] if str(row['date_q_exit'])[-8:] != '00:00:00' and row['number of Cases'] <= 5  else -1
        st_queued_high[row['call_id_']] = row['q_time'] if str(row['date_q_exit'])[-8:] != '00:00:00' and row['number of Cases'] > 5 else -1
    st_queued_norm_clean = {key: val for key, val in st_queued_norm.items() if val > -1}
    st_queued_high_clean = {key: val for key, val in st_queued_high.items() if val > -1}

    return [sum(st_queued_norm_clean.values()) / len(st_queued_norm_clean), sum(st_queued_high_clean.values()) / len(st_queued_high_clean)]


#-- QLP (Queue length-based Predictors) on Queueing Model Predictors
# m: mean service time (over all cases 194.5225555655359 sec), L(t): queue-length at time t, n: number of agents, µ=1/m: service rate of agent --> qlp (L(t)) = (L(t) +1) / (n*µ)

def qlp_predictor(df, stats_df, queue_values):
    n = len(df['server'].unique()) / 2 #maybe extract number of agents working that day?
    m = queue_values[-1]
    my = 1 / m
    df['number of Cases'] = stats_df['number of Cases']
    predicted_times = dict.fromkeys(df['call_id_'])
    for index, row in df.iterrows():
        len_queue = row['number of Cases']
        predicted_times[row['call_id_']] = (len_queue + 1)* m / n

    return predicted_times

#-- QLMP (Queue length-based  Markovian Predictors) assumes finite patience
#  θ: individual abandonment rate (total abandonments 63218/ sum of q time 26224345), i: number of customers in queue

def qlmp_predictor(df, queue_values, queues_stats):
    n = len(df['server'].unique()) / 2
    m = queue_values[-1]
    my = 1/ m
    theta = queue_values[3] / queue_values[0]

    queues_stats['index'] = [x for x in range(0, len(queues_stats))]
    queues_stats.set_index('index', inplace=True)
    df['queued'] = queues_stats['queued']
    predicted_times = dict.fromkeys(df['call_id_'])
    for index, row in df.iterrows():
        queue = row['queued']
        len_queue = len(queue)
        for pos in range(0, len_queue):
            if pos == 0:
                predicted_times[queue[pos][0]] = 1 / (n*my)
            else:
                predicted_times[queue[pos][0]] = predicted_times[queue[pos - 1][0]] + 1/(n*my + pos*theta)
    return predicted_times


#-- LES (Last-customer to enter service)
# delay of the most recent service entrant (customer that was in front of queue -- calculate for each customer [on the same line?] the predicted waiting time
# case ci that last entered service is the one that satisfies condition: there is a queue event (ti, ci, pi, ai) with pi = sStart and for all (tj, cj, pj, aj), i ≤ j it holds pj ̸= sStart. Then, with (tq, cq, pq, aq), cq = ci, pq = qEntry as the event indicating queue entrance of the respective customer, the predictor is derived as WLES = ti − tq
#split data set on vru lines, use q_time of i to predict q_time of i+1 -> directly calculate measurements?

def les_predictor(df):
    # service_start != 00:00:00 -> if abandoned than take value from last customer that entered service
    #les is q_time for LAST customer that actually entered service
    #lines = df['vru+line'].unique()
    #attr = df.columns
    #ret = pd.DataFrame(df.columns)
    # or 0 if queue is empty ?
    #order df by ser_start

    q_time = [0] + list(df['q_time'])[:-1]
    for index, row in df.iterrows():
        if str(row['date_ser_start'])[-8:] == '00:00:00' and index < (len(q_time) - 2):
            q_time[index + 1] = q_time[index - 1] if index > 0 else 0

    return q_time

#-- HOL (Head-of-line) assumes FCFS (order of queue Entry timestamps imposes the same order on service Start)
#use queue_stats to determine queue position -> "queued"
# time Point .now() - q_entry for HOL


def hol_predictor(df, queue_stats):
    queue_stats['index'] = [x for x in range(0, len(queue_stats))]
    queue_stats.set_index('index', inplace=True)
    df['queued'] = queue_stats['queued']

    tmp = df[df['priority'] < 2]
    tmp = tmp.sort_values(by='date_vru_entry').reset_index(drop=True)
    predicted_times = dict.fromkeys(tmp['call_id_'])
    for index, row in tmp.iterrows():
        curr_Time = row['date_vru_entry']  # if str(row['date_q_exit'])[-8:] != '00:00:00' else -1
        HOL = row['queued']
        if len(HOL) > 0:
            HOL_id = HOL[0][0]
            HOL_timedelta = max((curr_Time - HOL[0][2]).total_seconds(), 0)
            for c in range(1, len(HOL)):
                predicted_times[HOL[c][0]] = HOL_timedelta

    return predicted_times




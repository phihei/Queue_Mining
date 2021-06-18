#!/usr/bin/env python
# coding: utf-8

# In[134]:


import pm4py
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics
import datetime
from matplotlib import colors
from tqdm import tqdm
from datetime import timedelta
from pm4py.util.business_hours import BusinessHours

def analyzeQueueArrivalRate(eventLog, eventList, interval, startTime=None, endTime=None, cycle=None, aligned=True):
    """
    Analyzes the Arrival times customers.
    :param eventLog: A PM4PY event log
    :type eventLog: pm4py.objects.log.obj.EventLog
    :param eventList: A List. The values of this List are either Strings, if
        only a single Activity in the event log signalizes Arrival, or a list of
        strings, im multiple Activities lead to customers waiting on the same service.
    :type eventList: list
    :param interval: Specifies the size of the intervals in which the Queue arrivals are seperated. Use a
        datetime.timedelta object for all short timespans, and a string consisting of a (optional) (Standart: 1) number(integer)
        and unit (either month or year) for longer timespans.
        Note: If an edge land on a day that doesn't exist (like a 29th of non leap year feburary or 31st of april, at that point
        the edge will move forward to the 1st of the next month, (and stay on the first of that month)
    :type interval: datetime.timedelta or str
    :param startTime: Only Counts events after StartTime. If not specified, this will be the time of the earliest event in the event log.
    :type startTime: datetime.datetime
    :param endTime: Only Counts events before StartTime. If not specified, this will be the time of the latest event in the event log.
    :type endTime: datetime.datetime
    :param cycle: Combines diffrent repeating timeframes. Best example would be days in a week.
        Needs to be a multiple of the interval. Use a    datetime.timedelta object for all short timespans,
        and a string consisting of a (optional) (Standart: 1) number(integer) and unit (either month or year) for longer timespans.
        Cycle and interval must be of the same type.
    :type cycle: datetime.timedelta or str
    :param aligned: Specifies if the intervaledges should be aligned to higher units of time.
        Note: for this to do anything, the interval must perfectly divide a higher unit of time.
        Note: intervals specified by a datetime.timedelta, this will only align up to days, not weeks, months or years
        As example an interval of 1 hour would always have the seperation at minute 0, instead of the minute specified in starttime.
    :type aligned: bool
    :returns: A List of intervals, and how often events occured. This is the form of a list of tuples.
        Each tuple contains as it's first element a tuple that defines the times in which an event had to occur to be counted. 
        and the sencond value is the number of counts.
        For cycles these are the times of the first occurence.
    :rtype: list
    """

    if eventLog is None:
        raise TypeError("A PM4PY Event Log is required.")
    if type(eventLog) != pm4py.objects.log.obj.EventLog:
        raise TypeError("A PM4PY Event Log is required.")

    if type(eventList) != list:
        if type(eventList) == str:
            eventList = [eventList]
        else:
            raise TypeError("The eventList is not a List, or a string")

    mode = 0
    if type(interval) != datetime.timedelta:
        if type(interval) == str:
            try:
                intervalNumber, intervalType = __parseDToS(interval)
            except ValueError:
                raise ValueError("Interval String is not of a correct format.")
            mode = 1
        else:
            raise TypeError("The type of interval must be a string or datetime.timedelta")

    if startTime is None:
        starttime = __firstEventTime(eventLog)
    elif type(startTime) != datetime.datetime:
        raise TypeError("The type of startTime needs to be datetime.datetime")

    if endTime is None:
        endTime = __lastEventTime(eventLog)
    elif type(endTime) != datetime.datetime:
        raise TypeError("The type of endTime needs to be datetime.datetime")

    intervalsinCycle = 0
    if cycle is not None:
        if type(cycle) != type(interval):
            raise TypeError("The type of cycle and intervall must be the same")
        elif type(cycle) != datetime.timedelta:
            try:
                cycleNumber, cycleType = __parseDToS(cycle)
            except ValueError:
                raise ValueError("Cycle String is not of a correct format.")
            cycleMonths = cycleNumber if cycleType == "month" else cycleNumber * 12
            intervalMonths = intervalNumber if intervalType == "month" else intervalNumber * 12
            if intervalMonths % cycleMonths != 0:
                raise ValueError("The cycle must be a multiple of the interval")
            intervalsinCycle = intervalMonths // cycleMonths
        else:
            if interval % cycle != 0:
                raise ValueError("The cycle must be a multiple of the interval")
            intervalsinCycle = interval // cycle

    if type(aligned) != bool:
        raise TypeError("The type of aligned needs to be a bool.")

    relevantEvents = []
    for trace in eventLog:
        for event in trace:
            if starttime <= event["time:timestamp"] <= endTime:
                if eventList.__contains__(event["concept:name"]):
                    relevantEvents.append(event)

    relevantEvents.sort(key=lambda event: event['time:timestamp'])
    values = []
    if aligned:
        if mode == 0:
            intervalMicroseconds = interval.microseconds + 1000000 * (interval.seconds + interval.days * 3600 * 24)
            originalMicroseconds = starttime.microsecond + 1000000 * (
                        starttime.second + 60 * (starttime.minute + 60 * starttime.hour))
            if (1000000 * 3600 * 24) % intervalMicroseconds == 0:
                t = starttime - datetime.timedelta(microseconds=originalMicroseconds % intervalMicroseconds)
            else:
                t = starttime
        else:
            t = starttime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        pass
    else:
        t = starttime
    i = 0
    while t < endTime:
        if mode == 0:
            nt = t + interval
        else:
            nt = t
            if intervalType == "month":
                n = nt.month + intervalNumber
                try:
                    nt = nt.replace(year=nt.year + (n + 1 // 12), month=n % 12 if n % 12 != 0 else 12)
                except ValueError:
                    n = n + 1
                    nt = nt.replace(year=nt.year + (n + 1 // 12), month=n % 12 if n % 12 != 0 else 12, day=1)
            else:
                try:
                    nt = nt.replace(year=nt.year + intervalNumber)
                except ValueError:
                    nt = nt.replace(year=nt.year + intervalNumber, month=3, day=1)
        if cycle is None or i < intervalsinCycle:
            te = (t, nt)
            values.append((te, 0))
            if cycle is None:
                ri = i
            else:
                ri = i % intervalsinCycle
        else:
            ri = i
        t = nt
        while relevantEvents and relevantEvents[0]['time:timestamp'] < t:
            values[ri] = (values[ri][0], values[ri][1] + 1)
            relevantEvents.pop(0)
        i = i + 1

    return values


def __parseDToS(string: str):
    s = string.replace(" ", "")
    t = s.lstrip("0123456789")
    n = s[:-len(t)]
    if n == "":
        n = 1
    else:
        n = int(n)
    if t[:5] == "month":
        return n, "month"
    if t[:4] == "year":
        return n, "year"
    raise ValueError("string incorrect")

def __firstEventTime(eventLog):
    earliestTime = datetime.datetime(2025, 1, 1, tzinfo=eventLog[0][0]["time:timestamp"].tzinfo)
    for trace in eventLog:
        for event in trace:
            if earliestTime > event["time:timestamp"]:
                earliestTime = event["time:timestamp"]
    return earliestTime


def __lastEventTime(eventLog):
    lastTime = datetime.datetime(1970, 1, 2, tzinfo=eventLog[0][0]["time:timestamp"].tzinfo)
    for trace in eventLog:
        for event in trace:
            if lastTime < event["time:timestamp"]:
                lastTime = event["time:timestamp"]
    return lastTime


#st = datetime.fromtimestamp(100000000)
#et = datetime.fromtimestamp(200000000)
#bh_object = BusinessHours(st, et)
#worked_time = bh_object.getseconds()
#print(worked_time)
#time_difference = endTime[datetime.datetime] - starttime [datetime.datetime]
#histogram = (x , bins = None )


x = [eventList]
y = interval

plt.hist(x, y ,bin = 10, ec "blue")
plt.title('QueueArrivalRateAnalysis')
plt.xlabel('EventTime')
plt.ylabel('EventCount')
plt.show()






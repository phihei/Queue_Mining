import pm4py
import datetime
import re


def analyzeServiceDiscipline(eventLog, queueDict):
    """
    Analyzes the service discipline of events in an event Log.

    :param eventLog: A PM4PY event log
    :type eventLog: pm4py.objects.log.obj.EventLog
    :param queueDict: A dictionary. The values of this dictionary are 2-Tuples,
    whos values are either strings or lists of strings, corresponding to
    activities from the event log. The first value of the tuple corresponds to events
    after which the case is available for servicing, the 2nd value of the tuple
    corresponds to events that signal that the case has begun servicing.
    :type queueDict: dict
    :returns: A dictionary with the same keys as queueDict, with the values being
    n-Tuples of floats that correspond to percentages for adherance to diffrent
    potential Service Disciplines (FIFO-Adherance, LIFO-Adherance, other)
    TODO define which Service Disciplines we are testing for
    :rtype: tuple
    """
    # TODO implemtation
    return -1


def analyzeServiceTimes(eventLog, serviceDict):
    """
    Analyzes the service times of services in an event Log.

    :param eventLog: A PM4PY event log
    :type eventLog: pm4py.objects.log.obj.EventLog
    :param serviceDict: A dictionary. The values of this dictionary are 2-Tuples,
    whos values are either strings or lists of strings, corresponding to
    activities from the event log. The first value of the tuple corresponds to events
    that occur at the beginning of servicing, the 2nd value of the tuple
    corresponds to events that signal that the case has finished servicing.
    :type serviceDict: dict
    :returns: TODO find good way to represent this
    :rtype:
    """
    # TODO implemtation
    return -1


def analysisQueueArrivalRate(eventLog, eventList, interval, startTime=None, endTime=None, cycle=None, aligned=True):
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
    and unit (either month or year) for longer.
    Note: If an edge land on a day that doesn't exist (like a 29th of non leap year feburary or 31st of april, at that point
    the edge will move forward to the 1st of the next month, (and stay on the first of that month)
    :type interval: datetime.timedelta or str
    :param startTime: Only Counts events after StartTime. If not specified, this will be the time of the earliest event in the event log.
    :type startTime: datetime.datetime
    :param endTime: Only Counts events before StartTime. If not specified, this will be the time of the latest event in the event log.
    :type endTime: datetime.datetime
    :param aligned: Specifies if the intervaledges should be aligned to higher units of time.
    Note: for this to do anything, the interval must perfectly divide a higher unit of time.
    Note: intervals specified by a datetime.timedelta, this will only align up to days, not weeks, months or years
    As example an interval of 1 hour would always have the seperation at minute 0, instead of the minute specified in starttime.
    :type aligned: bool
    :returns: TODO find good way to represent this
    :rtype:
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
            intervalnumber, intervaltype = parseInterval(interval)
            mode = 1
        else:
            raise TypeError("The tyoe of interval must be a string or datetime.timedelta")

    if startTime is None:
        starttime = firstEventTime(eventLog)

    if endTime is None:
        endTime = lastEventTime(eventLog)

    relevantEvents = []
    for trace in eventLog:
        for event in trace:
            if starttime <= event["time:timestamp"] <= endTime:
                if eventList.__contains__(event["concept:name"]):
                    relevantEvents.append(event)

    relevantEvents.sort(key=lambda event: event['time:timestamp'])
    values = []
    if cycle is None:
        if aligned:
            if mode == 0:
                intervalMicroseconds = interval.microseconds + 1000000 * (interval.seconds + interval.days * 3600 * 24)
                originalMicroseconds = starttime.microsecond + 1000000 * (starttime.second + 60 * (starttime.minute + 60 * starttime.hour))
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
                if intervaltype == "month":
                    n = nt.month + intervalnumber
                    try:
                        nt = nt.replace(year=nt.year + (n + 1 // 12), month=n % 12 if n % 12 != 0 else 12)
                    except ValueError:
                        n = n + 1
                        nt = nt.replace(year=nt.year + (n + 1 // 12), month=n % 12 if n % 12 != 0 else 12, day=1)
                else:
                    try:
                        nt = nt.replace(year=nt.year + intervalnumber)
                    except ValueError:
                        nt = nt.replace(year=nt.year + intervalnumber, month=3, day=1)
            te = (t, nt)
            t = nt
            values.append((te, 0))
            while relevantEvents and relevantEvents[0]['time:timestamp'] < t:
                values[i] = (values[i][0], values[i][1] + 1)
                relevantEvents.pop(0)
            i = i + 1

    return values


def parseInterval(interval):
    t = interval.lstrip("0123456789")
    n = interval[:-len(t)]
    if n == "":
        n = 1
    else:
        n = int(n)
    if t[:5] == "month":
        return n, "month"
    if t[:4] == "year":
        return n, "year"
    raise ValueError("Interval String incorrect")


def firstEventTime(eventLog):
    earliestTime = datetime.datetime(2025, 1, 1, tzinfo=eventLog[0][0]["time:timestamp"].tzinfo)
    for trace in eventLog:
        for event in trace:
            if earliestTime > event["time:timestamp"]:
                earliestTime = event["time:timestamp"]
    return earliestTime


def lastEventTime(eventLog):
    lastTime = datetime.datetime(1970, 1, 2, tzinfo=eventLog[0][0]["time:timestamp"].tzinfo)
    for trace in eventLog:
        for event in trace:
            if lastTime < event["time:timestamp"]:
                lastTime = event["time:timestamp"]
    return lastTime


def convertInterval(interval, intervalUnits):
    if intervalUnits == "days":
        return datetime.timedelta(days=interval)
    if intervalUnits == "seconds":
        return datetime.timedelta(seconds=interval)
    if intervalUnits == "microseconds":
        return datetime.timedelta(microseconds=interval)
    if intervalUnits == "milliseconds":
        return datetime.timedelta(milliseconds=interval)
    if intervalUnits == "minutes":
        return datetime.timedelta(minutes=interval)
    if intervalUnits == "hours":
        return datetime.timedelta(hours=interval)
    if intervalUnits == "weeks":
        return datetime.timedelta(weeks=interval)
    raise ValueError(
        "IntervalUnits are not an accepted IntervalUnits (microseconds, milliseconds, seconds, minutes, hours, days or weeks")

import pm4py
import datetime

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

def analysisQueueArrivalRate(eventLog, eventList, interval, intervalUnit="days", startTime=None, endTime=None, cycle=None):
    """
    Analyzes the Arrival times customers.

    :param eventLog: A PM4PY event log
    :type eventLog: pm4py.objects.log.obj.EventLog
    :param eventList: A List. The values of this List are either Strings, if
    only a single Activity in the event log signalizes Arrival, or a list of
    strings, im multiple Activities lead to customers waiting on the same service.
    :type eventList: list
    :param interval:
    :type interval: int, float or string
    :param startTime: Only Counts events after StartTime
    :type startTime: datetime
    :param endTime: Only Counts events before StartTime
    :type endTime: datetime
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

    if type(interval) == str:
        rInterval = parseString1(interval)
    elif type(interval) == int or type(interval) == float:
        if interval == 0:
            raise ValueError("interval can't be 0.")
        rInterval = interval
    else:
        raise TypeError("The tyoe of interval must be a string or float")

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
        t = starttime + datetime.timedelta(days=interval)
        i = 0
        while t < endTime:
            values.append(0)
            while relevantEvents[0]['time:timestamp'] < t:
                values[i] = values[i] + 1
                relevantEvents.pop(0)
            t = t + datetime.timedelta(days=interval)
            i = i+1

    return values

def parseString1(string):
    return 1

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


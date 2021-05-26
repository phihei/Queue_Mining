
def analyzeServiceDiscipline(eventLog, queueDict):
    """
    Analyzes the service discipline of events in an event Log.

    :param eventLog: A PM4PY event log
    :type eventLog: PM4PY.EventLog
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
    :type eventLog: PM4PY.EventLog
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

def analysisQueueArrivalRate(eventLog, eventList):
    """
    Analyzes the Arrival times customers.

    :param eventLog: A PM4PY event log
    :type eventLog: PM4PY.EventLog
    :param eventList: A List. The values of this List are either Strings, if
    only a single Activity in the event log signalizes Arrival, or a list of
    strings, im multiple Activities lead to customers waiting on the same service.
    :type eventList: list
    :returns: TODO find good way to represent this
    :rtype:
    """
    # TODO implemtation
    return -1


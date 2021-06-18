def analyzeServiceDiscipline(eventLog, queueDict):
    """
    Analyzes the service discipline of events in an event Log.
    THIS IS STILL EMPTY AND ONLY RETURNS -1 AT THE MOMENT.

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

    :rtype: tuple
    """
    # TODO implemtation
    return -1


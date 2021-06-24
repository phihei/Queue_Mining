"""
 method, given an event log, to derive context
information on the workload over time. In addition, a method is introduced that allows adding
context information to the context attributes of events.
Workload information is in essence information about how busy or not busy the system is at some
point in time. The goal is to determine for each day how busy that day is.
methods:
1: The first is for each day to look at the
global arrival rate and global service rate and define the workload as the service rate divided by
the arrival rate and bin these workloads in a small number of classes.
2: sum the arrival rate over the last weeks and take this as the workload. Then bin these workloads
in a small number of classes.
3:  find the workload for each day by looking
at the arrival rates in some window. Then, the workload class is defined by taking the average
workload of the entire historical data and using the standard deviation to define classes for busy,
quiet and regular


map arrival rate to resources or activities

"""


def processWorkload(log, timespan, metric):
    """
    This function return the desired workload for one process. timespan defines whether the workload is calculated for
    one day, one hour, or one week. The value can be passed as datetime or timespan of seconds with a starting point.
    "Assume an ordered list of workload values is
supplied where workload(d) indicates the workload on day d, i.e. the amount of activities arrived
in a window of 7 days around d. "

ordered list of workload values
workload(d) indicates the workload on day d, i.e. the amount of activities arrived
in a window of 7 days around d.


    :param log:
    :param timespan:
    :return:
    """


def workloadStat(workload(d), nDays):
    """
    Output is the mean workload and the std workload
    NRDAY S indicates the range of days in log L
    :return:
    """

def workloadContext(meanW, stdW):
    """
    Classifies the workload for a desired time window as quiet (if workload(d) < meanW − stdW),
    busy(if workload(d) > meanW + stdW) or regular(otherwise)
    :param meanW:
    :param stdW:
    :return:
    """

def workloadTable(timeWindow):
    """
    Table 3.1: Context workload example values

    :param timeWindow:
    :return:
    """
""""
https://svn.win.tue.nl/repos/prom/Packages/QueueMiner/Trunk/src/org/processmining/models/queueminer/utils/Queue.java
Queues for an entire eventlog? How should we use it as a class?
3.1.3 Finding basic queues

"""
class Queues:
    resources = []
    activities = []
    arrivalRate = 0 #poisson arrival rate
    meanWork  = 0 # mean working time
    stdWork = 0 # std dev time
    queueServiceRate = {} #Hkey activity/queue, value serviceRate HashMap < String, HashMap < Integer, ArrayList < Point >> >
    queueArrivalRate = {} # key activity/queue, value arrivalRate HashMap < String, HashMap < Integer, Integer >>
    serviceDiscipline = {} #
    subTime

    def simpleQueue(log, activity):
        """
        This function aggregates the cases that are queued before beeing executed by an activity. So for the whole event log
        this function return a time interval and case IDs of cases that where queued.


        :param log:
        :param activity:
        :return:
        """

    def fairShareAttention_workthreshhold():


    def basicQueue():
        """
            "Table 3.7" classifying queues with activities and resources
            "cluster all resources and activities that occur in the event log such that
    each cluster of resources and activities accurately represents the servers and work items at a
    queue and workstation in the real process. As input for this method we have an event log and
    as output a set of basic queues which are useful for finding a queue collection."
        :return:
        """
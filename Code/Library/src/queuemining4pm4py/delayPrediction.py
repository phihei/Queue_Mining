import datetime

import pm4py


class DelayPredictor:

    def __init__(self, eventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent, serviceEndEvent, PARAMETERS=None):
        self.eventLog = eventLog
        process_tree = pm4py.discover_process_tree_inductive(eventLog)
        self.model = pm4py.convert_to_bpmn(process_tree)
        self.PTSSum = datetime.timedelta(seconds=0)
        self.PTSN = 0
        self.q = list()
        self.LES = None
        self.HOL = None
        self.annotation = self.annotate(eventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent, serviceEndEvent)

    def annotate(self, eventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent, serviceEndEvent):
        dictionary = dict()
        for node in self.model.get_nodes():
            dictionary[node] = [0, 0, 0]

        lesTime = None
        holTime = None
        for trace in eventLog:
            for i in range(len(trace) - 1):
                if trace[i]["concept:name"] == "EnterQueue" and trace[i+1]["concept:name"] == "ServiceStart":
                    wait = trace[i+1]["time:timestamp"] - trace[i]["time:timestamp"]
                    self.PTSSum = self.PTSSum + wait
                    self.PTSN = self.PTSN + 1
                    if lesTime is None or lesTime < trace[i+1]["time:timestamp"]:
                        lesTime = trace[i+1]["time:timestamp"]
                        self.LES = wait
            if trace[len(trace) - 1]["concept:name"] == "EnterQueue":
                if holTime is None or holTime > trace[len(trace) - 1]["time:timestamp"]:
                    holTime = trace[len(trace) - 1]["time:timestamp"]
                    self.HOL = trace[len(trace) - 1]["time:timestamp"]
                self.q.append((trace[len(trace) - 1]["time:timestamp"], trace.attributes["concept:name"]))

        self.q.sort(key=lambda customers: customers[0])

        return dictionary

    def getPTSPrediction(self, customer, currentTime=None):
        if currentTime is None:
            currentTime = datetime.datetime.now()
        customerTrace = None
        for trace in self.eventLog:
            if trace.attributes["concept:name"] == str(customer):
                customerTrace = trace
                break
        if customerTrace is None:
            raise ValueError("Couldn't find the speficfied customer")

        if self.PTSN != 0:
            predictedWait = self.PTSSum / self.PTSN
        else:
            predictedWait = self.PTSSum
        customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]
        customerQueueDuration = currentTime - customerQueueTime
        return max(predictedWait - customerQueueDuration, datetime.timedelta(seconds=0))

    def getQLPPrediction(self, customer, numServiceProviders, serviceProviderMeanTimes, currentTime=None):
        if currentTime is None:
            currentTime = datetime.datetime.now()
        customerTrace = None
        for trace in self.eventLog:
            if trace.attributes["concept:name"] == str(customer):
                customerTrace = trace
                break
        if customerTrace is None:
            raise ValueError("Couldn't find the speficfied customer")

        customerQueuePosition = 0
        while customerQueuePosition < len(self.q):
            if self.q[customerQueuePosition][1] == str(customer):
                break
            else:
                customerQueuePosition = customerQueuePosition + 1

        return (serviceProviderMeanTimes * (customerQueuePosition + 1)) / numServiceProviders

    def getQLMPPrediction(self, customer, numServiceProviders, serviceProviderMeanTimes: datetime.timedelta, customerAbandonRate, currentTime=None):
        if currentTime is None:
            currentTime = datetime.datetime.now()
        customerTrace = None
        for trace in self.eventLog:
            if trace.attributes["concept:name"] == str(customer):
                customerTrace = trace
                break
        if customerTrace is None:
            raise ValueError("Couldn't find the speficfied customer")

        customerQueuePosition = 0
        while customerQueuePosition < len(self.q):
            if self.q[customerQueuePosition][1] == str(customer):
                break
            else:
                customerQueuePosition = customerQueuePosition + 1

        my = 1 / serviceProviderMeanTimes.total_seconds()
        waitTime = datetime.timedelta(seconds=0)
        for i in range(customerQueuePosition):
            waitTime = waitTime + datetime.timedelta(seconds=1 / (numServiceProviders * my + i * customerAbandonRate))

        return waitTime

    def getLESPrediction(self, customer, currentTime=None):

        if currentTime is None:
            currentTime = datetime.datetime.now()
        customerTrace = None
        for trace in self.eventLog:
            if trace.attributes["concept:name"] == str(customer):
                customerTrace = trace
                break
        if customerTrace is None:
            raise ValueError("Couldn't find the speficfied customer")

        customerQueuePosition = 0
        while customerQueuePosition < len(self.q):
            if self.q[customerQueuePosition][1] == str(customer):
                break
            else:
                customerQueuePosition = customerQueuePosition + 1

        customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]
        customerQueueDuration = currentTime - customerQueueTime

        return max(self.LES - customerQueueDuration, datetime.timedelta(seconds=0))

    def getHOLPrediction(self, customer, currentTime=None):

        if currentTime is None:
            currentTime = datetime.datetime.now()
        customerTrace = None
        for trace in self.eventLog:
            if trace.attributes["concept:name"] == str(customer):
                customerTrace = trace
                break
        if customerTrace is None:
            raise ValueError("Couldn't find the speficfied customer")

        customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]

        return customerQueueTime - self.HOL



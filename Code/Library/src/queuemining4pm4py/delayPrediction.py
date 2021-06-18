import datetime
import pm4py


class DelayPredictor:

    def __init__(self, eventLog: pm4py.objects.Eventlog, queueEntryEvent, queueAbandonEvent, serviceStartEvent,
                 serviceEndEvent):
        self.eventLog = eventLog
        self.queueEntryEvent = queueEntryEvent
        self.queueAbandonEvent = queueAbandonEvent
        self.serviceStartEvent = serviceStartEvent
        self.serviceEndEvent = serviceEndEvent
        self.PTSSum = datetime.timedelta(seconds=0)
        self.PTSN = 0
        self.q = list()
        self.LES = None
        self.HOL = None
        self.__annotate()

    def updateEventLog(self, eventLog):
        self.eventLog = eventLog
        self.__annotate()

    def __annotate(self):
        lesTime = None
        holTime = None
        for trace in self.eventLog:
            for i in range(len(trace) - 1):
                if trace[i]["concept:name"] == self.queueEntryEvent and trace[i + 1][
                    "concept:name"] == self.serviceStartEvent:
                    wait = trace[i + 1]["time:timestamp"] - trace[i]["time:timestamp"]
                    self.PTSSum = self.PTSSum + wait
                    self.PTSN = self.PTSN + 1
                    if lesTime is None or lesTime < trace[i + 1]["time:timestamp"]:
                        lesTime = trace[i + 1]["time:timestamp"]
                        self.LES = wait
            if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                if holTime is None or holTime > trace[len(trace) - 1]["time:timestamp"]:
                    holTime = trace[len(trace) - 1]["time:timestamp"]
                    self.HOL = trace[len(trace) - 1]["time:timestamp"]
                self.q.append((trace[len(trace) - 1]["time:timestamp"], trace.attributes["concept:name"]))

        self.q.sort(key=lambda customers: customers[0])

    def getPTSPrediction(self, customer, currentTime: datetime.datetime = None):
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

    def getAllPTSPredictions(self, currentTime: datetime.datetime = None):
        if currentTime is None:
            currentTime = datetime.datetime.now()
        if self.PTSN != 0:
            predictedWait = self.PTSSum / self.PTSN
        else:
            predictedWait = self.PTSSum
        result = dict()
        for trace in self.eventLog:
            if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                customerQueueDuration = currentTime - customerQueueTime
                result[trace.attributes["concept:name"]] = max(predictedWait - customerQueueDuration,
                                                               datetime.timedelta(seconds=0))
        return result

    def getQLPPrediction(self, customer, numServiceProviders, serviceProviderMeanTimes):
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

    def getAllQLPPrediction(self, numServiceProviders, serviceProviderMeanTimes):
        result = dict()
        for index, customer in enumerate(self.q):
            result[self.q[index][0]] = (serviceProviderMeanTimes * (index + 1)) / numServiceProviders
        return result

    def getQLMPPrediction(self, customer, numServiceProviders, serviceProviderMeanTimes: datetime.timedelta,
                          customerAbandonRate):
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

    def getAllQLMPPrediction(self, numServiceProviders, serviceProviderMeanTimes: datetime.timedelta,
                             customerAbandonRate):
        result = dict()
        my = 1 / serviceProviderMeanTimes.total_seconds()
        for index, customer in enumerate(self.q):
            if index == 0:
                result[self.q[index][0]] = datetime.timedelta(
                    seconds=1 / (numServiceProviders * my + index * customerAbandonRate))
            else:
                result[self.q[index][0]] = result[self.q[index - 1][0]] + datetime.timedelta(
                    seconds=1 / (numServiceProviders * my + index * customerAbandonRate))
        return result

    def getLESPrediction(self, customer, currentTime: datetime.datetime = None):
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
        customerQueueDuration = currentTime - customerQueueTime
        return max(self.LES - customerQueueDuration, datetime.timedelta(seconds=0))

    def getAllLESPrediction(self, currentTime: datetime.datetime = None):
        if currentTime is None:
            currentTime = datetime.datetime.now()
        result = dict()
        for trace in self.eventLog:
            if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                customerQueueDuration = currentTime - customerQueueTime
                result[trace.attributes["concept:name"]] = max(self.LES - customerQueueDuration,
                                                               datetime.timedelta(seconds=0))
        return result

    def getHOLPrediction(self, customer):
        customerTrace = None
        for trace in self.eventLog:
            if trace.attributes["concept:name"] == str(customer):
                customerTrace = trace
                break
        if customerTrace is None:
            raise ValueError("Couldn't find the speficfied customer")
        customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]
        return customerQueueTime - self.HOL

    def getAllHOLPrediction(self):
        result = dict()
        for trace in self.eventLog:
            if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                result[trace.attributes["concept:name"]] = customerQueueTime - self.HOL
        return result
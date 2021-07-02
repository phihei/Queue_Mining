import datetime
import pm4py


class DelayPredictor:

    def __init__(self, eventLog: pm4py.objects.log.obj.EventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent,
                 classes=None):
        self.eventLog = eventLog
        self.queueEntryEvent = queueEntryEvent
        self.queueAbandonEvent = queueAbandonEvent
        self.serviceStartEvent = serviceStartEvent
        self.PTSSum = datetime.timedelta(seconds=0)
        self.PTSN = 0
        self.q = list()
        self.LES = None
        self.HOL = None

        self.multiClassSetting = False
        if classes is not None:
            self.multiClassSetting = True
        self.classes = classes

        self.PTSSums = dict()
        self.PTSNs = dict()
        self.LESs = dict()
        self.HOLs = dict()
        self.qs = dict()

        if self.multiClassSetting:
            for classs in self.classes:
                self.PTSSums[classs] = datetime.timedelta(seconds=0)
                self.PTSNs[classs] = 0
                self.qs[classs] = list()
                self.LESs[classs] = None
                self.HOLs[classs] = None


        self.__annotate()

    def updateEventLog(self, eventLog):
        self.eventLog = eventLog
        self.__annotate()

    def __annotate(self):

        self.PTSSum = datetime.timedelta(seconds=0)
        self.PTSN = 0
        self.q = list()
        self.LES = None
        self.HOL = None

        self.PTSSums = dict()
        self.PTSNs = dict()
        self.LESs = dict()
        self.HOLs = dict()
        self.qs = dict()

        if self.multiClassSetting:
            for classs in self.classes:
                self.PTSSums[classs] = datetime.timedelta(seconds=0)
                self.PTSNs[classs] = 0
                self.qs[classs] = list()
                self.LESs[classs] = None
                self.HOLs[classs] = None

        if not self.multiClassSetting:
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
        else:
            lesTimes = dict()
            holTimes = dict()
            for classs in self.classes:
                lesTimes[classs] = None
                holTimes[classs] = None

            for trace in self.eventLog:
                classs = trace.attributes["class"]
                for i in range(len(trace) - 1):
                    if trace[i]["concept:name"] == self.queueEntryEvent and trace[i + 1][
                        "concept:name"] == self.serviceStartEvent:
                        wait = trace[i + 1]["time:timestamp"] - trace[i]["time:timestamp"]
                        self.PTSSums[classs] = self.PTSSums[classs] + wait
                        self.PTSNs[classs] = self.PTSNs[classs] + 1
                        if lesTimes[classs] is None or lesTimes[classs] < trace[i + 1]["time:timestamp"]:
                            lesTimes[classs] = trace[i + 1]["time:timestamp"]
                            self.LESs[classs] = wait
                if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                    if holTimes[classs] is None or holTimes[classs] > trace[len(trace) - 1]["time:timestamp"]:
                        holTimes[classs] = trace[len(trace) - 1]["time:timestamp"]
                        self.HOLs[classs] = trace[len(trace) - 1]["time:timestamp"]
                    self.qs[classs].append((trace[len(trace) - 1]["time:timestamp"], trace.attributes["concept:name"]))

            for classs in self.classes:
                self.qs[classs].sort(key=lambda customers: customers[0])

    def getPTSPrediction(self, customer, currentTime: datetime.datetime = None):
        if self.multiClassSetting:
            if currentTime is None:
                currentTime = datetime.datetime.now()
            customerTrace = None
            for trace in self.eventLog:
                if trace.attributes["concept:name"] == str(customer):
                    customerTrace = trace
                    break
            if customerTrace is None:
                raise ValueError("Couldn't find the speficfied customer")
            classs = customerTrace.attributes["class"]
            if self.PTSNs[classs] != 0:
                predictedWait = self.PTSSums[classs] / self.PTSNs[classs]
            else:
                predictedWait = self.PTSSums[classs]
            customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]
            customerQueueDuration = currentTime - customerQueueTime
            return max(predictedWait - customerQueueDuration, datetime.timedelta(seconds=0))
        else:
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
        if self.multiClassSetting:
            if currentTime is None:
                currentTime = datetime.datetime.now()

            predictedWaits = dict()
            for classs in self.classes:
                if self.PTSN != 0:
                    predictedWaits[classs] = self.PTSSums[classs] / self.PTSNs[classs]
                else:
                    predictedWaits[classs] = self.PTSSums[classs]
            result = dict()
            for trace in self.eventLog:
                classs = trace.attributes["class"]
                if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                    customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                    customerQueueDuration = currentTime - customerQueueTime
                    result[trace.attributes["concept:name"]] = max(predictedWaits[classs] - customerQueueDuration,
                                                                   datetime.timedelta(seconds=0))
            return result
        else:
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
        if self.multiClassSetting:
            raise NotImplementedError("QLP is not implemented for multi class settings.")


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
        if self.multiClassSetting:
            raise NotImplementedError("QLP is not implemented for multi class settings.")
        result = dict()
        for index, customer in enumerate(self.q):
            result[self.q[index][0]] = (serviceProviderMeanTimes * (index + 1)) / numServiceProviders
        return result

    def getQLMPPrediction(self, customer, numServiceProviders, serviceProviderMeanTimes: datetime.timedelta,
                          customerAbandonRate):
        if self.multiClassSetting:
            raise NotImplementedError("QLMP is not implemented for multi class settings.")
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

        if self.multiClassSetting:
            raise NotImplementedError("QLMP is not implemented for multi class settings.")
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
        if self.multiClassSetting:
            if currentTime is None:
                currentTime = datetime.datetime.now()
            customerTrace = None
            for trace in self.eventLog:
                if trace.attributes["concept:name"] == str(customer):
                    customerTrace = trace
                    break
            if customerTrace is None:
                raise ValueError("Couldn't find the speficfied customer")
            classs = customerTrace.attributes["class"]
            customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]
            customerQueueDuration = currentTime - customerQueueTime
            return max(self.LESs[classs] - customerQueueDuration, datetime.timedelta(seconds=0))
        else:
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
        if self.multiClassSetting:
            if currentTime is None:
                currentTime = datetime.datetime.now()
            result = dict()
            for trace in self.eventLog:
                classs = trace.attributes["class"]
                if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                    customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                    customerQueueDuration = currentTime - customerQueueTime
                    result[trace.attributes["concept:name"]] = max(self.LESs[classs] - customerQueueDuration,
                                                                   datetime.timedelta(seconds=0))
            return result
        else:
            if currentTime is None:
                currentTime = datetime.datetime.now()
            result = dict()
            for trace in self.eventLog:
                if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                    customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                    customerQueueDuration = currentTime - customerQueueTime
                    result[trace.attributes["concept:name"]] = max(self.LESs - customerQueueDuration,
                                                                   datetime.timedelta(seconds=0))
            return result


    def getHOLPrediction(self, customer):
        if self.multiClassSetting:
            customerTrace = None
            for trace in self.eventLog:
                if trace.attributes["concept:name"] == str(customer):
                    customerTrace = trace
                    break
            if customerTrace is None:
                raise ValueError("Couldn't find the speficfied customer")
            classs = customerTrace.attributes["class"]
            customerQueueTime = customerTrace[len(customerTrace) - 1]["time:timestamp"]
            return customerQueueTime - self.HOLs[classs]
        else:
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
        if self.multiClassSetting:
            result = dict()
            for trace in self.eventLog:
                classs = trace.attributes["class"]
                if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                    customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                    result[trace.attributes["concept:name"]] = customerQueueTime - self.HOLs[classs]
            return result

        else:
            result = dict()
            for trace in self.eventLog:
                if trace[len(trace) - 1]["concept:name"] == self.queueEntryEvent:
                    customerQueueTime = trace[len(trace) - 1]["time:timestamp"]
                    result[trace.attributes["concept:name"]] = customerQueueTime - self.HOL
            return result

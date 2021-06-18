import datetime

import pm4py


class DelayPredictor:

    def __init__(self, eventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent, serviceEndEvent, PARAMETERS=None):
        process_tree = pm4py.discover_process_tree_inductive(eventLog)
        self.model = pm4py.convert_to_bpmn(process_tree)
        self.PTSSum = datetime.timedelta(seconds=0)
        self.PTSN = 0
        self.annotation = self.annotate(eventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent, serviceEndEvent)

    def annotate(self, eventLog, queueEntryEvent, queueAbandonEvent, serviceStartEvent, serviceEndEvent):
        dictionary = dict()
        for node in self.model.get_nodes():
            dictionary[node] = [0, 0, 0]

        for trace in eventLog:
            for i in range(len(trace) - 1):
                if trace[i]["concept:name"] == "EnterQueue" and trace[i+1]["concept:name"] == "ServiceStart":
                    wait = trace[i+1]["time:timestamp"] - trace[i]["time:timestamp"]
                    self.PTSSum = self.PTSSum + wait
                    self.PTSN = self.PTSN + 1

        print("Done")

        return dictionary

    def getPredictedWait(self, customer, predictor="PTS"):
        if predictor == "PTS":
            if self.PTSN != 0:
                return self.PTSSum / self.PTSN
            else:
                return self.PTSSum
        else:
            raise ValueError("Specified Predictor is either wrong or not yet implemented")



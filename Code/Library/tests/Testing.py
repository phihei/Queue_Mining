import unittest
import src.queuemining4pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
import warnings
import datetime

class TestLibrary(unittest.TestCase):
    def test_analyzeServiceDiscipline(self):
        pass

    def test_analyzeServiceTimes(self):
        pass

    def test_analysisQueueArrivalRate_for_ValueErrors(self):
        warnings.filterwarnings('ignore', category=ResourceWarning)
        log = xes_importer.apply("running-example.xes")
        self.assertRaises(ValueError, src.queuemining4pm4py.functions.analysisQueueArrivalRate, log, [], 0)

    def test_analysisQueueArrivalRate_for_TypeErrors(self):
        warnings.filterwarnings('ignore', category=ResourceWarning)
        self.assertRaises(TypeError, src.queuemining4pm4py.functions.analysisQueueArrivalRate, None, [], 1)
        self.assertRaises(TypeError, src.queuemining4pm4py.functions.analysisQueueArrivalRate, "EventLog", [], 1)
        log = xes_importer.apply("running-example.xes")
        self.assertRaises(TypeError, src.queuemining4pm4py.functions.analysisQueueArrivalRate, log, [], None)

    def test_analysisQueueArrivalRate_Behaviour(self):
        warnings.filterwarnings('ignore', category=ResourceWarning)
        log = xes_importer.apply("running-example.xes")
        values = src.queuemining4pm4py.functions.analysisQueueArrivalRate(log, 'register request', 1)
        self.assertListEqual(values, [3, 0, 0, 0, 0, 0, 1, 2])

if __name__ == '__main__':
    print("Main ran.")
    thislog = xes_importer.apply("running-example.xes")
    print(thislog)
    t1 = lastTime = datetime.datetime(1970, 1, 1, 0, 3)
    t2 = datetime.datetime(2000, 1, 2)
    print(t1)
    print(t2)
    print(t1 < t2)
    print(t1 > t2)

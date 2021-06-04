import unittest
import src.queuemining4pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
import warnings
import datetime


class TestAnalysisQueueArrivalRate(unittest.TestCase):

    def test_analysisQueueArrivalRate_for_ValueErrors(self):
        # Interval Value Checks
        warnings.filterwarnings('ignore', category=ResourceWarning)
        log = xes_importer.apply("running-example.xes")
        self.assertRaises(ValueError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], "1Day")
        self.assertRaises(ValueError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], "25Seconds")

        # Cycle Value Checks
        self.assertRaises(ValueError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], datetime.timedelta(days=2),
                          cycle=datetime.timedelta(days=3))
        self.assertRaises(ValueError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], "5 months", cycle="2 years")
        self.assertRaises(ValueError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], datetime.timedelta(days=2),
                          cycle=datetime.timedelta(days=3))
        self.assertRaises(ValueError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], "6 months", cycle="52 weeks")

    def test_analysisQueueArrivalRate_for_TypeErrors(self):
        # Event Log Type checks
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, None, "Event1",
                          datetime.timedelta(days=1))
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, "EventLog", ["Event1", "Event2"],
                          datetime.timedelta(days=1))

        # EventList Type checks
        warnings.filterwarnings('ignore', category=ResourceWarning)
        log = xes_importer.apply("running-example.xes")
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, None,
                          datetime.timedelta(days=1))
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, 1, datetime.timedelta(days=1))

        # Interval Type Checks
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, 'register request', None)
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, 'register request', 12)
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, 'register request', True)

        # Start and End times Checks
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, 'register request',
                          datetime.timedelta(days=1), True, False)
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], datetime.timedelta(days=1), "12th january",
                          "25th Febuary")

        # Cycle Type Checks
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], datetime.timedelta(days=1), cycle="1 month")
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], "2 years", datetime.timedelta(days=3650))

        # Aligned Type Checks
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log, 'register request',
                          datetime.timedelta(days=1), aligned=None)
        self.assertRaises(TypeError, src.queuemining4pm4py.analyzeQueueArrivalRate, log,
                          ['register request', 'reinitiate request'], aligned="True")


if __name__ == '__main__':
    pass

import unittest
import src.queuemining4pm4py
import warnings
import datetime
from pm4py.objects.log.importer.xes import importer as xes_importer


class TestAnalysisQueueArrivalRate(unittest.TestCase):

    def test_analysisQueueArrivalRate_for_ValueErrors(self):
        # Interval Value Checks
        warnings.filterwarnings('ignore', category=ResourceWarning)
        log = xes_importer.apply("logs/running-example.xes")
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
        log = xes_importer.apply("logs/running-example.xes")
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

    def test_delayPrediction_getPTSPrediction(self):
        log = xes_importer.apply('logs/delayPrediction/delayPrediction-example1.xes')
        delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart")
        waitPrediction = delayPredictor.getPTSPrediction(60, datetime.datetime(2021, 6, 18, 10))
        self.assertEqual(datetime.timedelta(seconds=0), waitPrediction)

    def test_delayPrediction_getQLPPrediction(self):
        log = xes_importer.apply('logs/delayPrediction/delayPrediction-example1.xes')
        delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart")
        waitPrediction = delayPredictor.getQLPPrediction(60, 2, datetime.timedelta(seconds=300))
        self.assertEqual(datetime.timedelta(seconds=1800), waitPrediction)

    def test_delayPrediction_getQLMPPrediction(self):
        log = xes_importer.apply('logs/delayPrediction/delayPrediction-example1.xes')
        delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart")
        waitPrediction = delayPredictor.getQLMPPrediction(60, 2, datetime.timedelta(seconds=300), 0.0001)
        self.assertEqual(datetime.timedelta(seconds=1537, microseconds=882536), waitPrediction)

    def test_delayPrediction_getLESPrediction(self):
        log = xes_importer.apply('logs/delayPrediction/delayPrediction-example1.xes')
        delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart")
        waitPrediction = delayPredictor.getLESPrediction(60, datetime.datetime(2021, 6, 18, 10))
        self.assertEqual(datetime.timedelta(seconds=650), waitPrediction)

    def test_delayPrediction_getHOLPrediction(self):
        log = xes_importer.apply('logs/delayPrediction/delayPrediction-example1.xes')
        delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart")
        waitPrediction = delayPredictor.getHOLPrediction(60)
        self.assertEqual(datetime.timedelta(seconds=713), waitPrediction)

if __name__ == '__main__':
    log = xes_importer.apply('logs/delayPrediction/delayPrediction-example1.xes')
    delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart")
    waitPrediction = delayPredictor.getPTSPrediction(60, datetime.datetime(2021, 6, 18, 10))
    print(f"Wait Prediction, Method: PTS {waitPrediction}")
    waitPrediction = delayPredictor.getQLPPrediction(60, 2, datetime.timedelta(seconds=300))
    print(f"Wait Prediction, Method: QLP {waitPrediction}")
    waitPrediction = delayPredictor.getQLMPPrediction(60, 2, datetime.timedelta(seconds=300), 0.0001)
    print(f"Wait Prediction, Method: QLMP {waitPrediction}")
    waitPrediction = delayPredictor.getLESPrediction(60, datetime.datetime(2021, 6, 18, 10))
    print(f"Wait Prediction, Method: LES {waitPrediction}")
    waitPrediction = delayPredictor.getHOLPrediction(60)
    print(f"Wait Prediction, Method: HOL {waitPrediction}")

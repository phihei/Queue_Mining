import unittest
import src.queuemining4pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
import warnings
import datetime

import pm4py

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.util import exec_utils, constants
from enum import Enum


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
    log = xes_importer.apply('delayPrediction-example1.xes')
    delayPredictor = src.queuemining4pm4py.DelayPredictor(log, "EnterQueue", "QueueAbandon", "ServiceStart",
                                                          "ServiceEnd")
    waitPrediction = delayPredictor.getPTSPrediction(60, datetime.datetime(2021, 6, 18, 10))
    print(f"PTS Delay Predictionn: {str(waitPrediction)}")
    waitPrediction = delayPredictor.getQLPPrediction(60, 2, datetime.timedelta(seconds=300),
                                                     datetime.datetime(2021, 6, 18, 10))
    print(f"QLP Delay Predictor: {str(waitPrediction)}")
    waitPrediction = delayPredictor.getQLMPPrediction(60, 2, datetime.timedelta(seconds=300), 0.0001,
                                                      datetime.datetime(2021, 6, 18, 10))
    print(f"QLMP Delay Predictor: {str(waitPrediction)}")
    waitPrediction = delayPredictor.getLESPrediction(60, datetime.datetime(2021, 6, 18, 10))
    print(f"LES Delay Predictor: {str(waitPrediction)}")
    waitPrediction = delayPredictor.getHOLPrediction(60, datetime.datetime(2021, 6, 18, 10))
    print(f"HOL Delay Predictor: {str(waitPrediction)}")
    print("Done!")


class Parameters(Enum):
    ATTRIBUTE_KEY = constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY


def others():
    variant = xes_importer.Variants.ITERPARSE
    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    log = xes_importer.apply('e.xes', variant=variant, parameters=parameters)

    # print(log)
    pm4py.view_performance_spectrum(log, ['register request', 'examine casually', 'check ticket', 'decide'],
                                    format="svg")

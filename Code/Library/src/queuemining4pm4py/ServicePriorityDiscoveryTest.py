import random

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
# import networkx as nx
import pm4py.objects.dfg.utils.dfg_utils as pm4pydfg
import pm4py

# import xes_to_nx_utilities
import statistics_logs
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.objects.log.util import interval_lifecycle
from pm4py.statistics.passed_time.log import algorithm
from pm4py.util import exec_utils, constants
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY
from datetime import datetime, timedelta
from pm4py.objects.log.exporter.xes import exporter as xes_expoter
from enum import Enum

from pm4py.algo.discovery.performance_spectrum.variants import dataframe, log, dataframe_disconnected, log_disconnected
from pm4py.util import exec_utils
import pkgutil
from enum import Enum
from pm4py.util import constants
from pm4py.algo.discovery.performance_spectrum import algorithm as performance_spectrum
from ServicePriorityDiscovery import ServicePriorityDiscovery
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

class Parameters(Enum):
    ATTRIBUTE_KEY = constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY


variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('running-example.xes', variant=variant, parameters=parameters)

# If the user puts 2 activities, then the function checks and shows result of Service priority.
# If the user puts one activity, then the function finds all the directly connected function with the activity and shows result for them.
activities = ['examine casually']
ServicePriorityDiscovery(log,activities)


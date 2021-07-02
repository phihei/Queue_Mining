
from pm4py.objects.log.importer.xes import importer as xes_importer

from enum import Enum
from pm4py.util import constants
from ServicePriorityDiscovery import ServicePriorityDiscovery

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


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import pm4py.objects.dfg.utils.dfg_utils as pm4pydfg
import xes_to_nx_utilities
import statistics_logs
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization




if __name__ == '__main__':
    variant = xes_importer.Variants.ITERPARSE
    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    log = xes_importer.apply('../../../../logs/running-example.xes', variant=variant, parameters=parameters)
    #
    # G = xes_to_nx_utilities.transform_xes_log_to_nxDiGraph(log, variant='inductive')
    #
    # nx.draw(G, with_labels=True)
    # plt.show()
    statistics_logs.case_duration_statistics(log, 1, vt='test')
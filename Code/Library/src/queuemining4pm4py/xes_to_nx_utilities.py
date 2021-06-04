import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import pm4py.objects.dfg.utils.dfg_utils
import pm4py.objects.petri_net.utils.networkx_graph
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.discovery.inductive import algorithm as inductive_miner



def transform_dfg_to_directed_nx_graph(dfg, activities=None) -> nx.DiGraph:
    """
    Transform DFG to directed NetworkX graph, adapted from existing function in PM4PY in dfg_utils.py.

     Parameters
        --------------
        dfg
            directly-follows graph
        activities
            list of activities corresponding to node labels
    Returns
    ------------
    G
        NetworkX DiGraph corresponding to dfg

    """

    if activities is None:
        activities = pm4py.objects.dfg.utils.dfg_utils.get_activities_from_dfg(dfg)

    G = nx.DiGraph()
    for act in activities:
        G.add_node(act)
    for el in dfg:
        act1 = el[0]
        act2 = el[1]
        G.add_edge(act1, act2)
    return G



def transform_xes_log_to_nxDiGraph(log, variant='dfg', integer_labels=False) -> nx.DiGraph:
    """
       Transform a given event log into a corresponding networkx DiGraph. At this time either a directly-follows graph
        using the dfg_disovery feature or a petri net using the inductive miner feature are used as graph representation
        of the log which then is transformed into a nx.DiGraph.

        Parameters
        --------------
        log
            Eventlog
        variant
            String: either 'dfg' or 'inductive' choosing the method for the base graph
        integer_labels
            Bool: whether to use integers as node labels or keep original labels

        Returns
        --------------
        G
            Networkx DiGraph corresponding to event log
        """
    if variant == 'dfg':
        dfg = dfg_discovery.apply(log)
        activities = pm4py.objects.dfg.utils.dfg_utils.get_activities_from_dfg(dfg)
        G = transform_dfg_to_directed_nx_graph(dfg, activities=activities)
        if integer_labels:
            return nx.convert_node_labels_to_integers(G, ordering="sorted")
        else:
            return G

    if variant == 'inductive':
        net, initial_marking, final_marking = inductive_miner.apply(log)
        G, inv_dict = pm4py.objects.petri_net.utils.networkx_graph.create_networkx_directed_graph(net)
        if integer_labels:
            return G
        else:
            return nx.relabel_nodes(G, inv_dict)

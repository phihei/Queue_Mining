from pm4py.streaming.stream.live_event_stream import LiveEventStream
from pm4py.objects.conversion.log import converter as stream_converter
from pm4py.streaming.algo.discovery.dfg import algorithm as dfg_discovery

import pm4py

from pm4py.algo.discovery.performance_spectrum import algorithm as performance_spectrum

live_event_stream = LiveEventStream()


streaming_dfg = dfg_discovery.apply()

live_event_stream.register(streaming_dfg)

live_event_stream.start()




def ServicePriorityDiscoveryStreaming(log, activities):
    """
   Finds the service priority (LIFO/FIFO/Random) in an online setting provided a log/dataframe
   and a list of activities

   Parameters
   -------------
   log
       Event log/Dataframe
   list_activities
       List of activities interested in the Service priority (at least one)
   variant
       Variant to be used (see Variants Enum)
   parameters
       Parameters of the algorithm, including:
           - Parameters.ACTIVITY_KEY
           - Parameters.TIMESTAMP_KEY

   Returns
   -------------
   Service priority order of streaming data
   """
    activities1=activities
    static_event_stream = stream_converter.apply(log, variant=stream_converter.Variants.TO_EVENT_STREAM)

    for ev in static_event_stream:
        live_event_stream.append(ev)

    live_event_stream.stop()


    if log is None:
        raise TypeError("A PM4PY Event Log is required.")
    if type(log) != pm4py.objects.log.obj.EventLog:
        raise TypeError("A PM4PY Event Log is required.")

    dfg, activities, start_activities, end_activities = streaming_dfg.get()
    # dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    activities = activities1
    df_activities = dfg.keys()

    if(len(activities)>1):
        for i in end_activities:
            if(i==activities[0]):
                raise TypeError("First activity can not be the end activity of the log")

        for i in start_activities:
            if(i==activities[1]):
                raise TypeError("Second activity can not be the first activity of the log")



    result = []
    if(len(activities)==1):

        for i in start_activities:
            if(i==activities[0]):
                raise TypeError("Single activity can not be the first activity of the log")



        # print("1")
        df_activities_list=[]

        # activity= "examine casually"
        for i,j in df_activities:
            # print(j,activities)
            if(j==activities[0]):
                df_activities_list.append(i)
                # print(df_activities_list)

        for i in  range(len(df_activities_list)):
            new_activity=[]
            new_activity.append(df_activities_list[i])
            new_activity.append(activities[0])
            # print(new_activity)
            Final_result=Performance_Analysis(log,new_activity)
            result.append(Final_result)

    else:
        Final_result=Performance_Analysis(log,activities)
        result.append(Final_result)


    return result





def Performance_Analysis(log, activities):


    perf_spectrum = performance_spectrum.apply(log,activities)
    Negative = 0
    Positive = 0
    for i in range(0, len(perf_spectrum['points']) - 1):
        value = perf_spectrum["points"][i + 1][1] - perf_spectrum["points"][i][1]
        # print(value)
        if (value > 0):
            Positive = Positive + 1
        else:
            Negative = Negative + 1

    # print(Negative)
    # print(Positive)
    result = []
    result.append(activities)
    # print(activities)
    if Negative == 0 and Positive > 0:
        # print("Fifo")
        result.append("Fifo")

    elif Negative > 0 and Positive == 0:
        # print("Lifo")
        result.append("Lifo")


    else:
        # print("Random")
        result.append("Random")

    return result








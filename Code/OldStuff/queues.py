"""
Analyze XES logs to extract queues for each activity
    for each activity get  case id, start timestamps, end timestamp, resource (optional)
    analyze for each activity if there are intersecting intervals, that means, whether more then one case is (to be) executed
    analyze end times of set of predecessors for each activity
    analyze time between end timestamp of activity n and following start timestamp for activity n+1, are the multiple cases in the same timeframe?




"""
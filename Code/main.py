#Code from Allesandros Demonstration
import pm4py
from intervaltree import IntervalTree, Interval

log = pm4py.read_xes("C:/running-example.xes")
tree = IntervalTree()
eps = 0.00001
for case in log:
    start_timestamp = case[0]["time:timestamp"].timestamp()
    end_timestamp = case[-1]["time:timestamp"].timestamp()
    print("st", start_timestamp, "et", end_timestamp)
    tree.add(Interval(start_timestamp-eps, end_timestamp+eps, data={"case_id": case.attributes["concept:name"]}))
print(tree[1294322520:1295174820])
print(tree[1294322520])

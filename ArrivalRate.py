#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy
import pandas
import queueing_tool
import pm4py
from tqdm import tqdm

from pm4py.objects.log.importer.xes import importer as xes_importer

#Read from file
variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('HospitalBillingEventLog.xes', variant=variant, parameters=parameters)




# In[7]:


#Queue Arrival rate
from pm4py.statistics.traces.log import case_arrival
case_arrival_ratio = case_arrival.get_case_arrival_avg(log, parameters={
    case_arrival.Parameters.TIMESTAMP_KEY: "time:timestamp"})


# In[4]:


print (case_arrival_ratio)


# In[14]:


from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
dfg = dfg_discovery.apply(log)

from pm4py.visualization.dfg import visualizer as dfg_visualization
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
dfg_visualization.view(gviz)


# In[20]:


import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)


# In[38]:


dataframe


# In[51]:


timestamp=pd.to_datetime(dataframe['time:timestamp'] , utc=True)
timestamp


# In[35]:


from pm4py.statistics.traces.pandas import case_statistics
variants_count = case_statistics.get_variant_statistics(dataframe,parameters={case_statistics.Parameters.TIMESTAMP_KEY: "time:timestamp"})


# In[36]:


variants_count


# In[27]:


from pm4py.objects.conversion.log import converter


# In[41]:


import pandas as pd
column = dataframe['time:timestamp']
column = pd.to_datetime(column,utc=True)


# In[42]:


column


# In[66]:


dataframe.groupby(timestamp).count().plot(kind="line")


# In[69]:


dataframe.groupby(timestamp).count().plot(kind="density")


# In[64]:


dataframe.groupby(timestamp.dt.month).count().plot(kind="hist")


# In[ ]:





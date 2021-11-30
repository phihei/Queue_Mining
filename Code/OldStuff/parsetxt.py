import ast
import os
import numpy as np
import pandas
import pandas as pd
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from callcenter_queues import clm_to_datetime, queue_analysis, qlp_predictor, customer_counter, qlmp_predictor, pts_predictor, kts_predictor, hol_predictor, les_predictor


directory = Path('/home/heisenB/PycharmProjects/Queue_Mining/logs/AnonymousBank')
# files = []
# for filename in os.listdir(directory):
#     if filename.endswith('.csv'):
#         files.append(filename)
#     else:
#         continue
#-- parse original data
# for filename in files:
#     data = pd.read_csv(directory/filename, delimiter='	')
#     data.to_csv(directory / (filename[:-4] + '.csv'), index=False)

# df = pd.DataFrame()

# for filename in files:
#     df = df.append(pd.read_csv(directory/filename))
# df = pd.read_csv(directory / "all1999_clean.csv",
#                                parse_dates=[["date", "vru_entry"], ["date", "vru_exit"], ["date", "q_start"],
#                                             ["date", "q_exit"], ["date", "ser_start"], ["date", "ser_exit"]]) #this is slow but gets the job done
#df = makeDateTime(df)

df = pd.read_csv(directory/"all1999_datetime_negative_q_.csv")
#queues_stats = pd.read_csv(directory/ "queues_stats_call_center_queues_only.csv")
#queues_stats.drop(index=df.index[0], axis=0, inplace=True)
df = clm_to_datetime(df)

df = df[df['date_vru_entry'] < dt.datetime(1999,3,31,23,59,59)]
df = df[df['priority'] == 2]
df = df.sort_values(by='date_vru_entry').reset_index(drop=True)
queues, stats = queue_analysis(df, 'hprio_result', True)
queue_values = customer_counter(df)

#multiprocessing?
sav = {}
pts = pts_predictor(df)
f = open('hprio_pts_results.pkl', 'wb')
pickle.dump(pts, f)
f.close()
kts = kts_predictor(df, stats)
h = open('hprio_kts_results.pkl', 'wb')
pickle.dump(kts, h)
h.close()
qlp = qlp_predictor(df, stats, queue_values)
j = open('hprio_qlp_results.pkl', 'wb')
pickle.dump(qlp, j)
j.close()
qlmp = qlmp_predictor(df, queue_values, queues)
k = open('hprio_qlmp_results.pkl', 'wb')
pickle.dump(qlmp, k)
k.close()
les = les_predictor(df)
m = open('hprio_les_results.pkl', 'wb')
pickle.dump(les, m)
m.close()
hol = hol_predictor(df, queues)
o = open('hprio_hol_results.pkl', 'wb')
pickle.dump(hol, o)
o.close()

#-- generate call_id_
# tmp = pd.DatetimeIndex(df['date_vru_entry']).month
# df['call_id_'] = tmp.astype(str) + df['vru+line'] + df['call_id'].astype(str)
#df = pd.read_csv(directory/"all1999_datetime_negative_q_.csv")
#df_tmp = df.loc[0:10]



# df = pd.read_csv(directory/ 'stats_df_call_center_queues_only.csv')
# df['time Points'] = pd.to_datetime(df['time Points'])
# training = df[df['time Points'] < dt.datetime(1999,3,31,23,59,59)]
# test = df[df['time Points'] > dt.datetime(1999,3,31,23,59,59)]
# print(training.info, test.info)
# x = training['number of Cases']
# x.plot.hist(bins=24, color='black', title='Frequency of Queued Cases Training Set', density=True, xticks=[ x for x in range(0,25)])
# plt.xlabel('Number in Queue')
# #plt.axvline(x=1, color='black')
# plt.axvline(x=5, color='grey')
# plt.tight_layout()
# plt.show()
#
# x = test['number of Cases']
# x.plot.hist(bins=24, color='black', title='Frequency of Queued Cases Test Set', density=True, xticks=[ x for x in range(0,25)])
# plt.xlabel('Number in Queue')
# #plt.axvline(x=1, color='black')
# plt.axvline(x=5, color='grey')
# plt.tight_layout()
# plt.show()


# df = pd.read_csv(directory/ 'stats_df_call_center.csv')
# df['time Points'] = pd.to_datetime(df['time Points'])
# df['case'] = 1
# print(df.columns)
# #df.drop(['number of Cases'], inplace=True)
# m = df.groupby(df['time Points'].dt.date).sum()
#
# m.plot.bar(xlabel='Time', y='case', title='Number of Customers per day Over Time', color='black', figsize=[10.0, 4.8])
# plt.xticks([ x for x in range(0,360, 30)], ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#        rotation=45)
# plt.axhline(y=1224, color='grey')
# plt.tight_layout()
# plt.show()
# print(max(m['case']), np.mean(m['case']), min(m['case']), np.std(m['case']))
# m.sort_values(by= 'case', ascending=False, inplace=True)
# m.plot.bar(xticks=[], xlabel='Timestamp', y='case', title='Number of Customers per Day - Descending', color= 'black', figsize=[10.0, 4.8])
# #plt.axhline(y=402)
# plt.axvline(x=113, color='black')
# #plt.axhline(y=1641)
# plt.axvline(x=300, color='black')
# plt.tight_layout()
# plt.show()

#
# X = test['number of Cases'].to_numpy().reshape(-1,1)
# for i in range(2, 8):
#     kmeans = KMeans(n_clusters=i).fit(X)
#     print('n clusters', i, 'centroids', kmeans.cluster_centers_)
#     print('silhouette score ', silhouette_score(X, kmeans.labels_))


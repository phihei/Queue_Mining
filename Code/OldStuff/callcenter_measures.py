import sklearn.metrics
import os
import pickle
import pandas as pd
from callcenter_queues import clm_to_datetime
from pathlib import Path
import datetime as dt
directory = Path('/home/heisenB/PycharmProjects/Queue_Mining/logs/AnonymousBank')
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse


# pts - list with one element
with open(directory/'hprio_pts_results.pkl', 'rb') as f:
    pts = pickle.load(f)
    f.close()

# kts - list with two elements
with open(directory / 'hprio_kts_results.pkl', 'rb') as h:
    kts = pickle.load(h)
    h.close()

# qlp - dict with ofer 400k keys
with open(directory / 'hprio_qlp_results.pkl', 'rb') as j:
    qlp = pickle.load(j)
    j.close()

# qlmp - dict with ofer 400k keys
with open(directory / 'hprio_qlmp_results.pkl', 'rb') as k:
    qlmp = pickle.load(k)
    k.close()

# les - list with 400k elements
with open(directory / 'hprio_les_results.pkl', 'rb') as m:
    les = pickle.load(m)
    m.close()

# hol - dict with ofer 400k keys
with open(directory / 'hprio_hol_results.pkl', 'rb') as o:
    hol = pickle.load(o)
    o.close()

df = pd.read_csv(directory/"all1999_datetime_negative_q_.csv")
df = clm_to_datetime(df)

df = df[df['date_vru_entry'] < dt.datetime(1999,3,31,23,59,59)]
df = df[df['priority'] == 2]
df = df.sort_values(by='date_vru_entry').reset_index(drop=True)
stats_df = pd.read_csv(directory/ "stats_df_call_hprio_result.csv")
stats_df['time Points'] = pd.to_datetime(stats_df['time Points'])
stats_df = stats_df.sort_values(by='time Points').reset_index(drop=True)
df['number of Cases'] = stats_df['number of Cases']
df_ids = df.sort_values(by='call_id_').reset_index(drop=True)
x = list(df_ids['q_time'])



def measures():
  print('pts')
  y_pts = [pts[0] for i in range(0, len(x))]
  pts_bias = mae(x, y_pts)
  pts_mse = mse(x, y_pts)
  print(pts_bias, pts_mse, 'Sample size', len(x))

  print('kts')
  st_queued_norm = {}
  st_queued_high = {}
  for index, row in df.iterrows():
    st_queued_norm[row['call_id_']] = row['q_time'] if str(row['date_q_exit'])[-8:] != '00:00:00' and row['number of Cases'] <= 5 else -1
    st_queued_high[row['call_id_']] = row['q_time'] if str(row['date_q_exit'])[-8:] != '00:00:00' and row['number of Cases'] > 5 else -1

  st_queued_norm_clean = {key: val for key, val in st_queued_norm.items() if val > -1}
  st_queued_high_clean = {key: val for key, val in st_queued_high.items() if val > -1}
  kts_bias_norm = mae(list(st_queued_norm_clean.values()), [kts[0] for i in range(0, len(st_queued_norm_clean))])
  kts_bias_high = mae(list(st_queued_high_clean.values()), [kts[1] for i in range(0, len(st_queued_high_clean))])
  kts_sq_norm = mse(list(st_queued_norm_clean.values()), [kts[0] for i in range(0, len(st_queued_norm_clean))])
  kts_sq_high = mse(list(st_queued_high_clean.values()), [kts[1] for i in range(0, len(st_queued_high_clean))])
  print(kts_bias_norm, kts_bias_high)
  print(kts_sq_norm, kts_sq_high, 'Sample size', len(st_queued_norm_clean), len(st_queued_high_clean))

  print('qlp')
  qlp_ = [[key, value] for key, value in qlp.items()]
  qlp_df = pd.DataFrame(qlp_, columns=['call_id_', 'q_pred'])
  qlp_df.sort_values(by='call_id_').reset_index(drop=True)
  qlp_sorted = qlp_df.values.tolist()
  df_sorted_list = df[['call_id_', 'q_time']].values.tolist()
  y_qlp = [y for [x,y] in qlp_sorted]
  x_qlp = [y for [x, y] in df_sorted_list]
  qlp_mae = mae(x_qlp, y_qlp)
  qlp_mse = mse(x_qlp, y_qlp)
  print(qlp_mae, qlp_mse, 'Sample size', len(qlp))

  print('qlmp')
  qlmp__ = {k: v for k, v in qlmp.items() if v is not None}
  qlmp_keys = list(qlmp__.keys())

  qlmp_ = [[key, value] for key, value in qlmp__.items()]
  qlmp_df = pd.DataFrame(qlmp_, columns=['call_id_', 'q_pred'])
  qlmp_df.sort_values(by='call_id_').reset_index(drop=True)
  qlmp_sorted = qlmp_df.values.tolist()

  df_qlmp_only = df[df['call_id_'].isin(qlmp_keys)]
  df_qlmp_only.sort_values(by='call_id_').reset_index(drop=True)
  df_sorted_qlmp = df_qlmp_only[['call_id_', 'q_time']].values.tolist()

  y_qlmp = [y for [x, y] in qlmp_sorted]
  x_qlmp = [y for [x, y] in df_sorted_qlmp]

  qlmp_mae = mae(x_qlmp, y_qlmp)
  qlmp_mse = mse(x_qlmp, y_qlmp)
  print(qlmp_mae, qlmp_mse, 'Sample size', len(qlmp__))

  print('les')
  les_bias = mae(list(df['q_time']), les)
  les_mse = mse(list(df['q_time']), les)
  print(les_bias, les_mse, 'Sample size', len(les))

  print('hol')
  hol__ = {k: v for k, v in hol.items() if v is not None}
  hol_keys = list(hol__.keys())
  hol_ = [[key, value] for key, value in hol__.items()]
  hol_df = pd.DataFrame(hol_, columns=['call_id_', 'q_pred'])
  hol_df.sort_values(by='call_id_').reset_index(drop=True)
  hol_sorted = hol_df.values.tolist()


  df_hol_only = df[df['call_id_'].isin(hol_keys)]
  df_hol_only.sort_values(by='call_id_').reset_index(drop=True)
  df_sorted_hol = df_hol_only[['call_id_', 'q_time']].values.tolist()

  y_hol = [y for [x, y] in hol_sorted]
  x_hol = [y for [x, y] in df_sorted_hol]

  hol_mae = mae(x_hol, y_hol)
  hol_mse = mse(x_hol, y_hol)
  print(hol_mae, hol_mse, 'Sample size', len(hol__))



measures()
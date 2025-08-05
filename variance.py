import pandas as pd
import numpy as np

mode = 'cv'

data_peaks = pd.read_csv('peaks_main.csv')
data_area = pd.read_csv('area_main.csv')

results_peaks = {}
results_area = {}

target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453, 1410, 1370, 1342, 1240, 1176, 1124, 1096, 1050, 1016, 972, 929, 872, 848, 792, 771]

data_peaks = data_peaks.drop(data_peaks.columns[0], axis = 1)
data_area = data_area.drop(data_area.columns[0], axis = 1)

if mode == 'stand_dev':

    for i, row in data_peaks.iterrows():
        stand_dev = row.std()
        if np.isnan(stand_dev):
            results_peaks[target[i]] = 'None'
        else:
            stand_dev = int(stand_dev)
            results_peaks[target[i]] = stand_dev

    for i, row in data_area.iterrows():
        stand_dev = row.std()
        if np.isnan(stand_dev):
            results_area[target[i]] = 'None'
        else:
            stand_dev = int(stand_dev)
            results_area[target[i]] = stand_dev

if mode == 'cv':

    for i, row in data_peaks.iterrows():
        stand_dev = row.std()
        if np.isnan(stand_dev):
            results_peaks[target[i]] = 'None'
        else:
            mean_1 = np.mean(row)
            cv = round(stand_dev/mean_1, 2)
            results_peaks[target[i]] = cv

    for i, row in data_area.iterrows():
        stand_dev = row.std()
        if np.isnan(stand_dev):
            results_area[target[i]] = 'None'
        else:
            mean_1 = np.mean(row)
            cv = round(stand_dev/mean_1, 2)
            results_area[target[i]] = cv

res_peaks = pd.DataFrame(results_peaks, index = ['Peaks']).T
res_area = pd.DataFrame(results_area, index = ['Area']).T

res_united = pd.concat([res_peaks, res_area], axis=1)

res_united.to_csv(f'united_{mode}.txt', index = True)

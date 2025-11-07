import pandas as pd
import json
import numpy as np
import peaks_finder_3
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore", category=RuntimeWarning)

# target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453, 1410, 1370, 1342, 1240, 1176, 1096, 1050, 1016, 972, 872, 848, 792]

def peaks_and_square(target=None, savgol_window=21, delta=20, baseline_square='horizontal_full'):

    data = None

    with open('data/spectra_dict.json', 'r', encoding = 'utf-8') as f:
        data = json.load(f)

    peaks = {}
    area = {}

    for culture, data_1 in tqdm(data.items(), desc = 'Обработка культур'):

        for type_name, data_2 in data_1.items():

            if type_name == 'Control':

                con_area_df_rows = []
                con_peaks_df_rows = []

                for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                    waves = data_3['wavelength']
                    absorption = data_3['absorption']

                    results = peaks_finder_3.peaks_finder_3(waves, absorption, targets=target, delta=delta, ax=None, 
                                                            plot=False, square=False, savgol_window=savgol_window, 
                                                            baseline_square=baseline_square)

                    area_row = {'Sample': sample}

                    for t in target:
                        if t in results['target']:
                            idx = results['target'].index(t)
                            val = results['area'][idx]
                            area_row[f'{t}'] = None if np.isnan(val) else val
                        else:
                            area_row[f'{t}'] = None

                    con_area_df_rows.append(area_row)

                    peaks_row = {'Sample': sample}

                    for t in target:
                        if t in results['target']:
                            idx = results['target'].index(t)
                            val = results['height'][idx]
                            peaks_row[f'{t}'] = None if np.isnan(val) else val
                        else:
                            peaks_row[f'{t}'] = None

                    con_peaks_df_rows.append(peaks_row)

                con_area_df = pd.DataFrame(con_area_df_rows)
                con_peaks_df = pd.DataFrame(con_peaks_df_rows)

            elif type_name == 'Experiment':

                exp_area_df_rows = []
                exp_peaks_df_rows = []

                for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                    waves = data_3['wavelength']
                    absorption = data_3['absorption']

                    results = peaks_finder_3.peaks_finder_3(waves, absorption, targets=target, delta=delta, ax=None, 
                                                            plot=False, square=False, savgol_window=savgol_window, 
                                                            baseline_square=baseline_square)

                    area_row = {'Sample': sample}

                    for t in target:
                        if t in results['target']:
                            idx = results['target'].index(t)
                            val = results['area'][idx]
                            area_row[f'{t}'] = None if np.isnan(val) else val
                        else:
                            area_row[f'{t}'] = None

                    exp_area_df_rows.append(area_row)

                    peaks_row = {'Sample': sample}

                    for t in target:
                        if t in results['target']:
                            idx = results['target'].index(t)
                            val = results['height'][idx]
                            peaks_row[f'{t}'] = None if np.isnan(val) else val
                        else:
                            peaks_row[f'{t}'] = None

                    exp_peaks_df_rows.append(peaks_row)

                exp_area_df = pd.DataFrame(exp_area_df_rows)
                exp_peaks_df = pd.DataFrame(exp_peaks_df_rows)

                area_full = pd.concat([con_area_df, exp_area_df], ignore_index=True)
                peaks_full = pd.concat([con_peaks_df, exp_peaks_df], ignore_index=True)

                area_full = area_full.set_index('Sample').T
                peaks_full = peaks_full.set_index('Sample').T

                area_full = area_full.drop(area_full.columns[0], axis=1)
                peaks_full = peaks_full.drop(peaks_full.columns[0], axis=1)

                res_peaks = []
                res_area = []

                for i, row in area_full.iterrows():
                    mean_1 = row.mean()
                    if np.isnan(mean_1):
                        res_area.append(None)
                    else:
                        # mean_1 = int(mean_1)
                        res_area.append(mean_1)

                for i, row in peaks_full.iterrows():
                    mean_1 = row.mean()
                    if np.isnan(mean_1):
                        res_peaks.append(None)
                    else:
                        # mean_1 = int(mean_1)
                        res_peaks.append(mean_1)

                area[culture] = res_area
                peaks[culture] = res_peaks

    area = pd.DataFrame(area)
    peaks = pd.DataFrame(peaks)

    area.to_csv('data/area_values.txt', index=False)
    peaks.to_csv('data/peaks_values.txt', index=False)

if __name__ == '__main__':

    peaks_and_square(target=None, savgol_window=21, 
                     delta=20, baseline_square='horizontal_full')
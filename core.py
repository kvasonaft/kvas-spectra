import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import logging
from peaks_finder import peaks_finder

logging.basicConfig(filename = 'log.txt', level = logging.INFO)

target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504,1470,  1453, 1410, 1370, 1342, 1240, 1176, 1124, 1096, 1050, 1016, 972, 929, 872, 848, 792, 771]
data = None

with open('spectra_dict.json', 'r', encoding = 'utf-8') as f:
    try:
        data = json.load(f)
        logging.info(f'Файл JSON был успешно загружен.')
    except Exception as e:
        logging.error(f'Ошибка при загрузке файла JSON: {e}')

if data is None:
    raise ValueError(f'Ошибка при загрузке файла JSON.')

for culture, data_1 in data.items():

    for type, data_2 in data_1.items():

        if type == 'Control':

            con_dict = {'wavelength': []}
            con_area_df_rows = []
            con_peaks_df_rows = []

            for sample, data_3 in data_2.items():

                waves = data[culture][type][sample]['wavelength']
                absorption = data[culture][type][sample]['absorption']

                results = peaks_finder(waves, absorption, target, 25, 0.7)

                area_row = {'Sample': sample}
                for t, a in zip(results['target'], results['area']):
                    area_row[f'{t}'] = a
                con_area_df_rows.append(area_row)

                peaks_row = {'Sample': sample}
                for t, a in zip(results['target'], results['height']):
                    peaks_row[f'{t}'] = a
                con_peaks_df_rows.append(peaks_row)

            con_area_df = pd.DataFrame(con_area_df_rows)
            con_peaks_df = pd.DataFrame(con_peaks_df_rows)

        elif type == 'Experiment':

            exp_dict = {'wavelength': []}
            exp_area_df_rows = []
            exp_peaks_df_rows = []

            for sample, data_3 in data_2.items():

                waves = data[culture][type][sample]['wavelength']
                absorption = data[culture][type][sample]['absorption']

                results = peaks_finder(waves, absorption, target, 25, 0.7)

                area_row = {'Sample': sample}
                for t, a in zip(results['target'], results['area']):
                    area_row[f'{t}'] = a
                exp_area_df_rows.append(area_row)

                peaks_row = {'Sample': sample}
                for t, a in zip(results['target'], results['height']):
                    peaks_row[f'{t}'] = a
                exp_peaks_df_rows.append(peaks_row)

            exp_area_df = pd.DataFrame(exp_area_df_rows)
            exp_peaks_df = pd.DataFrame(exp_peaks_df_rows)

            area_full = pd.concat([con_area_df, exp_area_df], ignore_index=True)
            peaks_full = pd.concat([con_peaks_df, exp_peaks_df], ignore_index=True)

            area_full = area_full.set_index('Sample').T
            peaks_full = peaks_full.set_index('Sample').set.T

            print(area_full)
            print(peaks_full)

    break


import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import logging
from peaks_finder import peaks_finder
from matplotlib.lines import Line2D

logging.basicConfig(filename = 'log.txt', level = logging.INFO)

target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453, 1410, 1370, 1342, 1240, 1176, 1124, 1096, 1050, 1016, 972, 929, 872, 848, 792, 771]
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

    fig, ax = plt.subplots(figsize = (20, 10))

    for type, data_2 in data_1.items():

        items_data_2 = list(data_2.items())
        half_data_2 = len(items_data_2) // 2

        if type not in ['Control', 'Experiment']:
            continue

        if type == 'Control':

            con_dict = {'wavelength': []}
            con_area_df_rows = []
            con_peaks_df_rows = []

            for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                waves = data[culture][type][sample]['wavelength']
                absorption = data[culture][type][sample]['absorption']

                results = peaks_finder(waves, absorption, target, delta = 25, integration = 0.7, ax = ax, color = 'orange')

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

            for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                waves = data[culture][type][sample]['wavelength']
                absorption = data[culture][type][sample]['absorption']

                results = peaks_finder(waves, absorption, target, delta = 25, integration = 0.7, ax = ax, color = 'black')

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
            peaks_full = peaks_full.set_index('Sample').T

            print(area_full)
            print(peaks_full)

            dif_area =[]
            dif_peaks = []

            for row_name, row in area_full.iterrows():

                dif_list = []

                for col1 in [col for col in area_full.columns if len(col) == 8]:
                    for col2 in [col for col in area_full.columns if len(col) == 8]:

                        if np.isnan(row[col1]) or np.isnan(row[col2]):
                            dif_list.append(np.nan)
                        else:
                            dif = round(abs(row[col1] - row[col2]), 2)
                            dif_list.append(dif)

                dif_array = np.array(dif_list)
                mean_dif = np.nanmean(dif_array)
                dif_area.append(mean_dif)


            dif_area = pd.Series(dif_area)
            print(dif_area)

    for t in target:
        ax.text(t, ax.get_ylim()[0] + 2, str(t), fontsize = 10, rotation = 90, ha = 'center', va = 'bottom')

    custom_lines = [
        Line2D([0], [0], color = 'black', lw = 2),
        Line2D([0], [0], color = 'orange', lw = 2)
    ]

    ax.legend(custom_lines, ['Контроль', 'Эксперимент'], loc = 'lower right', fontsize = 14, frameon = False)
    ax.set_xlabel('Длина волны, нм', fontsize = 14)
    ax.set_ylabel('Пропускание, %', fontsize = 14)
    ax.set_title(f'Сравнительная ИК-спектрограмма культуры {culture}', fontsize = 16)

    plt.tight_layout()
    # plt.savefig(f'{culture}.png', dpi = 300, bbox_inches = 'tight')
    plt.close()

    break


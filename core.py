import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import logging
import peaks_finder_2
from matplotlib.lines import Line2D
import warnings
from tqdm import tqdm
import time

warnings.filterwarnings("ignore", category=RuntimeWarning)

logging.basicConfig(filename = 'log.txt', filemode = 'w', format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)

target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453, 1410, 1370, 1342, 1240, 1176, 1124, 1096, 1050, 1016, 972, 929, 872, 848, 792, 771]

data = None

start_time = time.time()
logging.info('Программа запущена.')

with open('spectra_dict.json', 'r', encoding = 'utf-8') as f:
    try:
        data = json.load(f)
        logging.info(f'Файл JSON был успешно загружен.')
    except Exception as e:
        logging.error(f'Ошибка при загрузке файла JSON: {e}')

if data is None:
    raise ValueError(f'Ошибка при загрузке файла JSON.')

area_main = {'Wavelength': target}
peaks_main = {'Wavelength': target}
area_indicator = {}
peaks_indicator = {}

logging.info('Запуск главного цикла обработки данных...')

for culture, data_1 in tqdm(data.items(), desc = 'Обработка культур'):

    logging.info(f'Обработка культуры {culture}')

    fig, ax = plt.subplots(figsize = (20, 10))

    for type, data_2 in data_1.items():

        try:

            if type not in ['Control', 'Experiment']:
                logging.warning(f'Обнаружен образец без контрольной или экспериментальной метки в культуре {culture}')
                continue

            if type == 'Control':

                con_area_df_rows = []
                con_peaks_df_rows = []

                for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                    waves = data[culture][type][sample]['wavelength']
                    absorption = data[culture][type][sample]['absorption']

                    results = peaks_finder_2.peaks_finder_2(waves, absorption, target, ax, color = 'orange', square = True)

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

                exp_area_df_rows = []
                exp_peaks_df_rows = []

                for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                    waves = data[culture][type][sample]['wavelength']
                    absorption = data[culture][type][sample]['absorption']

                    results = peaks_finder_2.peaks_finder_2(waves, absorption, target, ax, color = 'black', square=True)

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

                dif_area = []
                dif_peaks = []

                for row_name, row in area_full.iterrows():

                    dif_list_a = []

                    for col1 in [col for col in area_full.columns if len(col) == 8]:
                        for col2 in [col for col in area_full.columns if len(col) > 8]:

                            if np.isnan(row[col1]) or np.isnan(row[col2]):
                                dif_list_a.append(np.nan)
                            else:
                                dif_a = round(abs(row[col1] - row[col2]), 2)
                                dif_list_a.append(dif_a)

                    dif_array_a = np.array(dif_list_a)
                    mean_dif_a = np.nanmean(dif_array_a)
                    dif_area.append(round(mean_dif_a, 2))

                for row_name, row in peaks_full.iterrows():

                    dif_list_p = []

                    for col1 in [col for col in peaks_full.columns if len(col) == 8]:
                        for col2 in [col for col in peaks_full.columns if len(col) > 8]:

                            if np.isnan(row[col1]) or np.isnan(row[col2]):
                                dif_list_p.append(np.nan)
                            else:
                                dif_p = round(abs(row[col1] - row[col2]), 2)
                                dif_list_p.append(dif_p)

                    dif_array_p = np.array(dif_list_p)
                    mean_dif_p = np.nanmean(dif_array_p)
                    dif_peaks.append(round(mean_dif_p, 2))

                indicator_peaks = int(round(np.nanmean(np.array(dif_peaks)), 0))
                indicator_area = int(round(np.nanmean(np.array(dif_area)), 0))

                dif_peaks = pd.Series(dif_peaks)
                dif_area = pd.Series(dif_area)

                peaks_main[f'{culture}({indicator_peaks})'] = dif_peaks
                area_main[f'{culture}({indicator_peaks})'] = dif_area

                peaks_indicator[f'{culture}({indicator_peaks})'] = indicator_peaks
                area_indicator[f'{culture}({indicator_area})'] = indicator_area

        except Exception as e:
            logging.info(f'Возникла ошибка при работе главного цикла обработки данных: {e}')

    logging.info('Работа главного цикла завершена успешно.')

    for t in target:
        ax.text(t, ax.get_ylim()[0] + 2, str(t), fontsize = 10, rotation = 90, ha = 'center', va = 'bottom')

    custom_lines = [
        Line2D([0], [0], color = 'black', lw = 2),
        Line2D([0], [0], color = 'orange', lw = 2)
    ]

    logging.info('Построение графиков и сохранение таблиц...')

    ax.legend(custom_lines, ['Контроль', 'Эксперимент'], loc = 'lower right', fontsize = 14, frameon = False)
    ax.set_xlabel('Длина волны, нм', fontsize = 16)
    ax.set_ylabel('Пропускание, %', fontsize = 16)
    ax.set_title(f'Сравнительная ИК-спектрограмма культуры {culture}', fontsize = 18)

    plt.tight_layout()
    plt.savefig(f'/home/kvasonaft/Development/graphs/{culture}.png', dpi = 300, bbox_inches = 'tight')
    plt.close()

try:

    peaks_main = pd.DataFrame(peaks_main)
    area_main = pd.DataFrame(area_main)

    peaks_indicator = pd.DataFrame.from_dict(peaks_indicator, orient='index', columns=['Indicator'])
    area_indicator = pd.DataFrame.from_dict(area_indicator, orient='index', columns=['Indicator'])

    peaks_main.to_csv('peaks_main.csv', index=False)
    area_main.to_csv('area_main.csv', index=False)
    peaks_indicator.to_csv('peaks_indicator.csv')
    area_indicator.to_csv('area_indicator.csv')

    logging.info('Все данные успешно сохранены.')

except Exception as e:
    logging.info(f'При сохранении данных произошла ошибка: {e}')

end_time = time.time()
elapsed_time = end_time - start_time

logging.info(f'Работа программы завершена успешно. Время выполнения: {elapsed_time:.2f} с.')

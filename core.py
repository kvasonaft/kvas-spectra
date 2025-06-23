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

for sample_name, sample_data in data.items():

    dictionary = {}

    experiment_data = sample_data.get('Experiment', {})
    control_data = sample_data.get('Control', {})

    for filename, spectrum in experiment_data.items():
        wavelengths = spectrum['wavelength']
        dictionary['wavelength'] = wavelengths
        break

    for filename, spectrum in experiment_data.items():
        absorptions_exp = spectrum['absorption']
        dictionary[filename] = absorptions_exp

    for filename, spectrum in control_data.items():
        absorptions_con = spectrum['absorption']
        dictionary[filename] = absorptions_con

    spectra_df = pd.DataFrame(dictionary)
    wave = np.array(spectra_df['wavelength'])

    result_dict = {}
    results = None

    for col in spectra_df.columns:

        res_dict = {}
        pre_dict = {'waves': [], 'peaks': [], 'areas': []}

        if col == 'wavelength':
            continue
        spec = np.array(spectra_df[col].values)
        results = peaks_finder(wave, spec, target, 25, 0.7, True)

        pre_dict['waves'].append(results['target'])
        pre_dict['peaks'].append(results['height'])
        pre_dict['areas'].append(results['area'])

        result_dict[col] = pre_dict
        break
    break
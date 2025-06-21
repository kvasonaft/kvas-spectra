import pandas as pd
import os
import json
from tqdm import tqdm

names = pd.read_excel('/home/kvasonaft/Development/spectra/metadata.xlsx')

path = '/home/kvasonaft/Development/spectra/dataset'

data = {}

for _, row in tqdm(names.iterrows(), desc = 'Общий прогресс'):

    try:

        sample_name = str(row['New name'])
        folder_path = os.path.join(path, sample_name)

        spectra = {'Experiment': {}, 'Control': {}}

        metadata = {'Taxonomy': [], 'Exposure time': [], 'Organism': [], 'Plastic type': [], 'Origin': []}

        for file_name in tqdm(sorted(os.listdir(folder_path)), desc = 'Запись файлов'):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)

                try:
                    df = pd.read_csv(file_path, sep = '\t', header = None)
                    values = [df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()]

                    if len(file_name) > 8:
                        spectra['Experiment'][file_name] = values
                    else:
                        spectra['Control'][file_name] = values

                except Exception as e:
                    print(f"Ошибка при чтении {file_path}: {e}")

        metadata['Taxonomy'] = row['Taxonomy']
        metadata['Exposure time'] = row['Exposure time']
        metadata['Organism'] = row['Bacteria / Fungi / Plank']
        metadata['Plastic type'] = row['Plastic type']
        metadata['Origin'] = row['Origin']

        data[sample_name] = {'Spectra' : spectra, 'Metadata': metadata}

    except Exception as e:
        print(f'Возникла проблема с чтением папки {row['New name']}')

with open('dataset.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, ensure_ascii = False, indent = 4)
import pandas as pd
import os
import sqlite3
from tqdm import tqdm

names = pd.read_excel('/home/kvasonaft/Development/spectra/metadata.xlsx')
path = '/home/kvasonaft/Development/spectra/dataset'

conn = sqlite3.connect('spectra.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE   
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS metadata (
    sample_id INTEGER,
    taxonomy TEXT,
    exposure_time INTEGER,
    organism TEXT,
    plastic_type TEXT,
    origin TEXT,
    FOREIGN KEY (sample_id) REFERENCES samples(id)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS spectra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER,
    filename TEXT,
    type TEXT CHECK(type IN ('Experiment', 'Control')),
    FOREIGN KEY (sample_id) REFERENCES samples(id)
)            
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS spectrum_values (
    spectrum_id INTEGER,
    point_index INTEGER,
    wavelength REAL,
    absorption REAL,
    FOREIGN KEY (spectrum_id) REFERENCES spectra(id)
)
''')

for _, row in tqdm(names.iterrows(), desc = 'Общий прогресс'):
    try:
        sample_name = str(row['New name'])
        folder_path = os.path.join(path, sample_name)

        cur.execute('INSERT OR IGNORE INTO samples (name) VALUES (?)', (sample_name,))
        conn.commit()

        cur.execute('SELECT id FROM samples WHERE name = ?', (sample_name,))
        sample_id = cur.fetchone()[0]

        cur.execute('''
        INSERT INTO metadata (sample_id, taxonomy, exposure_time, organism, plastic_type, origin) VALUES (?, ?, ?, ?, ?, ?)''', (
            sample_id,
            row['Taxonomy'],
            row['Exposure time'],
            row['Bacteria / Fungi / Plank'],
            row['Plastic type'],
            row['Origin']
        ))
        conn.commit()

        for file_name in tqdm(sorted(os.listdir(folder_path)), desc = 'Запись файлов'):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)

                try:
                    df = pd.read_csv(file_path, sep = '\t', header = None)
                    values = df.values.tolist()

                    spec_type = 'Experiment' if len(file_name) > 8 else 'Control'

                    cur.execute('''
                    INSERT INTO spectra (sample_id, filename, type) VALUES (?, ?, ?)''', (sample_id, file_name, spec_type))
                    spectrum_id = cur.lastrowid

                    for idx, (x, y) in enumerate(values):
                        cur.execute('''
                        INSERT INTO spectrum_values (spectrum_id, point_index, wavelength, absorption) VALUES (?, ?, ?, ?)
                        ''', (spectrum_id, idx, x, y))
                    conn.commit()

                except Exception as e:
                    print(f'Ошибка при чтении {file_path}: {e}')
    
    except Exception as e:
        print(f"Ошибка при обработке образца {row['New name']}: {e}")

conn.close()
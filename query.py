import sqlite3
import json
from collections import defaultdict

def query(path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/spectra.db'):

    '''
    
    Функция делает запрос к базе данных, формирует словарь следующей структуры: sample → Control/Experiment → filename → {"wavelength": [...], "absorption": [...]}

    Аргументы:
        path (str): путь к базе данных SQLite3.

    '''

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    query = """
    SELECT 
        sa.name AS sample_name,
        s.type AS spectrum_type,
        s.filename,
        sv.wavelength,
        sv.absorption
    FROM spectrum_values sv
    JOIN spectra s ON sv.spectrum_id = s.id
    JOIN samples sa ON s.sample_id = sa.id
    ORDER BY sample_name, spectrum_type, s.filename, sv.point_index
    """

    cursor.execute(query)

    data = defaultdict(lambda: {"Control": {}, "Experiment": {}})

    for sample, spec_type, filename, x, y in cursor.fetchall():
        sample_dict = data[sample][spec_type]
        if filename not in sample_dict:
            sample_dict[filename] = {"wavelength": [], "absorption": []}
        sample_dict[filename]["wavelength"].append(x)
        sample_dict[filename]["absorption"].append(y)

    conn.close()

    with open("data/spectra_dict.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    query()
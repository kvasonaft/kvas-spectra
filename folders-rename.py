import os
import pandas as pd

#column_old = input('Введите название столбца со старыми именами:')
#column_new = input('Введите название столбца с новыми именами:')
#base_dir = input('Введите путь к папке с набором папок для переименования:')
#names_table = input('Введите путь к таблице с именами:')

base_dir = '/home/kvasonaft/Development/dataset-code'
names_table = '/home/kvasonaft/Development/folders_names.csv'

df = pd.read_csv(names_table, sep = ';')

for _, row in df.iterrows():
    old_path = os.path.join(base_dir, row['old_name'])
    new_path = os.path.join(base_dir, str(row['code_name']))

    try:
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f'Папка {row['old_name']} переименована в {row['code_name']}')
        else:
            print(f'Папка {row['old_name']} не найдена')
    except Exception as e:
        print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')
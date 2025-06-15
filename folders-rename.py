import os
import pandas as pd

mode = 1

if mode == 1:

    first_path = 'path'
    names_table = 'path'
    df = pd.read_csv(names_table, sep = ';')

    for _, row in df.iterrows():
        old_path = os.path.join(first_path, row['control_name'])
        new_path = os.path.join(first_path, str(row['code_name']))

        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f'Папка {row['control_name']} переименована в {row['code_name']}')
            else:
                print(f'Папка {row['control_name']} не найдена')
        except Exception as e:
            print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')

elif mode == 2:

    second_path = 'path'

    for folder in os.listdir(second_path):
        folder_path = os.path.join(second_path, folder)
        if not os.path.isdir(folder_path):
            continue

        #files = [file for file in sorted(os.listdir(folder_path)) if os.path.isfile(os.path.join(folder_path, file)) and len(file) > 8]

        files = os.path.listdir(folder_path)

        for number, file in enumerate(files, start = 1):

            old_path = os.path.join(folder_path, file)

            if not os.path.isfile(old_path):
                continue

            new_name = f'{folder}_{number:02d}.txt'
            new_path = os.path.join(folder_path, new_name)
            try:
                os.rename(old_path, new_path)
                print(f'Файл {file} переименован в {new_name}')
            except Exception as e:
                print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')
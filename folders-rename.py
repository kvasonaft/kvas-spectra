import os
import pandas as pd

base_dir = '/home/kvasonaft/Development/dataset-code'
names_table = '/home/kvasonaft/Development/kvas-spectra/folders_names.csv'

df = pd.read_csv(names_table, sep = ';')

mode = 4

if mode == 1:

    for _, row in df.iterrows():
        old_path = os.path.join(base_dir, row['old_name'])
        new_path = os.path.join(base_dir, str(row['new_name']))

        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f'Папка {row['old_name']} переименована в {row['new_name']}')
            else:
                print(f'Папка {row['old_name']} не найдена')
        except Exception as e:
            print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')

elif mode == 2:

    for _, row in df.iterrows():
        old_path = os.path.join(base_dir, str(row['code_name']))
        new_path = os.path.join(base_dir, row['code_name'])

        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f'Папка {row['old_name']} переименована в {row['code_name']}')
            else:
                print(f'Папка {row['old_name']} не найдена')
        except Exception as e:
            print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')

elif mode == 3:

    control_path = '/home/kvasonaft/Development/spectra/controls'

    for folder in os.listdir(control_path):
        folder_path = os.path.join(control_path, folder)
        if not os.path.isdir(folder_path):
            continue

        files = os.listdir(folder_path)
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

elif mode == 4:

    main_path = '/home/kvasonaft/Development/spectra/dataset-code'

    for folder in os.listdir(main_path):
        folder_path = os.path.join(main_path, folder)
        if not os.path.isdir(folder_path):
            continue

        files = os.listdir(folder_path)
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
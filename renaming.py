import os
import pandas as pd

def folders_rename(old, new, folder_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/dataset', table_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/names.csv', separator = ';'):

    '''
    
    Функция переименовывает все объекты внутри указанной папки в соответствии с таблицей старых и новых имён.

    В качестве аргументов функции указываются названия старых и новых объектов в папке, она находит в главной папке объекты, имена которых соответствуют значениям столбца старых имён (old) и переименовывает их в значения столбца новых имён (new).

    Аргументы:
        old (str): название столбца со старыми именами объектов.
        new (str): название столбца с новыми именами объектов.
        folder_path (str): путь к папке с объектами для переименования.
        table_path (str): путь к таблице со столбцами новых и старых значений.
        separator (str): разделитель элементов для таблицы с именами.

    '''

    df = pd.read_csv(table_path, sep = separator)

    old = str(old)
    new = str(new)

    for _, row in df.iterrows():
        old_path = os.path.join(folder_path, row[old])
        new_path = os.path.join(folder_path, str(row[new]))

        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f'Папка {row[old]} переименована в {row[new]}')
            else:
                print(f'Папка {row[old]} не найдена')
        except Exception as e:
            print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')


def files_rename(mode = 'all', path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/dataset', format = 'txt'):

    '''
    
    Функция переименовывает файлы во вложенных папках следующим образом: "имя_папки_01.txt"

    Функция принимает значение пути к "главной папке", после чего для всех вложенных папок переименовывает их файлы, оставляя название папки, в которой они лежат и добавляя номер 01, 02 и т.д., а также выбранное расширение. Есть два режима работы, которые определяются аргументом mode. В режиме "all" переименовываются все файлы, в режиме "experiments" - только файлы, длина имён которых составляет более 8 символов.

    Аргументы:
        mode (str): режим работы (принимает только два значения - 'all' и 'experiments').
        path (str): путь к папке с вложенными папками и файлами для переименования.
        format (str): расширение файлов.

    '''

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if not os.path.isdir(folder_path):
            continue
        
        if mode == 'experiments':
            files = [file for file in sorted(os.listdir(folder_path)) if os.path.isfile(os.path.join(folder_path, file)) and len(file) > 8]
        elif mode == 'all':
            files = os.path.listdir(folder_path)

        for number, file in enumerate(files, start = 1):

            old_path = os.path.join(folder_path, file)

            if not os.path.isfile(old_path):
                continue

            new_name = f'{folder}_{number:02d}.{format}'
            new_path = os.path.join(folder_path, new_name)
            try:
                os.rename(old_path, new_path)
                print(f'Файл {file} переименован в {new_name}')
            except Exception as e:
                print(f'Ошибка при переименовании {old_path} -> {new_path}: {e}')
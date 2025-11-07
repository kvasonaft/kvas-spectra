from to_sql import sqlite_db
from to_json import json_db
from renaming import folders_rename, files_rename
from query import query
from core_2 import core
from post_core import post_core
import counter
from clipper import clipper
from pathlib import Path
import shutil
from regression import regression
from peaks_and_square import peaks_and_square
from variance import compute_variance


def pipeline(table_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/metadata.xlsx', 
             names_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/names.csv', 
             data_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/dataset', 
             old_column = 'Old_names', 
             new_column = 'New_names', 
             rename_files = False,
             rename_folders = False,
             renaiming_mode = 'experiments', 
             target = None, 
           drop_culture = [], cluster_processing=False, cluster_names=None, clusters=None,
           ranges=None, csv_separator=';', indicators_on_pictures=False, delta=20, color_con='black',
           color_exp='orange', plot=True, square=True, baseline_square='horizontal_full', savgol_window=21, 
           circle=False, pca_choise=False, cluster=True, json=False, sql=False, compute_differences=True, 
           diagrams=True, regression_choise=False, compute_peaks_and_square=False, 
           compute_variance_choise=False, variance_mode='cv', variance_filename='variance_hf_', 
           output_path='/Users/kvasonaft/Desktop'):

    if rename_files:
        files_rename(mode = renaiming_mode, 
                        path = data_path, format = 'txt')
    if rename_folders:
        folders_rename(old_column, new_column, folder_path = data_path, 
                        table_path = names_path, separator = csv_separator)
    if json:
        json_db(table = table_path, 
                folder = data_path)
    if sql:
        sqlite_db(table = table_path, 
                folder = data_path)
        query(path = 'data/spectra.db')

    if compute_differences:

        if target == None:
            raise ValueError('Для проведения вычислений разниц между спектрами укажите мишени волновых чисел.')
        
        core(target=target, drop_culture=drop_culture, indicators_on_pictures=indicators_on_pictures, 
                delta=delta, color_con=color_con, color_exp=color_exp, plot=plot, square=square, 
                baseline_square=baseline_square, savgol_window=savgol_window)

    if compute_peaks_and_square:

        if target == None:
                    raise ValueError('Для проведения вычислений разниц между ' \
                    'спектрами укажите мишени волновых чисел.')

        peaks_and_square(target=target, savgol_window=savgol_window, 
                    delta=delta, baseline_square=baseline_square)

    if diagrams:

        if (not circle) and (not pca_choise) and (not cluster):
            raise ValueError('Для построения диаграм выберите хотя бы один их тип.')

        post_core(circle=circle, pca_choise=pca_choise, cluster=cluster)

    if regression_choise:

        regression(scatter_color='orange', line_color='green')

    if compute_variance_choise:
         
         compute_variance(target=target, mode=variance_mode, filename=variance_filename)

    if cluster_processing:

        if cluster_names == None:
            raise ValueError('Для анализа кластеров введите их названия.')
        if clusters == None:
            raise ValueError('Для анализа кластеров введите их список.')
        if ranges == None:
            raise ValueError('Для анализа кластеров введите смысловые диапазоны волновых чисел.')
        
        for name, cluster_it in zip(cluster_names, clusters):
            clipper(cluster_name=name, cultures=cluster_it, target=target, ranges=ranges, con_color=color_con, exp_color=color_exp)
            counter.counter(cluster_name=name, cultures=cluster_it)
        
    shutil.copytree('Graphs', Path(output_path, 'Kvas-spectra results'))

if __name__ == '__main__':

        pipeline(table_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/metadata.xlsx', 
                names_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/names.csv', 
                data_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/dataset', 
                old_column = 'Old_names', 
                new_column = 'New_names', 
                rename_files = False,
                rename_folders = False,
                renaiming_mode = 'experiments', 
                target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453,
                1410, 1370, 1342, 1240, 1176, 1096, 1050, 1016, 972, 872, 848, 792], 
                drop_culture = [], cluster_processing=True, cluster_names=['A', 'B', 'C'], 
                clusters=[['P-Mw-PET-2_8rec-bt-433-M', 'P-Mw-PET-1-sf-ab-387-D', 'P-Mw-PET-1-bt-ab-387-D'], 
                          ['P-Mw-PET-2_8rec-bt-433-M', 'P-Mw-PET-1-sf-ab-387-D', 'P-Mw-PET-1-bt-ab-387-D'], 
                          ['P-Mw-PET-2_8rec-bt-433-M', 'P-Mw-PET-1-sf-ab-387-D', 'P-Mw-PET-1-bt-ab-387-D']],
                ranges=[(3020, 3080), (2780, 3100), (1480, 1800), (1310, 1520), (900, 1330), (600, 915)], 
                csv_separator=';', indicators_on_pictures=False, delta=20, color_con='black',
                color_exp='orange', plot=True, square=True, baseline_square='horizontal_full', savgol_window=21, 
                circle=False, pca_choise=False, cluster=True, json=False, sql=False, compute_differences=True, 
                diagrams=True, regression_choise=False, compute_peaks_and_square=False, 
                compute_variance_choise=False, variance_mode='cv', variance_filename='variance_hf_', 
                output_path='/Users/kvasonaft/Desktop')
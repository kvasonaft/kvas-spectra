from to_sql import sqlite_db
from to_json import json_db
from renaming import folders_rename, files_rename
from query import query
from core_2 import core
from post_core import post_core
from counter import counter
from clipper import clipper
from pathlib import Path
import shutil
# from regression import regression
from peaks_and_square import peaks_and_square
# from variance import compute_variance
import pandas as pd


def pipeline(table_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/metadata.xlsx', 
             names_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/names.csv', 
             data_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/dataset', 
             old_column = 'Old_names', 
             new_column = 'New_names', 
             rename_files = False,
             rename_folders = False,
             renaiming_mode = 'experiments', 
             target = None, 
           drop_culture = [], cluster_processing=False,
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
                baseline_square_ext=baseline_square, savgol_window=savgol_window)

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

    # if regression_choise:

    #     regression(scatter_color='orange', line_color='green')

    # if compute_variance_choise:
         
    #      compute_variance(target=target, mode=variance_mode, filename=variance_filename)

    if cluster_processing:

        if ranges == None:
            raise ValueError('Для анализа кластеров введите смысловые диапазоны волновых чисел.')
        
        data_area = pd.read_csv('data/cluster_labels_area.csv')
        data_area['Cluster'] = data_area['Cluster'].astype(int)
        cluster_max = max(data_area['Cluster'])
        cluster_dict = {}

        for i in range(1, cluster_max+1, 1):
            cluster_dict[i] = []

        for _, row in data_area.iterrows():
            for i in range(1, cluster_max+1, 1):
                if row['Cluster'] == i:
                    if row['Sample'] not in cluster_dict[row['Cluster']]:
                        cluster_dict[row['Cluster']].append(row['Sample'])
        clusters = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cluster_dict.items()]))

        for cluster_num, cluster_data in clusters.items():
            non_nan_values = cluster_data.dropna()
            if not non_nan_values.empty:
                cultures = non_nan_values.tolist()
                clipper(cluster_name=cluster_num, cultures=cultures, target=target, 
                    ranges=ranges, con_color=color_con, exp_color=color_exp, added_path=' (clusters by area)')
                counter(cluster_name=cluster_num, cultures=cultures, area=True, peaks=False)
        
        data_peaks = pd.read_csv('data/cluster_labels_peaks.csv')
        data_peaks['Cluster'] = data_peaks['Cluster'].astype(int)
        cluster_max_peaks = max(data_peaks['Cluster'])
        cluster_dict_peaks = {}

        for i in range(1, cluster_max_peaks+1, 1):
            cluster_dict_peaks[i] = []

        for _, row in data_peaks.iterrows():
            for i in range(1, cluster_max_peaks+1, 1):
                if row['Cluster'] == i:
                    if row['Sample'] not in cluster_dict_peaks[row['Cluster']]:
                        cluster_dict_peaks[row['Cluster']].append(row['Sample'])

        clusters_peaks = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cluster_dict_peaks.items()]))

        for cluster_num, cluster_data in clusters_peaks.items():
            non_nan_values = cluster_data.dropna()
            if not non_nan_values.empty:
                cultures = non_nan_values.tolist()
                clipper(cluster_name=cluster_num, cultures=cultures, target=target, 
                    ranges=ranges, con_color=color_con, exp_color=color_exp, added_path=' (clusters by peaks)')
                counter(cluster_name=cluster_num, cultures=cultures, peaks=True, area=False)

    shutil.copytree('Graphs', Path(output_path, 'Actual results'))

if __name__ == '__main__':

        pipeline(table_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/metadata.xlsx', 
                names_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/names.csv', 
                data_path = '/Users/kvasonaft/Desktop/Development/kvas-spectra/data/dataset', 
                old_column = 'Old_names', 
                new_column = 'New_names', 
                rename_files = False,
                rename_folders = False,
                cluster_processing=True,
                json=False,
                sql=False,
                compute_differences=False, 
                regression_choise=False,
                compute_peaks_and_square=False, 
                compute_variance_choise=False,
                renaiming_mode = 'experiments', 
                target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453,
                1410, 1370, 1342, 1240, 1176, 1096, 1050, 1016, 972, 872, 848, 792], 
                drop_culture = [], 
                ranges=[(3020, 3080), (2780, 3100), (1480, 1800), (1310, 1520), (900, 1330), (600, 915)], 
                csv_separator=';', indicators_on_pictures=False, 
                delta=20, color_con='black',
                color_exp='orange', plot=True, square=True, 
                baseline_square='horizontal_full', savgol_window=21, 
                circle=False, pca_choise=False, cluster=True, 
                diagrams=True,
                variance_mode='cv', variance_filename='variance_hf_', 
                output_path='/Users/kvasonaft/Desktop')
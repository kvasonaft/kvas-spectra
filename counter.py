import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def make_panel(n_plots, figsize_per_plot=(8, 8)):
    cols = math.ceil(math.sqrt(n_plots))
    rows = math.ceil(n_plots / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(figsize_per_plot[0]*cols, figsize_per_plot[1]*rows))
    axes = np.array(axes).flatten()

    for j in range(n_plots, len(axes)):
        axes[j].set_visible(False)

    return fig, axes[:n_plots]

def counter(cluster_name, cultures, peaks=False, area=True):

    cluster = cultures
    sns.set_theme(style="darkgrid", palette="colorblind")

    if area:
        area_indicators = pd.read_csv('data/area_indicator.csv', names=['culture', 'Indicator'], header=None)
        area_indicators = area_indicators[1:]
        area_ind = np.array(list(area_indicators['Indicator']))
        area_values = pd.read_csv('data/area_main.csv')
        result_dict_area = {'Wavenumber':list(area_values['Wavelength'])}
        wavenumbers = list(area_values['Wavelength'])
        area_values = area_values.drop(area_values.columns[0], axis=1)
        area_values = area_values.fillna(0)

        for culture, col_data in area_values.items():
            number = area_indicators[area_indicators['culture']==culture]['Indicator'].values[0]
            percent = np.asarray(col_data) / float(number) * 100
            result_dict_area[culture] = percent

        result_dict_area = pd.DataFrame(result_dict_area)
        result_dict_area = result_dict_area[cluster]

        fig, axes = make_panel(len(cluster))

        for idx, (culture, col_data) in enumerate(result_dict_area.items()):

            sns.barplot(x=wavenumbers, y=col_data, ax=axes[idx])
            axes[idx].set_title(culture, fontsize=14)
            axes[idx].set_xlabel('Центры диапазонов поиска пиков, см(-1)')
            axes[idx].set_ylabel('Вклад в интегральный показатель, %')
            axes[idx].tick_params(axis='x', rotation=45)
            plt.tight_layout()

        plt.suptitle(f'Кластер {cluster_name}', fontsize=18, y=0.99)
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.15, hspace=0.3)
        plt.savefig(f'graphs/counted/area/{cluster_name}_area.png', dpi=300, bbox_inches='tight')

    if peaks:
        peaks_indicators = pd.read_csv('data/peaks_indicator.csv', names=['culture', 'Indicator'], header=None)
        peaks_indicators = peaks_indicators[1:]
        peaks_ind = np.array(list(peaks_indicators['Indicator']))
        peaks_values = pd.read_csv('data/peaks_main.csv')
        result_dict_peaks = {'Wavenumber':list(peaks_values['Wavelength'])}
        wavenumbers = list(peaks_values['Wavelength'])
        peaks_values = peaks_values.drop(peaks_values.columns[0], axis=1)
        peaks_values = peaks_values.fillna(0)

        for culture, col_data in peaks_values.items():
            number = peaks_indicators[peaks_indicators['culture']==culture]['Indicator'].values[0]
            percent = np.asarray(col_data) / float(number) * 100
            result_dict_peaks[culture] = percent

        result_dict_peaks = pd.DataFrame(result_dict_peaks)
        result_dict_peaks = result_dict_peaks[cluster]

        fig, axes = make_panel(len(cluster))

        for idx, (culture, col_data) in enumerate(result_dict_peaks.items()):

            sns.barplot(x=wavenumbers, y=col_data, ax=axes[idx])
            axes[idx].set_title(culture, fontsize=14)
            axes[idx].set_xlabel('Центры диапазонов поиска пиков, см(-1)')
            axes[idx].set_ylabel('Вклад в интегральный показатель, %')
            axes[idx].tick_params(axis='x', rotation=45)
            plt.tight_layout()

        plt.suptitle(f'Кластер {cluster_name}', fontsize=18, y=0.99)
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.15, hspace=0.3)
        plt.savefig(f'graphs/counted/peaks/{cluster_name}_peaks.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    counter(cultures = ['B-BS-22-HF-4-2-4-282-G', 'B-BS-22-HF-ms-2-3-282-G', 'B-BS-22-HF-ms-1-1-973-G'], cluster_name='test_cluster')
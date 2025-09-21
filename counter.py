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

cluster = ['F-Arctic-PET-462-28-B', 'F-Bl-PET-454-211-A', 'F-Bl-PET-461-28-A', 'F-Bl-PET-468-28-A', 'P-Bl-PET-15-sm-204-C', 'P-Bl-PET-15-sm-378-C', 'P-Bl-PET-15-sm-98-C', 'P-Bl-PET-5-sm-204-C', 'P-Bl-PET-5-sm-378-C', 'P-Bl-PET-5-sm-98-C', 'P-Mw-PET-2-bt-ab-184-D', 'B-BS-22-HF-4-2-4-282-G', 'B-BS-22-HF-ms-2-3-282-G', 'B-BS-22-HF-ms-1-1-973-G', 'P-Mw-HF-Profi-1-sf-433-I', 'P-Mw-HF-Profi-2-bt-433-I', 'P-Mw-HF-Soft-1-sf-387-J', 'P-Mw-HF-Foot-2-bt-433-H', 'P-Mw-HF-Foot-2-sf-433-H', 'P-Mw-PET-2-sf-sm-434-E', 'P-Mw-PET-1-sf-sm-388-E']

sns.set_theme(style="darkgrid", palette="colorblind")

area_indicators = pd.read_csv('area_indicator.csv', names=['culture', 'Indicator'], header=None)
area_indicators = area_indicators[1:]
area_ind = np.array(list(area_indicators['Indicator']))

peaks_indicators = pd.read_csv('peaks_indicator.csv', names=['culture', 'Indicator'], header=None)
peaks_indicators = peaks_indicators[1:]
peaks_ind = np.array(list(peaks_indicators['Indicator']))

area_values = pd.read_csv('area_main.csv')
peaks_values = pd.read_csv('peaks_main.csv')

result_dict_area = {'Wavenumber':list(area_values['Wavelength'])}
result_dict_peaks = {'Wavenumber':list(area_values['Wavelength'])}

wavenumbers = list(area_values['Wavelength'])

area_values = area_values.drop(area_values.columns[0], axis=1)
peaks_values = peaks_values.drop(peaks_values.columns[0], axis=1)

area_values = area_values.fillna(0)
peaks_values = peaks_values.fillna(0)

for culture, col_data in area_values.items():
    number = area_indicators[area_indicators['culture']==culture]['Indicator'].values[0]
    percent = np.asarray(col_data) / float(number) * 100
    result_dict_area[culture] = percent

for culture, col_data in peaks_values.items():
    number = peaks_indicators[peaks_indicators['culture']==culture]['Indicator'].values[0]
    percent = np.asarray(col_data) / float(number) * 100
    result_dict_peaks[culture] = percent

result_dict_area = pd.DataFrame(result_dict_area)
result_dict_peaks = pd.DataFrame(result_dict_peaks)

result_dict_area = result_dict_area[cluster]
result_dict_peaks = result_dict_peaks[cluster]

# fig, axes = make_panel(len(cluster))

# for idx, (culture, col_data) in enumerate(result_dict_area.items()):

#     sns.barplot(x=wavenumbers, y=col_data, ax=axes[idx])
#     axes[idx].set_title(culture, fontsize=14)
#     axes[idx].set_xlabel('Центры диапазонов поиска пиков, см(-1)')
#     axes[idx].set_ylabel('Вклад в интегральный показатель, %')
#     axes[idx].tick_params(axis='x', rotation=45)
#     plt.tight_layout()

# plt.suptitle('Кластер А1 (площади)', fontsize=22, y=0.99)
# plt.tight_layout()
# plt.subplots_adjust(wspace=0.15, hspace=0.3)
# plt.savefig(f'/home/kvasonaft/Development/graphs/percent/area/A1_areas.png', dpi=300, bbox_inches='tight')
# plt.show()

fig, axes = make_panel(len(cluster))

for idx, (culture, col_data) in enumerate(result_dict_peaks.items()):

    sns.barplot(x=wavenumbers, y=col_data, ax=axes[idx])
    axes[idx].set_title(culture, fontsize=14)
    axes[idx].set_xlabel('Центры диапазонов поиска пиков, см(-1)')
    axes[idx].set_ylabel('Вклад в интегральный показатель, %')
    axes[idx].tick_params(axis='x', rotation=45)
    plt.tight_layout()

plt.suptitle('Кластер E', fontsize=18, y=0.99)
plt.tight_layout()
plt.subplots_adjust(wspace=0.15, hspace=0.3)
plt.savefig(f'/home/kvasonaft/Development/graphs/percent/peaks/E_peaks.png', dpi=300, bbox_inches='tight')
plt.show()

import json
import matplotlib.pyplot as plt
import numpy as np
import warnings
from pybaselines import Baseline
from scipy.signal import savgol_filter
from matplotlib.lines import Line2D

warnings.filterwarnings("ignore", category=RuntimeWarning)

def clipper(cluster_name, cultures, exp_color='orange', con_color='black',
            target=[3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453,
                     1410, 1370, 1342, 1240, 1176, 1096, 1050, 1016,972, 872, 848, 792],
                         ranges=[(3020, 3080), (2780, 3100), (1480, 1800), (1310, 1520), (900, 1330), (600, 915)], 
                         savgol_window=21):

    # ranges = [(3020, 3080), (2780, 3100), (1480, 1800), (1310, 1520), (900, 1330), (600, 915)]

    ranges_char = []

    for pair in ranges:
        first = str(pair[1])
        second = str(pair[0])
        element = first + '-' + second
        ranges_char.append(element)

    fig, axes = plt.subplots(2, 3, figsize=(20, 10))
    axes = axes.flatten()

    for idx in range(len(ranges_char)):

        start = ranges[idx][0]
        stop = ranges[idx][1]

        data = None

        with open('data/spectra_dict.json', 'r', encoding = 'utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(e)

        cultures = cultures

        if data is None:
            raise ValueError(f'Ошибка при загрузке файла JSON.')

        # fig, axes = plt.subplots((2, 3), figsize=(20, 10))

        for culture, data_1 in data.items():

            if culture not in cultures:
                continue
            else:

                for type, data_2 in data_1.items():

                    if type not in ['Control', 'Experiment']:
                        continue

                    if type == 'Control':
                        
                        all_wavenumbers_con = []
                        all_absorptions_con = []

                        for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                            x = data_3['wavelength']
                            y = data_3['absorption']

                            x = np.asarray(x, dtype=float)
                            y = np.asarray([str(v).replace(',', '.') for v in y], dtype=float)

                            y = savgol_filter(y, window_length=savgol_window, polyorder=3)
                            y = -y

                            baseline_fitter = Baseline(x_data=x)
                            bl_4, _ = baseline_fitter.snip(y, max_half_window=40, decreasing=True, smooth_half_window=3)
                            y = y - bl_4

                            indx = np.where(((x >= 650) & (x <= 1800)))[0]
                            if indx.size == 0:
                                raise ValueError("В заданном окне нет точек.")
                            norm = np.linalg.norm(y[indx])
                            y = y / norm

                            # y = y + abs(np.min(y))

                            important = np.array([start, stop])
                            indices = np.nonzero(np.isin(x, important))[0]
                            values = y[np.min(indices):np.max(indices)+1]

                            all_wavenumbers_con.extend(important)
                            all_absorptions_con.extend(values)

                            axes[idx].plot(x[np.min(indices):np.max(indices)+1], values, color='black')

                    elif type == 'Experiment':

                        all_wavenumbers_exp = []
                        all_absorptions_exp = []

                        for i, (sample, data_3) in enumerate(data_2.items(), start = 1):

                            x = data_3['wavelength']
                            y = data_3['absorption']

                            x = np.asarray(x, dtype=float)
                            y = np.asarray([str(v).replace(',', '.') for v in y], dtype=float)

                            y = savgol_filter(y, window_length=savgol_window, polyorder=3)
                            y = -y

                            baseline_fitter = Baseline(x_data=x)
                            bl_4, _ = baseline_fitter.snip(y, max_half_window=40, decreasing=True, smooth_half_window=3)
                            y = y - bl_4

                            indx = np.where(((x >= 650) & (x <= 1800)))[0]
                            if indx.size == 0:
                                raise ValueError("В заданном окне нет точек.")
                            norm = np.linalg.norm(y[indx])
                            y = y / norm

                            important = np.array([start, stop])
                            indices = np.nonzero(np.isin(x, important))[0]
                            values = y[np.min(indices):np.max(indices)+1]

                            all_wavenumbers_exp.extend(important)
                            all_absorptions_exp.extend(values)

                            axes[idx].plot(x[np.min(indices):np.max(indices)+1], values, color=exp_color)

        custom_lines = [Line2D([0], [0], color=con_color, lw=2), Line2D([0], [0], color=exp_color, lw=2)]
        axes[idx].legend(custom_lines, ['Эксперимент', 'Контроль'])
        axes[idx].set_xlabel('Обратные длины волн, см(-1)', fontsize = 10)
        axes[idx].set_ylabel('Пропускание, %', fontsize = 10)
        axes[idx].set_title(f'{ranges_char[idx]} см(-1)', fontsize = 12)

        plt.grid()
        plt.tight_layout()

    fig.suptitle(f'Кластер {cluster_name}', fontsize=24)
    plt.tight_layout()
    plt.savefig(f'graphs/clipped/{cluster_name}.png', dpi = 300, bbox_inches = 'tight')

if __name__ == '__main__':
    clipper('test_cluster', ['P-Mw-PET-2_8rec-bt-433-M', 'P-Mw-PET-1-sf-ab-389-D', 'P-Mw-PET-1-bt-ab-387-D'])
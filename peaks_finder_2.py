
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths
from scipy.integrate import trapezoid
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from matplotlib.patches import Polygon
import pandas as pd
import peaks_finder

data = pd.read_csv('data.txt', sep = '\t', header = None)

x = data[0]
y = data[1]

target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 1453, 1410, 1370, 1342, 1240, 1176, 1124, 1096, 1050, 1016, 972, 929, 872, 848, 792, 771]

def find_nearest(main_idx, side_indices):

    side_indices = np.asarray(side_indices).flatten()

    left_candidates = side_indices[side_indices < main_idx]
    right_candidates = side_indices[side_indices > main_idx]

    left_idx = int(left_candidates.max()) if left_candidates.size > 0 else None
    right_idx = int(right_candidates.min()) if right_candidates.size >0 else None

    return left_idx, right_idx

def peaks_finder_2(x, y, targets, ax = None, delta = 20, integration = 1.5, plot = True, color = 'green', square = False, hatch = False, logging = True):

    x = np.asarray(x, dtype=float)
    y = np.asarray([str(v).replace(',', '.') for v in y], dtype=float)

    results = {'target': [], 'found_x': [], 'height': [], 'area': []}

    y = median_filter(y, size = 5)
    y = savgol_filter(y, window_length = 11, polyorder = 3)

    if ax is None:
        ax = plt.gca()    

    ax.plot(x, y, color = color, linewidth = 1)

    for target in targets:

        mask = (x >= target - delta) & (x <= target + delta)
        x_win = x[mask]
        y_win = y[mask]

        if len(x_win) == 0:
            print(f'Окно пустое около {target}')

        peaks, _ = find_peaks(-y_win, prominence = 0.01)

        if len(peaks) == 0:

            if logging == True:
                print(f'Пиков около {target} не обнаружено')

            results['target'].append(target)
            results['found_x'].append(np.nan)
            results['height'].append(np.nan)
            results['area'].append(np.nan)
            continue

        best_peak_idx = peaks[np.argmax(y_win[peaks])]
        peak_x = x_win[best_peak_idx]
        peak_y = y_win[best_peak_idx]

        ax.axvspan(target - 5, target + 5, color = 'gray', alpha = 0.01)
        ax.plot(peak_x, peak_y, 'ro', alpha = 1, markersize = 4)

        # "Side"-part

        delta = delta

        mask = (x >= target - delta) & (x <= target + delta)
        x_win = x[mask]
        y_win = y[mask]

        side_peaks, _ = find_peaks(y_win, prominence = 0.01)
        side_peaks_indices = side_peaks
        side_peaks_indices = np.asarray(side_peaks_indices).flatten()

        left_side, right_side = find_nearest(best_peak_idx, side_peaks_indices)

        if left_side is not None:
            left_side_x = x_win[left_side]
            left_side_y = y_win[left_side]
            ax.plot(left_side_x, left_side_y, 'yo', markersize=4)

        if right_side is not None:
            right_side_x = x_win[right_side]
            right_side_y = y_win[right_side]
            ax.plot(right_side_x, right_side_y, 'yo', markersize=4)

        global_indices = np.where(mask)[0]
        peak_global_idx = global_indices[best_peak_idx]

        if left_side == None or right_side == None:
            continue
        else:
            left_side_global_idx = global_indices[left_side]
            right_side_global_idx = global_indices[right_side]

            left = max(0, left_side_global_idx)
            right = min(len(x), right_side_global_idx)

            if left >= right:
                results['area'].append(None)
                continue
            else:
                x_int= x[left:right]
                y_int = y[left:right]

                baseline = np.linspace(y_int[0], y_int[-1], len(y_int))

                corrected_signal = baseline - y_int

                corrected_signal[corrected_signal < 0] = 0

                area = trapezoid(corrected_signal, x_int)

        results['target'].append(target)
        results['found_x'].append(peak_x)
        results['height'].append(round(peak_y, 2))
        results['area'].append(round(-area, 2))

        if hatch == True:
            polygon = Polygon(np.column_stack((x_int, y_int)), closed = True, facecolor = 'none', edgecolor = color, hatch = '++', alpha = 0.3)
            ax.add_patch(polygon)

        if square == True:
            ax.fill_between(x_int, y_int, baseline, alpha = 0.2, color = color)

    plt.show()

    return results

results1 = peaks_finder_2(x, y, targets = target, square = True)
# results2 = peaks_finder.peaks_finder(x, y, target, square = True, plot = True)
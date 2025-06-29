
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths
from scipy.integrate import trapezoid
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from matplotlib.patches import Polygon

def peaks_finder(x, y, targets, ax = None, delta = 20, integration = 1.5, plot = False, color = 'green', square = False, hatch = False, log_missing = False):

    x = np.asarray(x, dtype=float)
    y = np.asarray([str(v).replace(',', '.') for v in y], dtype=float)


    results = {'target': [], 'found_x': [], 'height': [], 'area': []}

    y = median_filter(y, size = 5)
    y = savgol_filter(y, window_length = 10, polyorder = 3)

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

            if log_missing == True:
                print(f'Пиков около {target} не обнаружено')

            results['target'].append(target)
            results['found_x'].append(np.nan)
            results['height'].append(np.nan)
            results['area'].append(np.nan)
            continue

        best_peak_idx = peaks[np.argmax(y_win[peaks])]
        peak_x = x_win[best_peak_idx]
        peak_y = y_win[best_peak_idx]

        global_indices = np.where(mask)[0]
        peak_global_idx = global_indices[best_peak_idx]

        peak_width = peak_widths(-y, [peak_global_idx], rel_height = 0.5)[0][0]

        if target == 1096 or target == 1240:
            integration = integration * 0.8
        elif target == 1730:
            integration = integration * 4
        elif target == 2969:
            integration = integration * 0.35
        elif target == 972 or target == 1016:
            integration = integration * 1.4

        half_width = round(peak_width * integration)

        left = max(0, peak_global_idx - half_width)
        right = min(len(x), peak_global_idx + half_width)
        
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
            polygon = Polygon(np.column_stack((x_int, y_int)), closed = True, facecolor = 'none', edgecolor = color, hatch = '+++', alpha = 0.3)
            ax.add_patch(polygon)

        if square == True:
            ax.fill_between(x_int, y_int, baseline, alpha = 0.2, color = color)

        ax.axvspan(target - delta, target + delta, color = 'gray', alpha = 0.01)
        ax.plot(peak_x, peak_y, 'ro', alpha = 0.7, markersize = 6)

    return results

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths
from scipy.integrate import trapezoid
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter

def peaks_finder(x, y, targets, delta = 20, integration = 1.5, plot = False):

    results = []

    y = median_filter(y, size = 5)
    y = savgol_filter(y, window_length = 11, polyorder = 3)

    plt.figure(figsize = (12, 6))
    plt.plot(x, y, label = 'Спектр', color = 'blue')

    for target in targets:
        mask = (x >= target - delta) & (x <= target + delta)
        x_win = x[mask]
        y_win = y[mask]

        if len(x_win) == 0:
            print(f'Окно пустое около {target}')

        peaks, _ = find_peaks(-y_win, prominence = 0.01)

        if len(peaks) == 0:
            print(f'Пиков около {target} не обнаружено')
            results.append({'target': target, 'found_x': np.nan, 'height': np.nan, 'area': np.nan})
            continue

        best_peak_idx = peaks[np.argmax(y_win[peaks])]
        peak_x = x_win[best_peak_idx]
        peak_y = y_win[best_peak_idx]

        global_indices = np.where(mask)[0]
        peak_global_idx = global_indices[best_peak_idx]

        peak_width = peak_widths(-y, [peak_global_idx], rel_height = 0.5)[0][0]

        if target == 1096:
            integration = integration * 0.6
        elif target == 1730:
            integration = integration * 5
        elif target == 2969:
            integration = integration * 0.35
        elif target == 1240:
            integration = integration * 0.75

        half_width = round(peak_width * integration)

        left = max(0, peak_global_idx - half_width)
        right = min(len(x), peak_global_idx + half_width)
        
        x_int= x[left:right]
        y_int = y[left:right]

        baseline = np.linspace(y_int[0], y_int[-1], len(y_int))

        corrected_signal = baseline - y_int

        corrected_signal[corrected_signal < 0] = 0

        area = trapezoid(corrected_signal, x_int)

        results.append({'target': target, 'found_x': peak_x, 'height': peak_y, 'area': round(area, 2)})

        plt.plot(peak_x, peak_y, 'ro')
        plt.fill_between(x_int, y_int, baseline, alpha = 0.5, color = 'red')
        plt.axvspan(target - delta, target + delta, color = 'gray', alpha = 0.15)

        x_text = target + delta * 0.1
        y_text = max(y[(x >= target - delta) & (x <= target + delta)]) * 1.05
        plt.text(x_text, y_text, str(target), color = 'black', fontsize = 9, rotation = 90, verticalalignment = 'bottom')

    if plot == True:

        plt.xlabel("x")
        plt.ylabel("Интенсивность")
        plt.title("Найденные пики в заданных областях")
        plt.legend(['Спектр', 'Найденные пики', 'Площади', 'Области поиска'])
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return results
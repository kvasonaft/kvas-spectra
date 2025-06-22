
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapezoid

def peaks_finder(x, y, targets, delta = 20, plot = False):

    results = []

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

        integration_window = 10
        global_indices = np.where(mask)[0]
        peak_global_idx = global_indices[best_peak_idx]

        left = max(0, peak_global_idx - integration_window)
        right = min(len(x), peak_global_idx + integration_window)
        
        x_int= x[left:right]
        y_int = y[left:right]

        baseline = np.linspace(y_int[0], y_int[-1], len(y_int))

        corrected_signal = baseline - y_int

        corrected_signal[corrected_signal < 0] = 0

        area = trapezoid(corrected_signal, x_int)

        results.append({'target': target, 'found_x': peak_x, 'height': peak_y, 'area': area})

        plt.plot(peak_x, peak_y, 'ro')
        plt.fill_between(x_int, y_int, baseline, alpha = 0.3, color = 'orange')

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
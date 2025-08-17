
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapezoid
from scipy.signal import savgol_filter
from matplotlib.patches import Polygon
from pybaselines import Baseline
import logging
import normalization

def find_nearest(main_idx, side_indices):

    """
    Находит ближайшие к заданному индексу элементы слева и справа из массива индексов.

    Функция используется для поиска ближайших "боковых" максимумов (по индексам) по отношению к главному пику.
    Возвращает наибольший индекс из `side_indices`, который меньше `main_idx` (слева),
    и наименьший индекс, который больше `main_idx` (справа).

    Аргументы:
        main_idx (int): Индекс главного пика, относительно которого осуществляется поиск.
        side_indices (array-like): Массив индексов, в котором осуществляется поиск ближайших значений.

    Возвращает:
        tuple:
            - left_idx (int or None): Индекс ближайшего меньшего элемента (слева), либо None, если такого нет.
            - right_idx (int or None): Индекс ближайшего большего элемента (справа), либо None, если такого нет.

    Пример:
        >>> find_nearest(100, [50, 80, 120, 140])
        (80, 120)
    """

    side_indices = np.asarray(side_indices).flatten()

    left_candidates = side_indices[side_indices < main_idx]
    right_candidates = side_indices[side_indices > main_idx]

    left_idx = int(left_candidates.max()) if left_candidates.size > 0 else None
    right_idx = int(right_candidates.min()) if right_candidates.size >0 else None

    return left_idx, right_idx

def append_result(results, target, peak_x=np.nan, peak_y=np.nan, area=np.nan):
    results['target'].append(target)
    results['found_x'].append(peak_x)
    results['height'].append(round(peak_y, 2) if not np.isnan(peak_y) else np.nan)
    results['area'].append(round(area, 2) if not np.isnan(area) else None)

def peaks_finder_3(x, y, targets, ax=None, delta=20, side_delta=300, yellow_dots = False, color='green', square=False, hatch=False, log=False, baseline_square='linear', prominence=0.01, baseline_primary='snip', plot=False, savgol_window=11, zero=False, positive_peaks=True):

    area = None

    x = np.asarray(x, dtype=float)
    y = np.asarray([str(v).replace(',', '.') for v in y], dtype=float)

    y = savgol_filter(y, window_length=savgol_window, polyorder=3)

    y = normalization.normalization(x, y, start=3900, stop=3990, positive_peaks=positive_peaks, min_max=True)

    y = -y

    results = {'target': [], 'found_x': [], 'height': [], 'area': []}

    baseline_fitter = Baseline(x_data=x)
        
    if plot:
        if ax is None:
            ax = plt.gca()

    if baseline_primary == 'modpoly':
        bl_1, _ = baseline_fitter.modpoly(y, poly_order=3)
        # ax.plot(x, bl_1, color='blue', linewidth=1, label='modpoly')
    elif baseline_primary == 'asls':
        bl_2, _ = baseline_fitter.asls(y, lam=1e7, p=0.02)
        # ax.plot(x, bl_2, color='blue', linewidth=1, label='asls')
    elif baseline_primary == 'mor':
        bl_3, _ = baseline_fitter.mor(y, half_window=30)
        # ax.plot(x, bl_3, color='blue', linewidth=1, label='mor')
    elif baseline_primary == 'snip':
        bl_4, _ = baseline_fitter.snip(y, max_half_window=40, decreasing=True, smooth_half_window=3)
        # ax.plot(x, bl_4, color='blue', linewidth=1, label='snip')

    y = y - bl_4

    y = y + abs(np.min(y))

    if plot:
        ax.plot(x, y, color=color, linewidth=1)
        if zero:
            ax.plot(np.linspace(450, 4000, len(x)), np.zeros(len(x)))

    # prominence = prominence * (np.max(y) - np.min(y))
    prominence = None

    for target in targets:
        mask = (x >= target - delta) & (x <= target + delta)
        x_win = x[mask]
        y_win = y[mask]

        if len(x_win) == 0:
            if log:
                logging.warning(f'Окно пустое около {target}')
                append_result(results, target, peak_x, peak_y, area)
            continue

        peaks, _ = find_peaks(y_win, prominence=prominence)

        if len(peaks) == 0:
            if log:
                logging.info(f'Пиков около {target} не обнаружено')
                append_result(results, target, peak_x, peak_y, area)
            continue

        best_peak_idx = peaks[np.argmax(y_win[peaks])]
        peak_x = x_win[best_peak_idx]
        peak_y = y_win[best_peak_idx]
        peak_global_idx = np.argmin(np.abs(x - peak_x))

        if plot:
            ax.axvspan(target - 5, target + 5, color='gray', alpha=0.01)
            ax.plot(peak_x, peak_y, 'ro', alpha=1, markersize=4)

        side_mask = (x >= peak_x - side_delta) & (x <= peak_x + side_delta)
        x_side_win = x[side_mask]
        y_side_win = y[side_mask]

        side_peaks, _ = find_peaks(-y_side_win, prominence=prominence)
        side_peaks_indices = np.asarray(side_peaks).flatten()

        if len(side_peaks_indices) == 0:
            if log:
                logging.info(f'Боковых максимумов не найдено около {target}')
                append_result(results, target, peak_x, peak_y, area)
            continue

        side_global_indices = np.where(side_mask)[0][side_peaks_indices]
        left_side, right_side = find_nearest(peak_global_idx, side_global_indices)

        if plot:
            if yellow_dots:
                if left_side is not None and 0 <= left_side < len(x):
                    ax.plot(x[left_side], y[left_side], 'yo', markersize=4)
                if right_side is not None and 0 <= right_side < len(x):
                    ax.plot(x[right_side], y[right_side], 'yo', markersize=4)

        if left_side is None or right_side is None:
            logging.warning(f'Площадь около {target} невозможно рассчитать')
            append_result(results, target, peak_x, peak_y, area)
            continue

        left = left_side
        right = right_side

        if left >= right:
            append_result(results, target, peak_x, peak_y, area)
            continue

        x_int = x[left:right]
        y_int = y[left:right]

        if baseline_square == 'linear':
            baseline = np.linspace(y_int[0], y_int[-1], len(y_int))
        elif baseline_square == 'horizontal':
            baseline = np.full_like(y_int, min(y_int[0], y_int[-1]))
        elif baseline_square == 'horizontal_full':
            baseline = np.full_like(y_int, 0)

        corrected_signal = y_int - baseline
        corrected_signal[corrected_signal < 0] = 0

        area = -trapezoid(corrected_signal, x_int)

        append_result(results, target, peak_x, peak_y, area)

        if plot:
            if hatch:
                polygon = Polygon(np.column_stack((x_int, y_int)), closed=True, facecolor='none', edgecolor=color, hatch='++', alpha=0.3)
                ax.add_patch(polygon)
            if square:
                ax.fill_between(x_int, y_int, baseline, alpha=0.2, color=color)

    return results
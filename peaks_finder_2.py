
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapezoid
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from scipy.signal import medfilt
from matplotlib.patches import Polygon
import logging

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
    results['area'].append(round(area, 2) if not np.isnan(area) else np.nan)

def peaks_finder_2(x, y, targets, ax=None, delta=30, side_delta=300, yellow_dots = False, color='green', square=False, hatch=False, log=False, baseline_type='linear', prominence=0.01):

    """
    Находит пики (локальные минимумы) вблизи заданных целевых значений и рассчитывает площади под ними методом трапеций.

    Функция выполняет поиск локальных минимумов (основных пиков) рядом с каждым значением из списка `targets`. Для каждого найденного пика
    она ищет ближайшие локальные максимумы слева и справа в расширенном окне (`side_delta`) и строит базовую линию между ними.
    Затем рассчитывается площадь между пиком и базовой линией. Результат визуализируется с помощью Matplotlib.

    Аргументы:
        x (array-like): Массив значений по оси X.
        y (array-like): Массив значений по оси Y.
        targets (list of float): Список целевых значений X, вблизи которых нужно искать пики.
        ax (matplotlib.axes.Axes): Объект осей matplotlib для построения графика.
        delta (int): Половина ширины узкого окна поиска основного пика. По умолчанию 20.
        side_delta (int): Половина ширины окна для поиска боковых максимумов. По умолчанию 150.
        yellow_dots (bool): Если True — рисуются жёлтые точки на боковых максимумах. По умолчанию True.
        color (str): Цвет линий на графике. По умолчанию 'green'.
        square (bool): Если True — плошадь под пиком закрашивается. По умолчанию False.
        hatch (bool): Если True — добавляется штриховка площади пика. По умолчанию False.
        logging (bool): Если True — печатаются сообщения о ходе выполнения. По умолчанию False.

    Возвращает:
        dict: Словарь с результатами анализа, содержащий:
            - 'target' (list): Целевые значения (как передано).
            - 'found_x' (list): Найденные координаты X пиков или NaN, если пик не найден.
            - 'height' (list): Значения Y в точках пиков (высоты) или NaN.
            - 'area' (list): Расчётные площади пиков или NaN при ошибке.

    Особенности:
        - Предобработка сигнала включает медианную фильтрацию и сглаживание методом Савицкого–Голея.
        - Если не удаётся найти один из боковых максимумов, площадь не рассчитывается, в итоговый словарь по ключу 'area' добавляется NaN.
        - Основные пики ищутся через `scipy.signal.find_peaks` по инвертированному сигналу (`-y`).

    Пример использования:
        >>> results = peaks_finder_2(x, y, targets=[1730, 1644], square=True, logging=True)
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray([str(v).replace(',', '.') for v in y], dtype=float)

    results = {'target': [], 'found_x': [], 'height': [], 'area': []}

    y = median_filter(y, size=5)
    y = savgol_filter(y, window_length=11, polyorder=3)

    if ax is None:
        ax = plt.gca()

    ax.plot(x, y, color=color, linewidth=1)

    for target in targets:
        mask = (x >= target - delta) & (x <= target + delta)
        x_win = x[mask]
        y_win = y[mask]

        if len(x_win) == 0:
            if log:
                logging.warning(f'Окно пустое около {target}')
                append_result(results, target, peak_x, peak_y, np.nan)
            continue

        peaks, _ = find_peaks(-y_win, prominence=prominence)

        if len(peaks) == 0:
            if log:
                logging.info(f'Пиков около {target} не обнаружено')
                append_result(results, target, peak_x, peak_y, np.nan)
            continue

        best_peak_idx = peaks[np.argmin(y_win[peaks])]
        peak_x = x_win[best_peak_idx]
        peak_y = y_win[best_peak_idx]
        peak_global_idx = np.argmin(np.abs(x - peak_x))

        ax.axvspan(target - 5, target + 5, color='gray', alpha=0.01)
        ax.plot(peak_x, peak_y, 'ro', alpha=1, markersize=4)

        side_mask = (x >= peak_x - side_delta) & (x <= peak_x + side_delta)
        x_side_win = x[side_mask]
        y_side_win = y[side_mask]

        side_peaks, _ = find_peaks(y_side_win, prominence=prominence)
        side_peaks_indices = np.asarray(side_peaks).flatten()

        if len(side_peaks_indices) == 0:
            if log:
                logging.info(f'Боковых максимумов не найдено около {target}')
                append_result(results, target, peak_x, peak_y, np.nan)
            continue

        side_global_indices = np.where(side_mask)[0][side_peaks_indices]
        left_side, right_side = find_nearest(peak_global_idx, side_global_indices)

        if yellow_dots:

            if left_side is not None and 0 <= left_side < len(x):
                ax.plot(x[left_side], y[left_side], 'yo', markersize=4)

            if right_side is not None and 0 <= right_side < len(x):
                ax.plot(x[right_side], y[right_side], 'yo', markersize=4)

        if left_side is None or right_side is None:
            logging.warning(f'Площадь около {target} невозможно рассчитать')
            append_result(results, target, peak_x, peak_y, np.nan)
            continue

        left = left_side
        right = right_side

        if left >= right:
            append_result(results, target, peak_x, peak_y, np.nan)
            continue

        x_int = x[left:right]
        y_int = y[left:right]

        if baseline_type == 'linear':
            baseline = np.linspace(y_int[0], y_int[-1], len(y_int))
        elif baseline_type == 'horizontal':
            baseline = np.full_like(y_int, min(y_int[0], y_int[-1]))

        corrected_signal = baseline - y_int
        corrected_signal[corrected_signal < 0] = 0

        area = trapezoid(corrected_signal, x_int)

        append_result(results, target, peak_x, peak_y, area)

        if hatch:
            polygon = Polygon(np.column_stack((x_int, y_int)), closed=True, facecolor='none', edgecolor=color, hatch='++', alpha=0.3)
            ax.add_patch(polygon)

        if square:
            ax.fill_between(x_int, y_int, baseline, alpha=0.2, color=color)

    return results
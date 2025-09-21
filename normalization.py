import numpy as np
from scipy.signal import find_peaks

def normalization(x, y, start=None, stop=None, positive_peaks=True, min_max=False, lower_percentile=1, upper_percentile=99, normalize_by_peak=False, peak_start=None, peak_stop=None):

    if start==None or stop==None:
        pass
    else:
        important = np.array([start, stop])
        indices = np.nonzero(np.isin(x, important))[0]
        values = y[np.min(indices):np.max(indices)+1]

        if positive_peaks:
            mean_value = np.mean(values) + 100
            y = y - mean_value
        elif not positive_peaks:
            mean_value = np.mean(values) - 100
            y = y - mean_value

    if min_max:
        minimum = np.percentile(y, lower_percentile)
        maximum = np.percentile(y, upper_percentile)
        y = (y-minimum)/(maximum-minimum)
        y = np.clip(y, 0, 1)

    if normalize_by_peak:
        if peak_start is None or peak_stop is None:
            raise ValueError('Для нормализации по пику необходимо указать индексы границ пика.')
        
        values = np.array([peak_start, peak_stop])
        indices = np.nonzero(np.isin(x, values))[0]
        segment = y[np.min(indices):np.max(indices)+1]

        peaks, _ = find_peaks(segment)
        if len(peaks) == 0:
            raise ValueError("В интервале нет пиков")

        # выбираем самый высокий
        peak_idx = peaks[np.argmax(segment[peaks])]
        y_max = segment[peak_idx]

        y = y / y_max

    return(y)
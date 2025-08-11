import numpy as np

def normalization(x, y, start, stop, positive_peaks=True):
    important = np.array([start, stop])
    indices = np.nonzero(np.isin(x, important))[0]
    values = y[np.min(indices):np.max(indices)+1]

    if positive_peaks:
        mean_value = np.mean(values) + 100
        y = y - mean_value
    elif not positive_peaks:
        mean_value = np.median(values) - 100
        y = y - mean_value

    return(y)
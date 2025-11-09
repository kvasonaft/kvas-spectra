import pandas as pd
import matplotlib.pyplot as plt
import peaks_finder_3

target = [3054, 2969, 2908, 1730, 1644, 1577, 1538, 1504, 1470, 
          1410, 1370, 1342, 1240, 1176, 1096, 1050, 1016, 972, 872, 848, 792]

data = pd.read_csv('test_data/test_1.txt', sep='\t', header=None)

x = data[0]
y = data[1]

fig, ax = plt.subplots(figsize = (20, 10))

plt.grid()
plt.title('Стало', fontsize=18)
plt.xlabel('Обратные длины волн, см(-1)', fontsize=16)
plt.ylabel('Интенсивность поглощения', fontsize=16)

res = peaks_finder_3.peaks_finder_3(x, y, targets=target, delta=20, ax=ax, plot=True, 
                                    color='orange', square=True, savgol_window=21, 
                                    baseline_square='horizontal_full', prominence=None, 
                                    show_plot=True)
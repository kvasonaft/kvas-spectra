import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

conn = sqlite3.connect('data/spectra.db')

query = '''
SELECT samples.name, metadata.exposure_time
FROM samples
JOIN metadata ON samples.id = metadata.sample_id
'''

df = pd.read_sql_query(query, conn)

conn.close()

df_area = pd.read_csv('data/area_indicator.csv')
df_peaks = pd.read_csv('data/peaks_indicator.csv')

X_area = df_area[['Indicator']].values
X_peaks = df_peaks[['Indicator']].values
y = df['exposure_time']

model_area = LinearRegression()
model_peaks = LinearRegression()

X_area_train, X_area_test, y_area_train, y_area_test = train_test_split(X_area, y, test_size=0.2, random_state=7)

X_peaks_train, X_peaks_test, y_peaks_train, y_peaks_test = train_test_split(X_peaks, y, test_size=0.2, random_state=7)

model_area.fit(X_area_train, y_area_train)
model_peaks.fit(X_peaks_train, y_peaks_train)

y_area_pred = model_area.predict(X_area_test)
y_peaks_pred = model_peaks.predict(X_peaks_test)

r2_area = round(r2_score(y_area_test, y_area_pred), 2)
r2_peaks = round(r2_score(y_peaks_test, y_peaks_pred), 2)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (10, 6))

y_peaks_test = y_peaks_test.values
y_area_test = y_area_test.values

# Для X_peaks
X_peaks_full = np.linspace(X_peaks.min(), X_peaks.max(), 500).reshape(-1, 1)
y_peaks_full_pred = model_peaks.predict(X_peaks_full)

ax1.scatter(X_peaks, y, color='orange', label='Экспериментальные данные')
ax1.plot(y_peaks_full_pred, X_peaks_full, color='green',
         label=f'Модель линейной регрессии, R² = {r2_peaks}')
ax1.set_title('Интегральный показатель по значениям пиков')
ax1.set_xlabel('Значение интегрального показателя')
ax1.set_ylabel('Время экспонирования, сутки')
ax1.legend()

# Для X_area
X_area_full = np.linspace(X_area.min(), X_area.max(), 500).reshape(-1, 1)
y_area_full_pred = model_area.predict(X_area_full)

ax2.scatter(X_area, y, color='orange', label='Экспериментальные данные')
ax2.plot(y_area_full_pred, X_area_full, color='green',
         label=f'Модель линейной регрессии, R² = {r2_area}')
ax2.set_title('Интегральный показатель по площадям пиков')
ax2.set_xlabel('Значение интегрального показателя')
ax2.set_ylabel('Время экспонирования, сутки')
ax2.legend()

plt.tight_layout()
plt.savefig('/Users/kvasonaft/Desktop/Development/kvas-spectra/graphs/diagrams/regression.png', dpi = 600)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from adjustText import adjust_text
from scipy.cluster.hierarchy import linkage, dendrogram
from matplotlib.patches import Patch
import seaborn as sns
from tqdm import tqdm

area = pd.read_csv('area_main.csv', index_col = 'Wavelength')
peaks = pd.read_csv('peaks_main.csv', index_col = 'Wavelength')

area = area.dropna()
peaks = peaks.dropna()

for  idx, table in tqdm(enumerate([area, peaks]), desc = 'Обработка таблиц'):

    table = table.T

    scaler = StandardScaler()
    table_scaled = scaler.fit_transform(table)

    kmeans = KMeans(n_clusters = 2, random_state = 7)
    kmeans.fit(table_scaled)

    pca = PCA(n_components = 2)
    data_pca = pca.fit_transform(table_scaled)
    pca_df = pd.DataFrame(data_pca, columns = ['PC1', 'PC2'], index = table.index)
    pca_df['cluster'] = kmeans.labels_

    texts = []

    if idx == 1:
        colors = ['green', 'orange']
    else:
        colors = ['orange', 'green']

    fig, ax = plt.subplots(figsize=(12, 8))

    for cluster in [0, 1]:
        ax.scatter(pca_df[pca_df['cluster'] == cluster]['PC1'],
                    pca_df[pca_df['cluster'] == cluster]['PC2'], color = colors[cluster])

    for i, (name, row) in enumerate(pca_df.iterrows()):
        texts.append(
            ax.text(row['PC1'], row['PC2'], str(i), fontsize=9)
        )

    adjust_text(texts)
    
    if idx == 1:
        plt.title(f'Диаграмма двух главных компонент с кластерами, полученными методом k-средних (по значениям пиков)', fontsize = 14)
    else:
        plt.title(f'Диаграмма двух главных компонент с кластерами, полученными методом k-средних (по площадям пиков)', fontsize = 14)

    plt.xlabel(f'Первая главная компонента ({pca.explained_variance_ratio_[0] * 100:.2f}%)', fontsize = 12)
    plt.ylabel(f'Вторая главная компонента ({pca.explained_variance_ratio_[1] * 100:.2f}%)', fontsize = 12)

    if idx == 1:
        plt.savefig('pca_by_peaks.png', dpi = 600, bbox_inches = 'tight')
    else:
        plt.savefig('pca_by_area.png', dpi = 600, bbox_inches = 'tight')

    plt.close()



    linked = linkage(table, method = 'ward', metric = 'euclidean')
    plt.figure(figsize = (15, 10))

    if idx == 1:
        dendrogram(linked, labels = table.index.to_list(), leaf_rotation = 90, leaf_font_size = 10, color_threshold = 120)
    else:
        dendrogram(linked, labels = table.index.to_list(), leaf_rotation = 90, leaf_font_size = 10, color_threshold = 2000)

    if idx == 1:
        plt.title('Результаты иерархического кластерного анализа (по значениям пиков)', fontsize = 22)
    else:
        plt.title('Результаты иерархического кластерного анализа (по площадям пиков)', fontsize = 22)        

    plt.xlabel('Объекты', fontsize = 18)
    plt.ylabel('Расстояние', fontsize = 18)
    plt.tight_layout()

    if idx == 1:
        plt.savefig('dendrogram_by_peaks.png', dpi = 600, bbox_inches = 'tight')
    else:
        plt.savefig('dendrogram_by_area.png', dpi = 600, bbox_inches = 'tight')

    plt.close()




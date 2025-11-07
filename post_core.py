import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from adjustText import adjust_text
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

def post_core(circle=False, pca_choise=False, cluster=True):

    area = pd.read_csv('data/area_main.csv', index_col = 'Wavelength')
    peaks = pd.read_csv('data/peaks_main.csv', index_col = 'Wavelength')

    area = area.dropna()
    peaks = peaks.dropna()

    for idx, table in enumerate([area, peaks]):

        table = table.T

        # correlation circle

        if circle:

            scaler = StandardScaler()
            table_scaled = scaler.fit_transform(table)

            kmeans = KMeans(n_clusters = 2, random_state = 7)
            kmeans.fit(table_scaled)

            pca = PCA(n_components = 2)
            data_pca = pca.fit_transform(table_scaled)
            pca_df = pd.DataFrame(data_pca, columns = ['PC1', 'PC2'], index = table.index)
            pca_df['cluster'] = kmeans.labels_

            loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

            plt.figure(figsize=(8, 8))
            plt.axhline(0, color='gray', lw=1)
            plt.axvline(0, color='gray', lw=1)

            circle = plt.Circle((0,0), 1, color='black', fill=False)
            plt.gca().add_artist(circle)

            for i, var in enumerate(table.columns):
                plt.arrow(0, 0, loadings[i,0], loadings[i,1],
                        color='b', alpha=0.7, head_width=0.03)
                plt.text(loadings[i,0]*1.1, loadings[i,1]*1.1, var,
                        color='r', ha='center', va='center')

            plt.xlabel(f"1-я главная компонента ({pca.explained_variance_ratio_[0]*100:.1f}% дисперсии)")
            plt.ylabel(f"2-я главная компонента ({pca.explained_variance_ratio_[1]*100:.1f}% дисперсии)")

            if idx == 0:
                plt.title("Корреляционный круг переменных (по площадям пиков)")
            else:
                plt.title("Корреляционный круг переменных (по значениям пиков)")

            plt.xlim(-1.1, 1.1)
            plt.ylim(-1.1, 1.1)
            plt.grid(True)

            if idx == 1:
                plt.savefig('graphs/diagrams/circle_by_peaks.png', dpi = 600, bbox_inches = 'tight')
            else:
                plt.savefig('graphs/diagrams/circle_by_area.png', dpi = 600, bbox_inches = 'tight')

            plt.close()

        # PCA

        if pca_choise:

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
                plt.savefig('graphs/diagrams/pca_by_peaks.png', dpi = 600, bbox_inches = 'tight')
            else:
                plt.savefig('graphs/diagrams/pca_by_area.png', dpi = 600, bbox_inches = 'tight')

            plt.close()

        # hca

        if cluster:

            linked = linkage(table, method='ward', metric='euclidean')
            plt.figure(figsize=(15, 10))

            # задаём разные пороги для разных таблиц
            if idx == 1:
                color_threshold = 0.04
            else:
                color_threshold = 0.7

            dendro = dendrogram(
                linked,
                labels=table.index.to_list(),
                leaf_font_size=10,
                color_threshold=color_threshold,
                orientation='left'
            )

            # создаём DataFrame с кластерами

            cluster_labels = fcluster(linked, t=color_threshold, criterion='distance')
            df_clusters = pd.DataFrame({
                'Sample': table.index,
                'Cluster': cluster_labels
            }).set_index('Sample')

            # сортировка по номеру кластера
            df_clusters = df_clusters.sort_values(by='Cluster')

            # сохраняем результаты
            if idx == 1:
                df_clusters.to_csv('data/cluster_labels_peaks.csv')
                plt.title('Результаты иерархического кластерного анализа (по значениям пиков)', fontsize=22)
                plt.savefig('graphs/diagrams/dendrogram_by_peaks.png', dpi=600, bbox_inches='tight')
            else:
                df_clusters.to_csv('data/cluster_labels_area.csv')
                plt.title('Результаты иерархического кластерного анализа (по площадям пиков)', fontsize=22)
                plt.savefig('graphs/diagrams/dendrogram_by_area.png', dpi=600, bbox_inches='tight')

            plt.xlabel('Расстояние', fontsize=18)
            plt.ylabel('Объекты', fontsize=18)
            plt.tight_layout()
            plt.close()

if __name__ == '__main__':

    post_core(circle=False, pca_choise=False, cluster=True)

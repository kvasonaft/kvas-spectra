#### Импорт файлов

# Вектор, содержащий смысловые длины волн для ПЭТ-пластика
logic_wavelengths_PET <- c(3054, 2969, 2908, 1730, 1577, 1538, 1504, 1453, 1410, 1342, 1240, 1124, 1096, 1050, 972, 872, 848)

# Путь к папке для импорта файлов
path <- "/home/kvasonaft/Learning/analysis_of_spectra/pca_dataset"

# Получение списка файлов с расширением .dpt
files <- list.files(path, pattern = "\\.dpt$", full.names = TRUE)

library(readr)  # Пакет для чтения файлов

# Читаем все файлы и сохраняем их в один объект
data_list <- lapply(files, read_delim, delim = "\t", col_names = TRUE)

library(dplyr)

cultures <- tools::file_path_sans_ext(list.files(path = path))

# Присваиваем уникальные имена столбцам перед объединением
for (i in seq_along(data_list)) {
  colnames(data_list[[i]]) <- c("Wavelength", cultures[i])
}

# Присваиваем численные имена столбцам перед объединением
# numbers <- c(1:52)
# for (i in seq_along(data_list)) {
#   colnames(data_list[[i]]) <- c("Wavelength", numbers[i])
# }

# Объединяем все data.frames по Wavelength
merged <- Reduce(function(df1, df2) merge(df1, df2, by = "Wavelength", all = TRUE), data_list)

# Транспонирование итоговой таблицы

merged_t <- t(merged)
colnames(merged_t) <- logic_wavelengths_PET
PCA_df_pre <- as.data.frame(merged_t)
data_frame_main <- PCA_df_pre[-1,]

write.csv(data_frame_main, '/home/kvasonaft/Learning/spectra/data.csv', row.names = TRUE)

library(FactoMineR)

data_frame_main_scaled <- as.data.frame(scale(data_frame_main)) # Normalization

res.pca <- PCA (data_frame_main_scaled)

plot(res.pca)

##### Heatmap

library(corrplot)

# Вычисление корреляционной матрицы (по длинам волн)
cor_matrix <- cor(data_frame_main_scaled, method = "spearman")

cor_df <- as.data.frame(cor_matrix)
write.csv(cor_df, '/home/kvasonaft/Learning/spectra/correlation.csv', row.names = TRUE)

par(mar = c(6, 6, 6, 6))

corrplot(cor_matrix, 
         method = "color",
         type = "upper",
         tl.col = "black", tl.srt = 45,
         diag = TRUE,
         )

title('Тепловая карта изменений спектров по длинам волн', line = 7)

# Вычисление корреляционной матрицы (по культурам)

t_data_frame_main <- t(data_frame_main)
data_frame_main_t <- as.data.frame(t_data_frame_main)
data_frame_main_t_scaled <- as.data.frame(scale(data_frame_main_t))

cor_matrix <- cor(data_frame_main_t_scaled, method = "spearman")

corrplot(cor_matrix, 
         method = "color", # Цветные квадраты
         type = "upper",            # Только верхний треугольник
         order = "hclust",          # Упорядочить по кластерам
         #addCoef.col = "black",     # Добавить значения корреляции
         tl.col = "black", tl.srt = 45,  # Цвет и угол подписей
         diag = TRUE,              # Убрать диагональ
         )

# Иерархический кластерный анализ
matrix_scaled <- scale(data_frame_main)
dist_matrix <- dist(matrix_scaled, method = "euclidean")

hc <- hclust(dist_matrix, method = "ward.D2")
plot(hc,
     hang = -1)
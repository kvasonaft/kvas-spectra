culture <- "BM21PET3_1C"

export_path <- paste0("/home/kvasonaft/Documents/r_projects/Analysis of IR spectra/results/", culture, "_res/")
if (!dir.exists(export_path)) {
  dir.create(export_path)
}

export_pca <- paste0("/home/kvasonaft/Documents/r_projects/Analysis of IR spectra/pca_dataset/")

library(readr)
# Import
path <- paste0("/home/kvasonaft/Documents/r_projects/Analysis of IR spectra/spectra_dataset/", culture)
# Receiving .dpt files
files <- list.files(path, pattern = "\\.dpt$", full.names = TRUE)

# Saving all the data in one list
data_list <- lapply(files, read_delim, delim = "\t", col_names = FALSE)
# Vector of vital wavelengths
vital_wavelengths_PET <- c(3054, 2969, 2908, 1730, 1577, 1538, 1504, 1453, 1410, 1342, 1240, 1124, 1096, 1050, 972, 872, 848)

# Naming columns
for (i in 1:length(data_list)) {
  colnames(data_list[[i]]) <- c("Wavelength", "Absorbance")
}

#### Merging files
library(dplyr)
# Unique names
for (i in seq_along(data_list)) {
  colnames(data_list[[i]]) <- c("Wavelength", paste0("Absorbance_", i))
}
# Merging by Wavelength

merged_data <- Reduce(function(df1, df2) merge(df1, df2, by = "Wavelength", all = TRUE), data_list)

# Creating vectors of absorptions and wavelenghts
for (j in 1:length(data_list)) {
  if (j <= length(data_list)/2) {
    assign(paste0("absorbance_exp_", j), merged_data[j+1])
  }else{
    assign(paste0("absorbance_con_", j), merged_data[j+1])
  }
}
wavelengths <- merged_data$Wavelength

# Внешний цикл по файлам
for (n in 1:length(data_list)) {
  if (n <= length(data_list) / 2) {
    # Инициализация векторов для экспериментальных данных
    assign(paste0("peaks_exp_", n), numeric(16))
    assign(paste0("peaks_waves_exp_", n), numeric(16))
    assign(paste0("peaks_absorbance_exp_", n), numeric(16))
    
    absorbance_name <- paste0("absorbance_exp_", n)
    peaks_index_exp_name <- paste0("peaks_exp_", n)
    peaks_waves_exp_name <- paste0("peaks_waves_exp_", n)
    peaks_absorbance_exp_name <- paste0("peaks_absorbance_exp_", n)
    
    absorbance_data <- get(absorbance_name)[[1]]  # Извлекаем вектор из data.frame
    
    for (l in 1:length(vital_wavelengths_PET)) {
      # Выбираем диапазон длин волн (±20)
      wave_range <- wavelengths >= vital_wavelengths_PET[l] - 20 & 
        wavelengths <= vital_wavelengths_PET[l] + 20
      current_selected_waves <- wavelengths[wave_range]
      current_selected_absorbance <- absorbance_data[wave_range]  # Теперь работает как вектор
      
      # Находим индекс минимума в выбранном диапазоне
      peak_index <- which.min(current_selected_absorbance)
      
      # Сохраняем результаты с помощью assign
      assign(peaks_index_exp_name, replace(get(peaks_index_exp_name), l, peak_index))
      assign(peaks_waves_exp_name, replace(get(peaks_waves_exp_name), l, current_selected_waves[peak_index]))
      assign(peaks_absorbance_exp_name, replace(get(peaks_absorbance_exp_name), l, current_selected_absorbance[peak_index]))
    }
    
    library(ggplot2)
    
    # Создаем data frame для всего спектра
    spectrum_df <- data.frame(Wavelength = wavelengths, Absorbance = absorbance_data)  # Используем данные, а не имя
    
    # Создаем data frame для найденных минимумов
    peaks_df <- data.frame(
      Wavelength = get(peaks_waves_exp_name),  # Получаем значения вектора
      Absorbance = get(peaks_absorbance_exp_name)
    )
    
    # Создаем data frame для серых полос (диапазоны поиска)
    ranges_df <- data.frame(
      xmin = vital_wavelengths_PET - 20,
      xmax = vital_wavelengths_PET + 20,
      ymin = min(spectrum_df$Absorbance, na.rm = TRUE),  # Учитываем возможные NA
      ymax = max(spectrum_df$Absorbance, na.rm = TRUE),
      Label = vital_wavelengths_PET
    )
    
    # Определяем координаты для подписей (по центру полос)
    ranges_df$Label_x <- (ranges_df$xmin + ranges_df$xmax) / 2
    ranges_df$Label_y <- ranges_df$ymax + 0.02 * (ranges_df$ymax - ranges_df$ymin)  # Теперь числовые значения
    
    # Строим график
    graph <- ggplot() +
      # Серые полосы (диапазоны поиска)
      geom_rect(data = ranges_df, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax),
                fill = "green", alpha = 0.3) +
      # Линия спектра
      geom_line(data = spectrum_df, aes(x = Wavelength, y = Absorbance), color = "black") +
      # Точки минимумов
      geom_point(data = peaks_df, aes(x = Wavelength, y = Absorbance), color = "red", size = 3) +
      labs(title = paste0("Experimental peaks ", n),  # Динамическое название
           x = "Wavelength",
           y = "Absorbance") +
      theme_minimal()
    
    # Сохраняем график
    ggsave(paste0(export_path, culture, "_exp_graph_", n, ".png"), plot = graph, width = 8, height = 6)
    
  } else {
    # Инициализация векторов для контрольных данных
    assign(paste0("peaks_con_", n), numeric(16))
    assign(paste0("peaks_waves_con_", n), numeric(16))
    assign(paste0("peaks_absorbance_con_", n), numeric(16))
    
    absorbance_name <- paste0("absorbance_con_", n)
    peaks_index_con_name <- paste0("peaks_con_", n)
    peaks_waves_con_name <- paste0("peaks_waves_con_", n)
    peaks_absorbance_con_name <- paste0("peaks_absorbance_con_", n)
    
    absorbance_data <- get(absorbance_name)[[1]]  # Извлекаем вектор из data.frame
    
    for (l in 1:length(vital_wavelengths_PET)) {
      # Выбираем диапазон длин волн (±20)
      wave_range <- wavelengths >= vital_wavelengths_PET[l] - 20 & 
        wavelengths <= vital_wavelengths_PET[l] + 20
      current_selected_waves <- wavelengths[wave_range]
      current_selected_absorbance <- absorbance_data[wave_range]  # Теперь работает как вектор
      
      # Находим индекс минимума в выбранном диапазоне
      peak_index <- which.min(current_selected_absorbance)
      
      # Сохраняем результаты с помощью assign
      assign(peaks_index_con_name, replace(get(peaks_index_con_name), l, peak_index))
      assign(peaks_waves_con_name, replace(get(peaks_waves_con_name), l, current_selected_waves[peak_index]))
      assign(peaks_absorbance_con_name, replace(get(peaks_absorbance_con_name), l, current_selected_absorbance[peak_index]))
    }
    
    library(ggplot2)
    
    # Создаем data frame для всего спектра
    spectrum_df <- data.frame(Wavelength = wavelengths, Absorbance = absorbance_data)  # Используем данные, а не имя
    
    # Создаем data frame для найденных минимумов
    peaks_df <- data.frame(
      Wavelength = get(peaks_waves_con_name),  # Получаем значения вектора
      Absorbance = get(peaks_absorbance_con_name)
    )
    
    # Создаем data frame для серых полос (диапазоны поиска)
    ranges_df <- data.frame(
      xmin = vital_wavelengths_PET - 20,
      xmax = vital_wavelengths_PET + 20,
      ymin = min(spectrum_df$Absorbance, na.rm = TRUE),  # Учитываем возможные NA
      ymax = max(spectrum_df$Absorbance, na.rm = TRUE),
      Label = vital_wavelengths_PET
    )
    
    # Определяем координаты для подписей (по центру полос)
    ranges_df$Label_x <- (ranges_df$xmin + ranges_df$xmax) / 2
    ranges_df$Label_y <- ranges_df$ymax + 0.02 * (ranges_df$ymax - ranges_df$ymin)  # Теперь числовые значения
    
    # Строим график
    graph <- ggplot() +
      # Серые полосы (диапазоны поиска)
      geom_rect(data = ranges_df, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax),
                fill = "green", alpha = 0.3) +
      # Линия спектра
      geom_line(data = spectrum_df, aes(x = Wavelength, y = Absorbance), color = "black") +
      # Точки минимумов
      geom_point(data = peaks_df, aes(x = Wavelength, y = Absorbance), color = "red", size = 3) +
      labs(title = paste0("Control peaks ", n),  # Динамическое название
           x = "Wavelength",
           y = "Absorbance") +
      theme_minimal()
    
    # Сохраняем график
    ggsave(paste0(export_path, culture, "_con_graph_", n, ".png"), plot = graph, width = 8, height = 6)
    
  }
}

# Создание итоговой таблицы пиков
table_of_peaks <- data.frame(matrix(ncol = 0, nrow = length(vital_wavelengths_PET)))

for (k in 1:length(data_list)) {
  if (k <= length(data_list)/2) {
    wave_name <- paste0("peaks_waves_exp_", k)
    abs_name <- paste0("peaks_absorbance_exp_", k)
    col_wave <- paste0("Wavelength_exp_", k)
    col_abs <- paste0("Absorbance_exp_", k)
  } else {
    wave_name <- paste0("peaks_waves_con_", k)
    abs_name <- paste0("peaks_absorbance_con_", k)
    col_wave <- paste0("Wavelength_con_", k)
    col_abs <- paste0("Absorbance_con_", k)
  }
  
  table_of_peaks[[col_wave]] <- get(wave_name)
  table_of_peaks[[col_abs]] <- get(abs_name)
}

# Опционально: сохранить таблицу в файл
write.csv(table_of_peaks, paste0(export_path, culture, "_individual_peaks.csv"), row.names = FALSE)

# После всех предыдущих операций
result <- data.frame(Wavelength = vital_wavelengths_PET)

for (m in 1:length(data_list)) {
  if (m <= length(data_list)/2) {
    abs_name <- paste0("peaks_absorbance_exp_", m)
    col_abs <- paste0("Absorbance_exp_", m)
  } else {
    abs_name <- paste0("peaks_absorbance_con_", m)
    col_abs <- paste0("Absorbance_con_", m)
  }
  result[[col_abs]] <- get(abs_name)
}

# Опционально: сохранить таблицу
write.csv(result, paste0(export_path, culture, "_result.csv"), row.names = FALSE)

# После обработки спектров и создания peaks_absorbance_exp_*, peaks_absorbance_con_*
result_final <- data.frame(Wavelength = vital_wavelengths_PET)
for (w in 1:length(data_list)) {
  if (w <= length(data_list)/2) {
    abs_name <- paste0("peaks_absorbance_exp_", w)
    col_abs <- paste0("Absorbance_exp_", w)
  } else {
    abs_name <- paste0("peaks_absorbance_con_", w)
    col_abs <- paste0("Absorbance_con_", w)
  }
  result_final[[col_abs]] <- get(abs_name)
}

# Тест Манна-Уитни
results_wilcox <- data.frame(
  Wavelength = result_final$Wavelength,
  p_value = NA,
  Significant = NA
)

# Определение колонок для экспериментальной и контрольной групп
exp_cols <- grep("Absorbance_exp_", colnames(result_final), value = TRUE)
con_cols <- grep("Absorbance_con_", colnames(result_final), value = TRUE)

for (h in 1:nrow(result_final)) {
  # Извлечение всех значений для экспериментальной группы
  exp_group <- unlist(result_final[h, exp_cols])
  # Удаление NA значений, если такие есть
  exp_group <- exp_group[!is.na(exp_group)]
  
  # Извлечение всех значений для контрольной группы
  control_group <- unlist(result_final[h, con_cols])
  # Удаление NA значений, если такие есть
  control_group <- control_group[!is.na(control_group)]
  
  # Выполнение теста Манна-Уитни
  test_result <- wilcox.test(exp_group, control_group, exact = FALSE)$p.value
  results_wilcox$p_value[h] <- round(test_result, 3)
  results_wilcox$Significant[h] <- test_result < 0.05
}

print(results_wilcox)
write.csv(results_wilcox, paste0(export_path, culture, "_statistics.csv"), row.names = FALSE)

library(dplyr)

# Определение колонок для экспериментальной и контрольной групп
exp_cols <- grep("Absorbance_exp_", colnames(result), value = TRUE)
con_cols <- grep("Absorbance_con_", colnames(result), value = TRUE)

mean_result <- result %>%
  mutate(
    Mean_Exp = rowMeans(select(., all_of(exp_cols)), na.rm = TRUE),
    Mean_Con = rowMeans(select(., all_of(con_cols)), na.rm = TRUE)
  ) %>%
  select(Wavelength, Mean_Exp, Mean_Con)

difference_vector_pre <- abs(mean_result$Mean_Exp - mean_result$Mean_Con)
difference_vector <- round(difference_vector_pre, 4)

difference_dataframe <- data.frame(
  "Wavelength" = vital_wavelengths_PET,
  "Difference" = difference_vector
)

damage <- round(sum(difference_vector), 0)
write_delim(difference_dataframe, paste0(export_path, culture, " (", damage, ")", ".dpt"), delim = "\t")

library(tidyr)

# Преобразуем данные в длинный формат для ggplot
plot_data <- mean_result %>%
  mutate(Index = row_number()) %>%
  pivot_longer(cols = c(Mean_Exp, Mean_Con), names_to = "Group", values_to = "Value")

# Создаем позиции для столбцов с пробелами между парами
plot_data <- plot_data %>%
  mutate(Position = rep(1:17, each = 2) * 3 + rep(c(-0.5, 0.5), times = 17))

# Создаем гистограмму
hist_final <- ggplot(plot_data, aes(x = Position, y = Value, fill = Group)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9), width = 0.8) +
  scale_x_continuous(breaks = seq(3, 51, by = 3), labels = mean_result$Wavelength) +
  scale_fill_manual(values = c("Mean_Exp" = "blue", "Mean_Con" = "red")) +
  labs(x = "Wavelength", y = "Absorbance", title = "Histogram of Mean Absorbance Values") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
ggsave(paste0(export_path, culture, "_histogram.png"), plot = hist_final, width = 8, height = 6)

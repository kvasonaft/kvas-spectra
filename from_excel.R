library(openxlsx)
library(readr)

setwd("/home/kvasonaft/Documents/r_projects/Analysis of IR spectra/new_spectra")

# Укажите путь к вашему xlsx-файлу
file_path <- "/home/kvasonaft/Documents/r_projects/Analysis of IR spectra/river.xlsx"

# Получить список всех листов в файле
sheet_names <- getSheetNames(file_path)

# Функция для сохранения двух столбцов в файл .dpt
save_as_dpt <- function(data, file_name) {
  # .dpt файлы обычно используют табуляцию как разделитель и не имеют заголовков
  write_tsv(data, file_name, col_names = TRUE)
}

# Обработать каждый лист
for (sheet in sheet_names) {
  # Читаем данные из листа
  sheet_data <- read.xlsx(file_path, sheet = sheet)
  
  # Проверяем, что в листе есть хотя бы два столбца
  if (ncol(sheet_data) >= 2) {
    # Создаём имя файла на основе имени листа
    output_file <- paste0(sheet, ".dpt")
    
    # Выбираем первые два столбца
    two_columns <- sheet_data[, 1:2]
    
    # Сохраняем в .dpt
    save_as_dpt(two_columns, output_file)
    
    cat("Сохранено:", output_file, "\n")
  } else {
    cat("В листе", sheet, "меньше двух столбцов. Пропускаем.\n")
  }
}

cat("Обработка завершена!\n")
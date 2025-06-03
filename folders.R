library(readr)
path <- "/home/kvasonaft/Documents/r_projects/Analysis of IR spectra/spectra_dataset/"
all_folders <- list.dirs(path, full.names = FALSE, recursive = FALSE)
all_folders_col <- as.data.frame(all_folders)
write_delim(all_folders_col, "folders.txt", delim = "/t")

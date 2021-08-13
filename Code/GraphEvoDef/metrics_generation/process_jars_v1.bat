@echo "Processing" %1

SET jar_file_name=%1
SET uploaded_file=.\uploaded_files\%1
SET decompiled_files_folder=.\decompiled_files\%1
SET decompiled_files_class_folder=.\decompiled_files\%1\classes
SET decompiled_files_zip=%decompiled_files_folder%\%1
SET fernflower_path = .\utilities\fernflower.jar
SET jmetrics_path  = .\utilities\JSMAnalysis-JMetrics-d9b7378\jmetrics
SET jmetrics_reports_path  = .\utilities\JSMAnalysis-JMetrics-d9b7378\jmetrics\reports

SET current_directory = %CD%
SET decompiled_files_cd_folder=%CD%\decompiled_files\%1

md %decompiled_files_folder%
md %decompiled_files_class_folder%

copy %uploaded_file% %decompiled_files_class_folder%\

cd %decompiled_files_class_folder%

jar xf %jar_file_name%

cd %current_directory%

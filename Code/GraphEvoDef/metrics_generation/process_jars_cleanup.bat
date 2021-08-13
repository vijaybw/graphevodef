@echo "Processing" %1

SET jar_file_name=%1
SET processed_file=.\processed_files\%1.txt
SET uploaded_file=.\uploaded_files\%1
SET decompiled_files_folder=.\decompiled_files\%1

SET current_directory = %CD%
SET decompiled_files_cd_folder=%CD%\decompiled_files\%1

del %processed_file%

rmdir /s /q %decompiled_files_cd_folder%

del %uploaded_file%
@echo "Processing" %1

SET jar_file_name=%1
SET uploaded_file=.\uploaded_files\%1
SET processed_file=.\processed_files\%1.txt
SET decompiled_files_folder=.\decompiled_files\%1
SET decompiled_files_class_folder=decompiled_files\%1\classes
SET decompiled_files_zip=%decompiled_files_folder%\%1
SET fernflower_path = .\utilities\fernflower.jar
SET jmetrics_path  = .\utilities\JSMAnalysis-JMetrics-d9b7378\jmetrics
SET jmetrics_reports_path  = .\utilities\JSMAnalysis-JMetrics-d9b7378\jmetrics\reports
SET out_file_path = .\utilities\out.txt

SET current_directory = %cd%
SET decompiled_files_cd_folder=%CD%\decompiled_files\%1

cd metrics_generation
::copy C:\graphevodefect\fernflowertest\utilities\out.txt %decompiled_files_class_folder%\

cd .%current_directory%\%decompiled_files_class_folder%

for /F "delims=" %%a in ('dir /s /b') do (
     echo %%a | java -jar C:\graphevodefect\fernflowertest\utilities\runable-ckjm_ext-2.3.jar >> out.txt
)

REN out.txt %jar_file_name%.txt

move %jar_file_name%.txt ..

cd ..

move %jar_file_name%.txt ..

cd ..

move %jar_file_name%.txt ..

cd ..

move %jar_file_name%.txt %processed_file%
::cd %current_directory% %decompiled_files_folder%\

::for /f %a in ('dir /s /b') do echo %~fa >> myClasses.txt
::copy %uploaded_file% %decompiled_files_class_folder%\

::for /f %a in ('dir /s /b') do echo %~fa | java -jar C:\graphevodefect\fernflowertest\utilities\runable-ckjm_ext-2.3.jar >> out.txt
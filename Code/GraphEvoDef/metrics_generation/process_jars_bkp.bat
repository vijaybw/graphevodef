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

java -jar .\utilities\fernflower.jar %uploaded_file% %decompiled_files_folder%

cd %decompiled_files_folder%

jar xf %jar_file_name%

REN *.jar *.jar.zip

cd ../..

java -jar .\utilities\ck-0.6.3-SNAPSHOT-jar-with-dependencies.jar %decompiled_files_folder%

move class.csv %decompiled_files_folder%
move field.csv %decompiled_files_folder%
move method.csv %decompiled_files_folder%
move variable.csv %decompiled_files_folder%

cd .\utilities\JSMAnalysis-JMetrics-d9b7378\jmetrics

gradlew run --args="-p %decompiled_files_cd_folder% -t source -o %decompiled_files_cd_folder%"

cd ../../..
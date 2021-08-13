import os
app_path = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY ='rakan'
    WORKSPACE_LOCATION = os.path.join(app_path, 'static/projects')
    UPLOAD_FOLDER = os.path.join(app_path, 'upload')
    INPUT_JAR_FOLDER = os.path.join(app_path, 'input_jars')
    OUTPUT_CGS_FOLDER = os.path.join(app_path, 'output_cgs')
    KPI_DATA_FOLDER = os.path.join(app_path, 'kpi_data')
    KPI_GEN_FOLDER = os.path.join(app_path, 'metrics_generation')
    KPI_GEN_PROCESSED_FOLDER = os.path.join(app_path, 'metrics_generation', 'processed_files')
    KPI_GEN_UPLOAD_FOLDER = os.path.join(KPI_GEN_FOLDER, 'uploaded_files')
    BUG_DATASET_FILE = os.path.join(os.path.join(app_path, 'data'), 'all-modfd.csv')
    BUG_DATASET_FILE2 = os.path.join(os.path.join(app_path, 'data'), 'all-modfdbugsv2.csv')
    PROJECT_NAME = ""
    PROJECT_LOCATION = ""
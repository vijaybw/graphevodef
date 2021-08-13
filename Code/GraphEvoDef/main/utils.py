
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Rakan Alanazi, Vijay Walunj
"""

from werkzeug.utils import secure_filename
from flask import current_app
import os 

def save_file(uploaded_file,project_name,last_file_flag=False):
    filename = secure_filename(uploaded_file.filename) 
    _, f_ext = os.path.splitext(filename)
    prediction_fn = str(project_name) + f_ext
    uploaded_file.save(os.path.join(current_app.config['PROJECT_LOCATION'],prediction_fn))  
    if last_file_flag:
        return prediction_fn


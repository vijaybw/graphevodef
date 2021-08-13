# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Vijay Walunj
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError

import os
from flask import current_app

class NewProjectForm(FlaskForm):
    project_name = StringField('Project Name',
                           validators=[DataRequired(), Length(min=2, max=50)])
    project_file = MultipleFileField('Project Files', validators=[FileAllowed(['edgelist','txt'])],render_kw={'multiple': True, 'style':'display: none'})
    submit = SubmitField('Upload')

    def validate_project_name(self, project_name):
        projects = os.listdir(current_app.config['WORKSPACE_LOCATION'])   # Get all projects
        if project_name.data in projects:
            raise ValidationError('That project name is taken. Please choose a different one.')

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Rakan Alanazi, Vijay Walunj
"""
import flask
from flask import (render_template,url_for,
                   redirect, request, jsonify, Blueprint,current_app)
from werkzeug.utils import secure_filename

from main.CallGraphGeneration import process_jar_files
from main.forms import NewProjectForm
from graph.schema import graph_builder, parse_edgelist, parse_nodes_text, parse_edgelist_text
import main.utils as util
import os

main = Blueprint('main', __name__)

@main.route("/",methods=['GET', 'POST'])
def landing():
    temp_proj = "dora"
    current_app.config['PROJECT_NAME'] = temp_proj
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.root_path, 'static/projects',
                                                          temp_proj)
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.config['PROJECT_LOCATION'], "one1")
    return redirect(url_for('main.home',name=temp_proj,state='True'))

@main.route("/uploader",methods=['GET', 'POST'])
def loadproject():
    form = NewProjectForm()
    current_app.config['PROJECT_NAME'] = form.project_name.data
    print("X:" + str(current_app.config['PROJECT_NAME']) )
    #if current_app.config['PROJECT_NAME'] != None and current_app.config['PROJECT_NAME'] != "dora" :
    jar_files_uploaded = False
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.root_path, 'static/projects', current_app.config['PROJECT_NAME'])
    if not os.path.exists(current_app.config['PROJECT_LOCATION']):
            os.makedirs(current_app.config['PROJECT_LOCATION'])
    else:
        list_dir = os.listdir(current_app.config['PROJECT_LOCATION'])
        list_dir = [f.lower() for f in list_dir]
        list_dir = sorted(list_dir)
        current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.config['PROJECT_LOCATION'],list_dir[0])
        graph_url = os.path.join(current_app.config['PROJECT_LOCATION'], 'diffdata.json')
        print('GRapho',graph_url)
        if not os.path.exists(graph_url):
            print("NOT EXITED",graph_url)
            redirect(url_for('main.home',name=current_app.config['PROJECT_NAME'],state='True'))
        else:
            print("EXITED",graph_url)
            redirect(url_for('main.home',name=current_app.config['PROJECT_NAME'],state='Loaded'))

    files_filenames = []
    project_version_path = ""
    files = request.files.getlist("project_file[]")
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.root_path, 'static/projects',
                                                              current_app.config['PROJECT_NAME'])
    if files.__len__() > 0:
            for file in files:
                file_filename = secure_filename(file.filename)
                if file_filename == '':
                    #Break when no files to process
                    break

                substring = ".jar"

                if substring in str(file_filename):
                    jar_files_uploaded = True

                file_name, f_ext = os.path.splitext(file_filename)
                prediction_fn = str(current_app.config['PROJECT_NAME']) + f_ext

                project_version_path = os.path.join(current_app.config['PROJECT_LOCATION'], file_name)
                if jar_files_uploaded:
                    # project_version_path = current_app.config['PROJECT_LOCATION']
                    prediction_fn = file_name + f_ext
                if not os.path.exists(project_version_path):
                    os.makedirs(project_version_path)
                file.save(os.path.join(project_version_path, prediction_fn))
                files_filenames.append(file_name)

            if jar_files_uploaded:
                if process_jar_files(project_name=(current_app.config['PROJECT_NAME']),project_path=(current_app.config['PROJECT_LOCATION'])):
                    print("Files Processed Succcessfully")

            previous_graph = None
            previous_nodesList = None
            previos_edgeList = None
            for file_name in files_filenames:
                project_version_path = os.path.join(current_app.config['PROJECT_LOCATION'], file_name)

                previous_graph = graph_builder(current_app.config['PROJECT_NAME'], file_name, project_version_path, previous_graph, previous_nodesList, previos_edgeList)

                previous_nodesList = parse_nodes_text(project_version_path)
                previos_edgeList = parse_edgelist_text(project_version_path)

            current_app.config['PROJECT_LOCATION'] = project_version_path

    return redirect(url_for('main.home',name=current_app.config['PROJECT_NAME'],state='True'))

    
@main.route("/project/<name>/<state>",methods=['GET', 'POST'])
def home(name,state=None):

    current_app.config['PROJECT_NAME'] = name
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.root_path, 'static/projects', current_app.config['PROJECT_NAME'])
    list_dir = os.listdir(current_app.config['PROJECT_LOCATION'])
    list_dir = [f.lower() for f in list_dir]
    list_dir = sorted(list_dir,reverse=True)
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.config['PROJECT_LOCATION'],list_dir[0])

    return render_template('home.html',name=name,len = len(list_dir), versions= list_dir,state=state)

@main.route("/graph/<project>",methods=['GET', 'POST'])
def graph_data(project):
    graph_url = os.path.join(current_app.config['PROJECT_LOCATION'], 'diffdata.json')
    if not os.path.exists(graph_url):
        graph_url = os.path.join(current_app.config['PROJECT_LOCATION'], 'data.json')

    import json

    print(str(project) + ":" + str(graph_url))
    if request.method == 'POST':
        data = request.get_json()
        with open(graph_url, 'w') as f:
            json.dump(data, f)
        return ""

    elif request.method == 'GET':

        json_data = open(graph_url,encoding='utf-8', errors='ignore')
        graph = json.load(json_data, strict=False)
        graph = jsonify(graph)
        return graph

@main.route("/graph/<project>/<version>",methods=['GET', 'POST'])
def graph_data_version(project, version):
    current_app.config['PROJECT_LOCATION'] = current_app.config['PROJECT_LOCATION'].rsplit('\\', 1)[0]
    current_app.config['PROJECT_LOCATION'] = os.path.join(current_app.config['PROJECT_LOCATION'], version)
    graph_url = os.path.join(current_app.config['PROJECT_LOCATION'], 'diffdata.json')
    if not os.path.exists(graph_url):
        graph_url = os.path.join(current_app.config['PROJECT_LOCATION'], 'data.json')

    print(str(project) + ":" + str(version) + ":" + str(graph_url))
    import json

    if request.method == 'POST':
        data = request.get_json()
        with open(graph_url, 'w') as f:
            json.dump(data, f)
        return ""

    elif request.method == 'GET':

        json_data = open(graph_url,encoding='utf-8', errors='ignore')
        graph = json.load(json_data, strict=False)
        graph = jsonify(graph)
        return graph
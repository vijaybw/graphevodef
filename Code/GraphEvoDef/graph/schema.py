#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2021 - Vijay Walunj
"""
import csv
from collections import namedtuple
from random import randrange

from flask import current_app, Blueprint
import networkx as nx
import json
import os
from pathlib import Path
from main.datacore import SoftwareMetric
graph = Blueprint('graph', __name__)


def graph_builder(project_name, version_name, current_project_version_path, previous_version_graph = None, previous_nodesList = None, previous_edgesList = None):
    G = parse_edgelist(current_project_version_path)
    N = parse_nodes(current_project_version_path)
    T = parse_nodes_text(current_project_version_path)
    E = parse_edgelist_text(current_project_version_path)
    data_file_path = Path(current_project_version_path, version_name + '.metrics')
    data = []
    # with open(data_file_path) as f:
    #     reader = csv.reader(f)
    #     Data = namedtuple("Data", next(reader))
    #     data = [Data(*r) for r in reader]

    with open(data_file_path, "r") as file:
        data = file.read()

    data = data.strip(' ').split('\n')

    list_of_classes = []

    tmetrics = []
    first_line = True
    for cdata in data:
        if not first_line and not cdata.__contains__('$'):
            temp_c = None
            tmetrics = cdata.strip(' ').split(',')
            if tmetrics.__len__() == 25:
                temp_c = SoftwareMetric(tmetrics[0], tmetrics[1], tmetrics[2],
                                        tmetrics[3], tmetrics[4], tmetrics[5], tmetrics[6], tmetrics[7],
                                        tmetrics[8], tmetrics[9],
                                        tmetrics[10], tmetrics[11], tmetrics[12], tmetrics[13], tmetrics[14],
                                        tmetrics[15],
                                        tmetrics[16], tmetrics[17], tmetrics[18], tmetrics[19], tmetrics[20], tmetrics[21], tmetrics[24])
                temp_c.add_portrait_metrics(tmetrics[22],tmetrics[23])
                list_of_classes.append(temp_c)
        first_line = False
    print(data)

    save_call_graph(G, N, list_of_classes, current_project_version_path, previous_version_graph, T, E, previous_edgesList, previous_nodesList)
    return G

def parse_edgelist(project_version_path):
    get_edgelist_file = [x for x in os.listdir(project_version_path)
                         if x.endswith('.edgelist')][0]
    edgelist = open(os.path.join(project_version_path,
                                 get_edgelist_file), 'rb')
    G = nx.read_edgelist(edgelist, create_using=nx.DiGraph)
    edgelist.close()
    return G

def parse_edgelist_text(project_version_path):
    get_edgelist_file = [x for x in os.listdir(project_version_path)
                         if x.endswith('.edgelist')][0]
    get_nodelist_file = [x for x in os.listdir(project_version_path)
                         if x.endswith('.nodes')][0]

    d={}
    with open(os.path.join(project_version_path,
                           get_nodelist_file), 'rb') as f:
        for line in f:
            (key, val) = line.split()
            d[int(key)] = str(val)
    strlist = []
    with open(os.path.join(project_version_path,
                           get_edgelist_file), 'rb') as f:
        for line in f:
            (onen, twon) = line.split()
            strlist.append(d[int(onen)].replace("b'","").replace("'","") + "," + d[int(twon)].replace("b'","").replace("'",""))

    return strlist

def parse_nodes(project_version_path):
    get_edgelist_file = [x for x in os.listdir(project_version_path)
                         if x.endswith('.nodes')][0]
    d={}
    with open(os.path.join(project_version_path,
                           get_edgelist_file), 'rb') as f:
        for line in f:
            (key, val) = line.split()
            d[int(key)] = str(val)

    return d

def parse_nodes_text(project_version_path):
    get_edgelist_file = [x for x in os.listdir(project_version_path)
                         if x.endswith('.nodes')][0]
    names = []
    with open(os.path.join(project_version_path,
                           get_edgelist_file), 'rb') as f:
        for line in f:
            (key, val) = line.split()
            names.append(str(val).replace("b'","").replace("'",""))

    return names
def save_call_graph(GraphObj, nodeslist, data, current_project_version_path, previous_version_graph = None, T = None, E = None, previous_edgesList = None, previous_nodesList = None):
    (nodes, edges) = graph_tojson(GraphObj, nodeslist, data)
    write_call_graph(GraphObj, nodes, edges, current_project_version_path)
    if previous_version_graph is not None:
        (nodes, edges) = diff_graph_tojson(GraphObj, nodeslist, data, previous_version_graph, T, E, previous_edgesList, previous_nodesList)
        write_call_graph(GraphObj, nodes, edges, current_project_version_path, "diff")

def write_call_graph(
        graph,
        nodes,
        edges,
        graph_filepath,
        diff_text = ''
):
    graph_attr = {}
    graph_attr['nodes'] = nodes
    graph_attr['edges'] = edges

    nx.write_gml(graph, graph_filepath + '/' + diff_text + 'Graph.gml')
    outfile = open(graph_filepath + '/' + diff_text + 'data.json', 'w')
    json.dump(graph_attr, outfile)
    outfile.close()

def graph_tojson(graph,nodeslist, data):
    all_nodes = list()
    all_edges = list()

    for node in graph.nodes():
        full_name = nodeslist[int(node)][2:][:-1]
        class_name = nodeslist[int(node)][2:][:-1].split(":")[0]
        func_name = nodeslist[int(node)][2:][:-1].split(":")[1]
        x = {
            'id': full_name,
            'title': full_name,
            'label': func_name,
            'shape': 'dot',
            'group': 'blue',
            'customone': randrange(10)
        }
        kpis = {}
        kpis = get_kpi_for_class(class_name, data)
        x.update(kpis)
        if 'DEFECT_CNT' in x:
            if float(x['DEFECT_CNT']) > 0:
                if int(x['DEFECT_CNT']) >= 3:
                    x['group'] = 'red'
                    print("red " + class_name + " " + str(float(x['DEFECT_CNT'])))
                elif int(x['DEFECT_CNT']) == 1:
                    x['group'] = 'red'
                    print("orange " + class_name + " " + str(float(x['DEFECT_CNT'])))
                else:
                    x['group'] = 'blue'
        else:
            x['group'] = 'blue'

        all_nodes.append(x)
        for adj in list(graph.successors(node)):
            y = {
                'from': nodeslist[int(node)].replace("b'","").replace("'",""),
                'to': nodeslist[int(adj)].replace("b'","").replace("'",""),
                'arrows': 'to'
            }
            all_edges.append(y)
    return (all_nodes, all_edges)

def diff_graph_tojson(current_graph, nodeslist, data, previous_graph = None, T = None, E = None, previous_edgesList = None, previous_nodesList = None):
    current_all_nodes = list()
    current_all_edges = list()

    count_of_nodes_total = 0
    count_of_nodes_in_previous = 0
    for current_graph_node in current_graph.nodes():
        color = 'blue'
        count_of_nodes_total += 1
        full_name = nodeslist[int(current_graph_node)][2:][:-1]

        if str(full_name) in previous_nodesList:
            count_of_nodes_in_previous += 1
            color = 'lightblue'


        class_name = nodeslist[int(current_graph_node)][2:][:-1].split(":")[0]
        func_name = nodeslist[int(current_graph_node)][2:][:-1].split(":")[1]

        x = {
            'id': full_name,
            'title': full_name,
            'label': func_name,
            'shape': 'dot',
            'group': color,
            'customone': randrange(10)
        }
        kpis = {}
        kpis = get_kpi_for_class(class_name, data)
        x.update(kpis)

        if 'DEFECT_CNT' in x:
            if float(x['DEFECT_CNT']) > 0:
                if int(x['DEFECT_CNT']) >= 3:
                    x['group'] = 'red'
                    if str(full_name) in previous_nodesList:
                        x['group'] = 'lightred'
                    print("red " + class_name + " " + str(float(x['DEFECT_CNT'])))
                elif int(x['DEFECT_CNT']) == 1:
                    x['group'] = 'red'
                    if str(full_name) in previous_nodesList:
                        x['group'] = 'lightred'
                    print("orange " + class_name + " " + str(float(x['DEFECT_CNT'])))
                else:
                    x['group'] = 'blue'
        else:
            x['group'] = 'blue'

        current_all_nodes.append(x)
        for current_graph_adj in list(current_graph.successors(current_graph_node)):
            color = 'blue'
            fromtxt = nodeslist[int(current_graph_node)].replace("b'","").replace("'","")
            totext =  nodeslist[int(current_graph_adj)].replace("b'","").replace("'","")
            fulltxt = fromtxt + "," + totext
            if fulltxt in previous_edgesList:
                color = 'lightblue'
            y = {
                'from': nodeslist[int(current_graph_node)].replace("b'","").replace("'",""),
                'to': nodeslist[int(current_graph_adj)].replace("b'","").replace("'",""),
            }
            current_all_edges.append(y)
    print("current" + str(count_of_nodes_total) + "added" + str(count_of_nodes_in_previous))
    return (current_all_nodes, current_all_edges)


def get_kpi_for_class(function_name, data):
    return_dict = {}
    for s in data:
        if s.CLASS_NAME == function_name:
            return_dict = vars(s)
            return return_dict
    print(function_name)
    return return_dict
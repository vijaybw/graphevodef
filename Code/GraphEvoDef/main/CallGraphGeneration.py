# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Vijay Walunj
"""

import csv
import shutil
import constant
import subprocess
from pathlib import Path
from config import Config
from flask import current_app
from main.datacore import SoftwareMetric
import pandas as pd
import csv
import os

def process_jar_files(project_name, project_path):
    from pathlib import Path
    pathlist = Path(project_path).rglob('*.jar')
    list_of_jars = []
    count_of_jars = 0
    import os

    #Clear input_jars folder before use
    files = Path(Config.INPUT_JAR_FOLDER).glob('*')
    for f in files:
        os.remove(f)
    files = Path(Config.OUTPUT_CGS_FOLDER).glob('*')
    for f in files:
        os.remove(f)

    for path in pathlist:

         jar_file_path, f_ext = os.path.splitext(path)
         head, file_name = os.path.split(jar_file_path)
         list_of_jars.append(file_name + f_ext)
         project_version_path = os.path.join(project_path, file_name)
         file_path = os.path.join(project_version_path, file_name + f_ext)
         # Move a file from the directory d1 to d2
         shutil.move(file_path, Config.INPUT_JAR_FOLDER)
         count_of_jars = count_of_jars + 1

    args = []
    args.append(r"java")
    args.append("-jar")
    args.append(constant.JAR_FILE)
    args.append(count_of_jars)
    args.extend(list_of_jars)

    args_str= ""
    for i in args:
        if args_str.__len__() == 0:
            args_str = str(i)
        else:
            args_str = args_str + " " + str(i)

    import subprocess
    def run_command(command):
        p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
        p.wait()
        return iter(p.stdout.readline, b'')


    for output_line in run_command(args_str):
        print(output_line)

    for file_name in list_of_jars:
        project_version_path = os.path.join(project_path, os.path.splitext(file_name)[0])
        output_cg_path = constant.OUTPUT_CALLGRAPHS_FOLDER + "/" + os.path.splitext(file_name)[0] + "-callgraphNumbers.txt"
        edgelist_temp_path = Path(constant.INPUT_CALLGRAPHS_FOLDER, project_name + '--' +os.path.splitext(file_name)[0] + '-callgraphNumbers.txt')
        edgelist_path = project_version_path + "/" + os.path.splitext(file_name)[0] + ".edgelist"

        output_cg_nodemapping_path = constant.OUTPUT_CALLGRAPHS_FOLDER + "/" + os.path.splitext(file_name)[
            0] + "-callgraph.txt"
        nodemapping_path = project_version_path + "/" + os.path.splitext(file_name)[0] + ".nodes"
        # Move a file from the directory d1 to d2
        shutil.copy(output_cg_path, edgelist_temp_path)
        shutil.move(output_cg_path, edgelist_path)
        shutil.move(output_cg_nodemapping_path, nodemapping_path)

    # creating list
    list_of_SoftwareMetrics = []
    last_file_name = ''
    first_version_processed = False
    prior_version_processed = ''
    prior_version_processed_number = ''
    prior_version_processed_classes = []
    old_dfbugs = pd.read_csv(Config.BUG_DATASET_FILE2, dtype=str, names=['PROJECT_VERSION','CLASS_NAME','DEFECT_CNT'])

    last_jar_metrics = []
    current_jar_metrics = []
    for file_name in list_of_jars:
        from pathlib import Path
        project_version_path = os.path.join(project_path, os.path.splitext(file_name)[0])
        project_version_software_metrics_path = project_version_path + "/" + os.path.splitext(file_name)[0] + ".metrics"

        shutil.copy(Path(Config.INPUT_JAR_FOLDER,file_name), Config.KPI_GEN_UPLOAD_FOLDER)
        subprocess.call([os.path.join(current_app.root_path, 'metrics_generation','process_jars.bat'), file_name],cwd=os.path.join(current_app.root_path, 'metrics_generation'))
        subprocess.call([os.path.join(current_app.root_path, 'metrics_generation','process_jars_next.bat'), file_name],cwd=os.path.join(current_app.root_path, 'metrics_generation'))
        subprocess.call([os.path.join(current_app.root_path, 'metrics_generation','process_jars_next2.bat'), file_name],cwd=os.path.join(current_app.root_path, 'metrics_generation'))

        last_jar_metrics = current_jar_metrics
        current_jar_metrics = []

        if os.path.exists(Path(Config.KPI_GEN_PROCESSED_FOLDER, file_name + ".txt")):

            try:
                metrics_file = open(Path(Config.KPI_GEN_PROCESSED_FOLDER, file_name + ".txt"), "r")
                tmetrics = []
                current_max_cc = 0
                totalcc = 0
                totalmethods = 0

                for aline in metrics_file:
                    aline = aline.rstrip('\n')
                    if aline.split(' ').__len__() == 19:
                        tmetrics = aline.split(' ')
                        tmetrics[-1] = tmetrics[-1].replace('\n','')
                    elif aline.startswith(' ~'):
                        totalmethods = totalmethods + 1
                        totalcc = totalcc + int(aline.split(' ')[-1].replace('\n',''))
                        if current_max_cc < int(aline.split(' ')[-1].replace('\n','')):
                            current_max_cc = int(aline.split(' ')[-1].replace('\n',''))
                    elif aline == '':
                        if int(totalmethods) > 0:
                            tmetrics.append(int(totalcc / totalmethods))
                        else:
                            tmetrics.append(int(0))
                        tmetrics.append(current_max_cc)

                        sw_version = file_name
                        class_nm = tmetrics[0]
                        if class_nm.__contains__("org.apache.camel.Message"):
                            cf1 = 1
                        new_df = old_dfbugs[((old_dfbugs['PROJECT_VERSION'] == sw_version.replace(".jar","")) & (old_dfbugs['CLASS_NAME'] == class_nm))]

                        strc = class_nm

                        defect_count = 0
                        try:
                            defect_count = new_df['DEFECT_CNT'].values[0]
                        except IndexError:
                            defect_count = 0

                        if str(strc).__contains__('$') and defect_count == 0:
                            for x in range(35):
                                searchk = "$" + str(35-x)
                                if(str(strc).__contains__(searchk)):
                                    # print(strc)
                                    strc = strc.replace(searchk,'')
                                    break
                            if str(strc).__contains__('$'):
                                strc = strc.replace('$','')
                            if str(strc).__contains__('$'):
                                strc = strc.replace('$','')
                            if str(strc).__contains__('$'):
                                strc = strc.replace('$','')
                            if str(strc).__contains__('$'):
                                strc = strc.replace('$','')

                            new_df = old_dfbugs[((old_dfbugs['PROJECT_VERSION'] == sw_version.replace(".jar","")) & (old_dfbugs['CLASS_NAME'] == strc))]

                            try:
                                defect_count = new_df['DEFECT_CNT'].values[0]
                            except IndexError:
                                defect_count = 0

                        print(str(tmetrics[0]) + str(tmetrics[1]) + str(tmetrics[2]) + str(tmetrics[3]) + str(
                            tmetrics[4]) + str(tmetrics[5]) + str(tmetrics[6]) + str(tmetrics[7]) + str(
                            tmetrics[8]) + str(tmetrics[9]) +
                              str(tmetrics[10]) + str(tmetrics[11]) + str(tmetrics[12]) + str(tmetrics[13]) + str(
                            tmetrics[14]) + str(tmetrics[15]) +
                              str(tmetrics[16]) + str(tmetrics[17]) + str(tmetrics[18]) + str(tmetrics[19]) + str(
                            tmetrics[20]) + str(defect_count))
                        try:
                            current_jar_metrics.append(SoftwareMetric(project_name, tmetrics[0],tmetrics[1],tmetrics[2],
                                tmetrics[3],tmetrics[4],tmetrics[5],tmetrics[6],tmetrics[7],tmetrics[8],tmetrics[9],
                                tmetrics[10],tmetrics[11],tmetrics[12],tmetrics[13],tmetrics[14],tmetrics[15],
                                tmetrics[16],tmetrics[17],tmetrics[18],tmetrics[19],tmetrics[20], defect_count))
                        finally:
                            print("Error ocurred.")
                        #intialize fields for next class
                        totalcc - 0
                        totalmethods = 0
                        current_max_cc = 0
                        tmetrics = []
                # try:
                #     import csv
                #     with open(project_version_software_metrics_path, 'w', newline='') as f:
                #         writer = csv.writer(f)
                #         writer.writerow(['PROJECT_NAME,CLASS_NAME,WMC,DIT,NOC,CBO,RFC,LCOM,Ca,Ce,NPM,LCOM3,LOC,DAM,MOA,MFA,CAM,IC,CBM,AMC,AVG_CC,MAX_CC'])
                #         for item in current_jar_metrics:
                #             writer.writerow([item.PROJECT_NAME, item.CLASS_NAME, item.WMC, item.DIT, item.NOC,
                #                 item.CBO, item.RFC, item.LCOM, item.Ca, item.Ce, item.NPM, item.LCOM3,item.LOC,
                #                 item.DAM, item.MOA, item.MFA, item.CAM, item.IC, item.CBM, item.AMC,
                #                 item.AVG_CC, item.MAX_CC])
                # except BaseException as e:
                #     print('BaseException:', project_version_software_metrics_path)

            finally:
                metrics_file.close()


        subprocess.call(
            [os.path.join(current_app.root_path, 'metrics_generation', 'process_jars_cleanup.bat'), file_name],
            cwd=os.path.join(current_app.root_path, 'metrics_generation'))

        application_name = project_name
        application_version = os.path.splitext(file_name)[0]

        nodemapping_path = Path(project_version_path, os.path.splitext(file_name)[0] + ".nodes")
        current_edgelist_path = Path(project_version_path, os.path.splitext(file_name)[0] + ".edgelist")

        #Read Nodes List
        callgraph_methods_file = open(nodemapping_path,'r')
        callgraph_methods_file_lines = callgraph_methods_file.readlines()
        #Read edges between the nodes.
        callgraph_methods_ids_file = open(current_edgelist_path,'r')
        callgraph_methods_file_ids_lines = callgraph_methods_ids_file.readlines()

        process_version(application_name + '--' + application_version, callgraph_methods_file_lines,
                        callgraph_methods_file_ids_lines)
        print("Processed " + application_name + '--' + application_version)

        # driver code
        current_version_processed = ''
        current_version_processed_number = ''
        current_version_processed_classes = []
        import csv

        current_version_processed = application_name + '--' + application_version
        current_version_processed_number = application_version

        nodemapping_path = Path(project_version_path, os.path.splitext(file_name)[0] + ".nodes")
        current_edgelist_path = Path(project_version_path, os.path.splitext(file_name)[0] + ".edgelist")

        callgraph_methods_file = open(nodemapping_path,'r')
        list_of_methods = callgraph_methods_file.readlines()

        # intilize a null list
        list_of_classes = []

        # traverse for all elements
        for x in list_of_methods:
            # extract class name from full qualified name
            x = x.split(' ')[1].split(':')[0]
            # check if exists in list_of_classes or not
            if x not in list_of_classes:
                list_of_classes.append(x)
        # removing duplicated in case
        list_of_classes = list(dict.fromkeys(list_of_classes))
        current_version_processed_classes = list_of_classes

        # loop over list of classes
        from os import listdir
        from os.path import isfile, join

        onlyfiles = [f for f in listdir(constant.OUTPUT) if isfile(join(constant.OUTPUT, f))]

        # filter the methods which belong to particular class
        matching_cgs_files = [s for s in onlyfiles if application_version in s]
        matching_methods_ids = []

        from pathlib import Path
        cwd = os.getcwd()
        script_path = Path(cwd, "portrait_divergence.py").as_posix()
        script_parameters = Path("-d --weighted=strength").as_posix()

        with open(Path(constant.OUTPUT_CSV, current_version_processed + '-network_portrait.csv'), 'w',
                  newline='') as csvfile:
            fieldnames = ['class_name', 'new', 'portrait']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            if prior_version_processed == '':
                for cgs in matching_cgs_files:
                    new_one = 1
                    class_name_in_file = cgs.split("--")[2].replace(".txt", "")
                    first = current_edgelist_path
                    second = Path(constant.OUTPUT, cgs)

                    filenamef = Path(cwd, first).as_posix()
                    filenames = Path(cwd, second).as_posix()

                    import sys

                    calculated_portrait = os.popen(
                        sys.executable + ' ' + script_path + ' ' + script_parameters + ' ' + filenamef + ' ' + filenames).readlines()
                    calculated_portraittext = ""
                    for ln in calculated_portrait:
                        calculated_portraittext = calculated_portraittext + ln.rstrip('\n')

                    for s in current_jar_metrics:
                        if s.CLASS_NAME == class_name_in_file:
                            s.add_portrait_metrics(new_one, calculated_portraittext)
                    writer.writerow(
                        {'class_name': class_name_in_file, 'new': new_one, 'portrait': calculated_portraittext})
                    # print(current_version_processed + " " +  class_name_in_file + " " + calculated_portraittext)
            else:
                for cgs in matching_cgs_files:
                    class_name_in_file = cgs.split("--")[2].replace(".txt", "")
                    from pathlib import Path
                    if prior_version_processed_classes.count(str(class_name_in_file)) > 0:
                        new_one = "0"
                        first = Path(constant.OUTPUT, cgs.replace(application_version,prior_version_processed_number))
                    else:
                        new_one = "1"
                        first = Path(constant.INPUT_CALLGRAPHS_FOLDER, current_version_processed + '-callgraphNumbers.txt')
                    from pathlib import Path
                    second = Path(constant.OUTPUT, cgs)

                    filenamef = Path(cwd, first).as_posix()
                    filenames = Path(cwd, second).as_posix()

                    import sys
                    calculated_portrait = os.popen(
                        sys.executable + ' ' + script_path + ' ' + script_parameters + ' ' + filenamef + ' ' + filenames).readlines()
                    calculated_portraittext = ""
                    for ln in calculated_portrait:
                        calculated_portraittext = calculated_portraittext + ln.rstrip('\n')

                    for s in current_jar_metrics:
                        if s.CLASS_NAME == class_name_in_file:
                            s.add_portrait_metrics(new_one, calculated_portraittext)
                    writer.writerow(
                        {'class_name': class_name_in_file, 'new': new_one, 'portrait': calculated_portraittext})

        if current_jar_metrics.__len__() > 0:
            try:
                import csv
                with open(project_version_software_metrics_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    fields = ["PROJECT_NAME","CLASS_NAME","WMC","DIT","NOC","CBO","RFC","LCOM","Ca","Ce","NPM","LCOM3","LOC","DAM","MOA","MFA","CAM","IC","CBM","AMC","AVG_CC","MAX_CC","NEWONE","PORTRAIT","DEFECT_CNT"]
                    writer.writerow(fields)
                    for item in current_jar_metrics:

                        try:
                            wmc = item.WMC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            wmc = None
                        try:
                            dit = item.DIT
                        except (AttributeError, IndexError, ValueError, TypeError):
                            dit = None
                        try:
                            noc = item.NOC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            noc = None
                        try:
                            cbo = item.CBO
                        except (AttributeError, IndexError, ValueError, TypeError):
                            cbo = None
                        try:
                            rfc =  item.RFC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            rfc = None
                        try:
                            lcom = item.LCOM
                        except (AttributeError, IndexError, ValueError, TypeError):
                            lcom = None
                        try:
                            ca = item.Ca
                        except (AttributeError, IndexError, ValueError, TypeError):
                            ca = None
                        try:
                            ce = item.Ce
                        except (AttributeError, IndexError, ValueError, TypeError):
                            ce = None
                        try:
                            npm = item.NPM
                        except (AttributeError, IndexError, ValueError, TypeError):
                            npm = None
                        try:
                            lcom3 = item.LCOM3
                        except (AttributeError, IndexError, ValueError, TypeError):
                            lcom3 = None
                        try:
                            loc = item.LOC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            loc = None
                        try:
                            dam = item.DAM
                        except (AttributeError, IndexError, ValueError, TypeError):
                            dam = None
                        try:
                            moa = item.MOA
                        except (AttributeError, IndexError, ValueError, TypeError):
                            moa = None
                        try:
                            mfa = item.MFA
                        except (AttributeError, IndexError, ValueError, TypeError):
                            mfa = None
                        try:
                            cam = item.CAM
                        except (AttributeError, IndexError, ValueError, TypeError):
                            cam = None
                        try:
                            ic = item.IC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            ic = None
                        try:
                            cbm = item.CBM
                        except (AttributeError, IndexError, ValueError, TypeError):
                            cbm = None
                        try:
                            amc = item.AMC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            amc = None
                        try:
                            AVG_CC = item.AVG_CC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            AVG_CC = None
                        try:
                            MAX_CC = item.MAX_CC
                        except (AttributeError, IndexError, ValueError, TypeError):
                            MAX_CC = None

                        # writer.writerow([item.PROJECT_NAME, item.CLASS_NAME, item.WMC, item.DIT, item.NOC,
                        #                  item.CBO, item.RFC, item.LCOM, item.Ca, item.Ce, item.NPM, item.LCOM3, item.LOC,
                        #                  item.DAM, item.MOA, item.MFA, item.CAM, item.IC, item.CBM, item.AMC,
                        #                  item.AVG_CC, item.MAX_CC, item.NEWONE, item.PORTRAIT, item.DEFECT_CNT])
                        writer.writerow([item.PROJECT_NAME, item.CLASS_NAME, wmc, dit, noc, cbo, rfc, lcom,
                                         ca, ce, npm, lcom3, loc, dam, moa, mfa, cam, ic, cbm, amc, AVG_CC,
                                         MAX_CC, item.NEWONE, item.PORTRAIT, item.DEFECT_CNT])

            except BaseException as e:
                print('BaseException:', project_version_software_metrics_path)

        #project_version_software_metrics_path = project_version_path + "/" + os.path.splitext(file_name)[0] + ".metrics"

        prior_version_processed = current_version_processed
        prior_version_processed_number = current_version_processed_number
        prior_version_processed_classes = current_version_processed_classes

    return True

def process_version(current_version, list_of_methods, list_of_callgraph_ids):
    # intilize a null list
    list_of_classes = []

    # traverse for all elements
    for x in list_of_methods:
        # extract class name from full qualified name
        x = x.split(' ')[1].split(':')[0]
        # check if exists in list_of_classes or not
        if x not in list_of_classes:
            list_of_classes.append(x)
    # removing duplicated in case
    list_of_classes = list(dict.fromkeys(list_of_classes))
    # loop over list of classes
    for current_class in list_of_classes:
        # filter the methods which belong to particular class
        matching_methods = [s for s in list_of_methods if current_class in s]
        matching_methods_ids = []
        # get ids of filtered methods
        for m in matching_methods:
            matching_methods_ids.append(int(m.split(" ")[0]))
        modified_callgraph_list = []
        # loop over call graph to filter the lines which are related to the class
        for sid in list_of_callgraph_ids:
            first = int(sid.split(" ")[0])
            second = int(sid.split(" ")[1])

            if first in matching_methods_ids or second in matching_methods_ids:
                modified_callgraph_list.append(str(first) + ' ' + str(second) + ' ' + "1.5")
            else:
                modified_callgraph_list.append(str(first) + ' ' + str(second) + ' ' + "1.0")
            filepath = Path(constant.OUTPUT, current_version + '--' + current_class + '.txt')
            with open(filepath, 'w') as file_handler:
                for item in modified_callgraph_list:
                    file_handler.write("{}\n".format(item))


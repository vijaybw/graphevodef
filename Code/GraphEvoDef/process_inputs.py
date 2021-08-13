import constant
import sys, os
from pathlib import Path
def process_version(current_version, list_of_methods,list_of_callgraph_ids):
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
        #loop over call graph to filter the lines which are related to the class
        for sid in list_of_callgraph_ids:
            first = int(sid.split(" ")[0])
            second = int(sid.split(" ")[1])

            if first in matching_methods_ids or second in matching_methods_ids:
                modified_callgraph_list.append(str(first) + ' ' + str(second) + ' ' + "1.5")
            else:
                modified_callgraph_list.append(str(first) + ' ' + str(second) + ' ' + "1.0")
            filepath = constant.OUTPUT + '/' + current_version + '-' + current_class + '.txt'
            with open(filepath, 'w') as file_handler:
                for item in modified_callgraph_list:
                    file_handler.write("{}\n".format(item))
def generate_cg_files(list_of_applications):
    for application in list_of_applications:
        application_name = application.__str__()
        for application_version in list_of_applications[application_name]:
            callgraph_methods_file = open(
                constant.INPUT_CALLGRAPHS_FOLDER + '/' + application_name + '-' + application_version + '-callgraph.txt',
                'r')
            callgraph_methods_file_lines = callgraph_methods_file.readlines()
            callgraph_methods_ids_file = open(
                constant.INPUT_CALLGRAPHS_FOLDER + '/' + application_name + '-' + application_version + '-callgraphNumbers.txt',
                'r')
            callgraph_methods_file_ids_lines = callgraph_methods_ids_file.readlines()
            process_version(application_name + '-' + application_version, callgraph_methods_file_lines,
                            callgraph_methods_file_ids_lines)
            print("Processed " + application_name + '-' + application_version)
def process_cgs():
    # driver code
    current_version_processed = ''
    current_version_processed_number = ''
    prior_version_processed = ''
    current_version_processed_classes = []
    import csv

    for application in constant.APPLICATION:
        application_name = application.__str__()
        for application_version_number in constant.APPLICATION[application_name]:
            prior_version_processed =  current_version_processed
            prior_version_processed_number = current_version_processed_number
            current_version_processed = application_name + '-' + application_version_number
            current_version_processed_number = application_version_number

            callgraph_methods_file = open(
                constant.INPUT_CALLGRAPHS_FOLDER + '/' + application_name + '-' + application_version_number + '-callgraph.txt',
                'r')
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
            prior_version_processed_classes = current_version_processed_classes
            list_of_classes = list(dict.fromkeys(list_of_classes))
            current_version_processed_classes = list_of_classes

            # loop over list of classes
            from os import listdir
            from os.path import isfile, join

            onlyfiles = [f for f in listdir(constant.OUTPUT) if isfile(join(constant.OUTPUT, f))]

            # filter the methods which belong to particular class
            matching_cgs_files = [s for s in onlyfiles if application_version_number in s]
            matching_methods_ids = []

            cwd = os.getcwd()
            script_path = Path(cwd,"portrait_divergence.py").as_posix()
            script_parameters = Path("-d --weighted=strength").as_posix()

            with open(constant.OUTPUT_CSV + '/' + current_version_processed +'-network_portrait.csv', 'w', newline='') as csvfile:
                fieldnames = ['class_name', 'new', 'portrait']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                if prior_version_processed == '':
                    for cgs in matching_cgs_files:
                        new_one = 1
                        class_name_in_file = cgs.split("-")[2].replace(".txt", "")
                        first = constant.INPUT_CALLGRAPHS_FOLDER + '/' + current_version_processed + '-callgraphNumbers.txt'
                        second = constant.OUTPUT + '/' + cgs

                        filenamef = Path(cwd, first).as_posix()
                        filenames = Path(cwd, second).as_posix()

                        calculated_portrait = os.popen(sys.executable + ' ' + script_path + ' ' + script_parameters + ' ' + filenamef + ' ' + filenames).readlines()
                        calculated_portraittext = ""
                        for ln in calculated_portrait:
                            calculated_portraittext = calculated_portraittext + ln.rstrip('\n')
                        writer.writerow({'class_name': class_name_in_file, 'new': new_one,'portrait': calculated_portraittext})
                        # print(current_version_processed + " " +  class_name_in_file + " " + calculated_portraittext)
                else:
                    for cgs in matching_cgs_files:
                        class_name_in_file = cgs.split("-")[2].replace(".txt","")
                        if cgs == 'ant-1.6-org.apache.tools.ant.AntClassLoader.txt':
                            abc = 1

                        if prior_version_processed_classes.count(str(class_name_in_file)) > 0:
                            new_one = "0"
                            first = constant.OUTPUT + '/' + cgs.replace(application_version_number,prior_version_processed_number)
                        else:
                            new_one = "1"
                            first = constant.INPUT_CALLGRAPHS_FOLDER + '/' + current_version_processed + '-callgraphNumbers.txt'

                        second = constant.OUTPUT + '/' + cgs

                        filenamef = Path(cwd, first).as_posix()
                        filenames = Path(cwd, second).as_posix()

                        calculated_portrait = os.popen(sys.executable + ' ' + script_path + ' ' + script_parameters + ' ' + filenamef + ' ' + filenames).readlines()
                        calculated_portraittext = ""
                        for ln in calculated_portrait:
                            calculated_portraittext = calculated_portraittext + ln.rstrip('\n')
                        writer.writerow({'class_name': class_name_in_file, 'new': new_one, 'portrait': calculated_portraittext})
            print("Processed " + application_name + '-' + application_version_number)
def club_data():
    promisedata_list = []
    for application in constant.APPLICATION:
        application_name = application.__str__()
        for application_version_number in constant.APPLICATION[application_name]:
            current_version_processed = application_name + '-' + application_version_number
            import csv
            #file_name = constant.PROMISEDATA + '/' + application_name + '/' + current_version_processed + '/' + current_version_processed + ".csv"
            if os.path.isdir(constant.PROMISEDATA + '/' + application_name + '/' + current_version_processed):
                file_name = constant.PROMISEDATA + '/' + application_name + '/' + current_version_processed + '/' + current_version_processed + ".csv"
            else:
                file_name = constant.PROMISEDATA + '/' + application_name + '/' + current_version_processed + ".csv"
            import csv

            with open(file_name, newline='') as f:
                reader = csv.reader(f)
                for x in list(reader):
                    promisedata_list.append(x)
    networkportraitdata_list = []
    for application in constant.APPLICATION:
        application_name = application.__str__()
        for application_version_number in constant.APPLICATION[application_name]:
            current_version_processed = application_name + '-' + application_version_number
            import csv
            file_name = constant.OUTPUT_CSV + '/' + current_version_processed + "-network_portrait.csv"
            import csv

            with open(file_name, newline='') as f:
                reader = csv.reader(f)
                for x in list(reader):
                    p = list(x)
                    p.extend([application_name,application_version_number])
                    networkportraitdata_list.append(p)

    app_name = ''
    app_version = ''
    app_class_name = ''
    processed_list = []
    for x in promisedata_list:
        if x[0] != 'name':
            app_name = x[0]
            app_version = x[1]
            if app_name == 'camel':
                if app_version == '1':
                    app_version = '1.0.0'
                elif app_version == '1.2':
                    app_version = '1.2.0'
            if app_name == 'ivy':
                if app_version == '2':
                    app_version = '2.0.0'
            if app_name == 'lucene':
                if app_version == '2':
                    app_version = '2.0.0'
                elif app_version == '2.2':
                    app_version = '2.2.0'
                elif app_version == '2.4':
                    app_version = '2.4.0'
            if app_name == 'pbeans':
                if app_version == '1':
                    app_version = '1.0'
                elif app_version == '2':
                    app_version = '2.0'
            if app_name == 'poi':
                if app_version == '2.0RC1':
                    app_version = '2.0'
                elif app_version == '2.5':
                    app_version = '2.0'
                elif app_version == '3':
                    app_version = '3.0'

            app_class_name = x[2]
            for n in networkportraitdata_list:
                if app_name == n[3] and app_version == n[4] and app_class_name == n[0]:
                    p = list(x)
                    p.extend([n[1], n[2]])
                    processed_list.append(p)
    with open(constant.PROCESSED + '/' +'processed_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['name','version','name','wmc','dit','noc','cbo','rfc','lcom','ca','ce','npm','lcom3','loc','dam','moa','mfa','cam','ic','cbm','amc','max_cc','avg_cc','bug','new','portrait']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in processed_list:
            writer.writerow({'name': x[0], 'version': x[1], 'name': x[2], 'wmc': x[3],
                 'dit': x[4], 'noc': x[5], 'cbo': x[6], 'rfc': x[7], 'lcom': x[8], 'ca': x[9],
                 'ce': x[10], 'npm': x[11], 'lcom3': x[12], 'loc': x[13], 'dam': x[14], 'moa': x[15],
                 'mfa': x[16], 'cam': x[17], 'ic': x[18], 'cbm': x[19], 'amc': x[20],
                 'max_cc': x[21], 'avg_cc': x[22], 'bug': x[23], 'new': x[24], 'portrait': x[25]})
# generate_cg_files()
# process_cgs()
club_data()
#process_cgs()
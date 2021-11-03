from modules.dict_regex import version_regex
import os

cwd = os.getcwd()
path = "{}/version".format(cwd)
os.mkdir(path)
os.chdir(path)


def version_parser(output):
    data_dictionary = {}
    ios_software_list = []
    name_list = []
    uptime_list = []
    version_list = []
    serial_list = []
    model_list = []
    memory_list = []
    cpu_clock_list = []
    cpu_core_list = []
    cpu_model_list = []
    ios_release_list = []
    mac_list = []

    for key, regex in version_regex.items():
        matches = regex.findall(output)
        if matches:
            if key == "IOS Software":
                ios_software_list.append(matches[0])
            if key == "Name":
                name_list.append(matches[0])
            if key == "Uptime":
                uptime_list.append(matches[0])
            if key == "Version":
                version_list.append(matches[0])
            if key == 'Serial':
                serial_list.append(matches[0])
            if key == 'Model':
                model_list.append(matches[0])
            if key == 'Memory':
                memory_list.append(matches[0])
            if key == 'CPU Clock':
                cpu_clock_list.append(matches[0])
            if key == 'CPU Core':
                cpu_core_list.append(matches[0])
            if key == 'CPU Model':
                cpu_model_list.append(matches[0])
            if key == 'IOS Release':
                ios_release_list.append(matches[0])
            if key == 'MAC':
                mac_list.append(matches[0])

    data_dictionary['IOS Software'] = ios_software_list
    data_dictionary['Name'] = name_list
    data_dictionary['Uptime'] = uptime_list
    data_dictionary['Version'] = version_list
    data_dictionary['Serial'] = serial_list
    data_dictionary['Model'] = model_list
    data_dictionary['Memory'] = memory_list
    data_dictionary['CPU Clock'] = cpu_clock_list
    data_dictionary['CPU Core'] = cpu_core_list
    data_dictionary['CPU Model'] = cpu_model_list
    data_dictionary['IOS Release'] = ios_release_list
    data_dictionary['MAC Address'] = mac_list

    # print(data_dictionary)
    return data_dictionary

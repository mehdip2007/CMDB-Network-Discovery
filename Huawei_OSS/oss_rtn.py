import re
import os
import pandas as pd


def data_to_csv(string, filename):

    def dict_to_csv(dictionary):
        df = pd.DataFrame.from_dict(dictionary, orient="index").T
        df.to_csv("{}.csv".format(filename), index=False)

    string = string.replace("{", "").replace("}", "").replace('"', '')

    keys_pattern = r"(\S+)="
    keys_match = re.findall(keys_pattern, string, re.M)

    values_pattern = r"=(\S+)"
    values_match = re.findall(values_pattern, string, re.M)
    values_match = [i.replace(",", "") for i in values_match]

    data_dictionary = dict(zip(keys_match, values_match))
    dict_to_csv(data_dictionary)


def get_nepara(filepath):
    nepara_pattern = r":cfg-nepara:((?s){.*?})"

    filename, file_extension = os.path.splitext(filepath)
    filename = filename.split("/")[-1]

    with open(filepath, "r") as file_object:
        lines = file_object.read()
        matches = re.search(nepara_pattern, lines)
        matches = matches.group(1)
        data_to_csv(matches, filename)


file_to_read = "/Users/mehdi/Downloads/NEData_148-42499_H1511_(UTF-8).txt"
get_nepara(file_to_read)

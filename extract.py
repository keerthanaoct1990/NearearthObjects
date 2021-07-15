"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


instances = {}


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, 'r') as csv_file:  #read from csv
        reader = csv.DictReader(csv_file)
        neo_instances = []
        for row in reader:
            content = NearEarthObject(row['pdes'], row['name'], row['diameter'], row['pha'])  #read data from required cols
            neo_instances.append(content)
            instances[row['pdes']] = content
    return neo_instances


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_app_instances = []
    with open(cad_json_path, 'r') as json_file:  #load json data
        data = json.load(json_file)
        content = data['data']
        for d in content:
            each_row = CloseApproach(instances.get(d[0]), d[3], d[4], d[7])
            close_app_instances.append(each_row)

    return close_app_instances

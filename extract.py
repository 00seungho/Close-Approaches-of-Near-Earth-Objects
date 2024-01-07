import csv
import json

from models import NearEarthObject, CloseApproach


import csv
from models import NearEarthObject

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = [] 

    with open(neo_csv_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[15]:
                dbdiameter = float(row[15])
            else:
                dbdiameter = float('nan')
            neo = NearEarthObject(designation = row[3],name=row[4],diameter=dbdiameter,hazardous=row[7] == "Y")
            neos.append(neo)

    return neos

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_approaches = [] 
    with open(cad_json_path, "r") as file:
        data = json.load(file)
        fields = data['fields']
        for entry in data['data']:
            ca_data = dict(zip(fields, entry))
            if float(ca_data['dist']):
                float_dist = float(ca_data['dist'])
            else:
                float_dist=float('nan')
            if float(ca_data['v_rel']):
                float_v_rel = float(ca_data['v_rel'])
            else:
                float_v_rel=float('nan')
            ca = CloseApproach(_designation = ca_data['des'],time=ca_data['cd'],distance= float_dist,velocity = float_v_rel)
            close_approaches.append(ca)

    return close_approaches

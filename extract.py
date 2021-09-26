"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, "r") as infile:
        reader = csv.DictReader(infile)

        neo_objs = []
        for line in reader:

            if not line["diameter"]:
                line["diameter"] = float("nan")
            else:
                line["diameter"] = float(line["diameter"])

            if not line["name"]:
                line["name"] = None

            line["pha"] = False if line["pha"] in ["N", ""] else True

            dict_info = {
                "pdes": line["pdes"],
                "name": line["name"],
                "diameter": line["diameter"],
                "pha": line["pha"],
            }

            neo_obj = NearEarthObject(**dict_info)

            neo_objs.append(neo_obj)

    return neo_objs


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, "r") as f:
        loader = json.load(f)
        list_cad = [dict(zip(loader["fields"], cad)) for cad in loader["data"]]

        cads = []
        for line in list_cad:

            dict_info = {
                "des": str(line["des"]),
                "cd": line["cd"],
                "dist": float(line["dist"]),
                "v_rel": float(line["v_rel"]),
            }

            cad = CloseApproach(**dict_info)
            cads.append(cad)

    return cads

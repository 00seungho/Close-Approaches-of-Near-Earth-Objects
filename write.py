import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    
    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            content = result.serialize()
            content.update(result.neo.serialize())
            content["name"] = content["name"] if content["name"] is not None else ""
            content["potentially_hazardous"] = "True" if content["potentially_hazardous"] else "False"
            writer.writerow(content)

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    json_data = []
    for result in results:
        content = result.serialize()
        content.update(result.neo.serialize())
        content["name"] = content["name"] if content["name"] is not None else ""
        content["potentially_hazardous"] = "True" if content["potentially_hazardous"] else "False"
        json_data.append(
            {
                "datetime_utc": content["datetime_utc"],
                "distance_au": content["distance_au"],
                "velocity_km_s": content["velocity_km_s"],
                "neo": {
                    "designation": content["designation"],
                    "name": content["name"],
                    "diameter_km": content["diameter_km"],
                    "potentially_hazardous": bool(content["potentially_hazardous"])
                }
            }
        )
    with open(filename, "w") as json_file:
        json.dump(json_data, json_file)
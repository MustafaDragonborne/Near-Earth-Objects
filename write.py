"""
Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""

import csv
import json
from helpers import datetime_to_str


def csv_data_structure(approach):
    """Return dictionary with required format containing CloseApproach data.

    The approach parameter is a CloseApproach object. This function takes in a
    CloseApproach object and returns a dictionary with the required parameters
    in the required structure for writing to csv. This function is called
    within the write_to_csv function.
    """
    approach_dict = {'datetime_utc': datetime_to_str(approach.time),
                     'distance_au': approach.distance,
                     'velocity_km_s': approach.velocity,
                     'designation': approach._designation,
                     'name': approach.neo.name,
                     'diameter_km': approach.neo.diameter,
                     'potentially_hazardous': approach.neo.hazardous}
    if approach_dict['name'] is None:
        approach_dict['name'] = ''
    return approach_dict


def json_data_structure(approach):
    """Return dictionary with required format containing CloseApproach data.

    The approach parameter is a CloseApproach object. This function takes in a
    CloseApproach object and returns a dictionary with the required parameters
    in the required structure for writing to json. This function is called
    within the write_to_json function.
    """
    approach_dict = {'datetime_utc': datetime_to_str(approach.time),
                     'distance_au': approach.distance,
                     'velocity_km_s': approach.velocity,
                     'neo': {
                        'designation': approach._designation,
                        'name': approach.neo.name,
                        'diameter_km': approach.neo.diameter,
                        'potentially_hazardous': approach.neo.hazardous
                            }
                     }
    if approach_dict['neo']['name'] is None:
        approach_dict['neo']['name'] = ''
    return approach_dict


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` tream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')
    list_approach_dict = [csv_data_structure(approach) for approach in
                          list(results)]
    with open(filename, 'w', newline='') as f:
        # use DictWrite to also include the header row
        writer = csv.DictWriter(f, fieldnames=list_approach_dict[0].keys())
        writer.writeheader()  # write the header line
        if list_approach_dict:
            for elem in list_approach_dict:
                writer.writerow(elem)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is
    a list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    list_approach_dict = [json_data_structure(approach) for approach in
                          list(results)]
    with open(filename, 'w') as f:
        json.dump(list_approach_dict, f, indent=3)

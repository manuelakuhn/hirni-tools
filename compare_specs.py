""" Reading and comparing datalad studyspec files """

import json
from pathlib import Path
# from pprint import pprint
# import re

from deepdiff import DeepDiff


def _remove_keys(input_dict: dict):
    """ Remove keys from dict that are may differ between datasets"""

    to_remove = ["dataset-id", "dataset-refcommit", "uid"]

    for key in to_remove:
        try:
            del input_dict[key]
        except KeyError:
            pass

    return input_dict


def read_spec(file_name: str or Path):
    """ Reads a datalad spec file and converts it into proper python objects"""

    # allow string
    file_name = Path(file_name)

    # strip: file may contain empty lines
    lines = file_name.read_text().strip().split("\n")
    return list(map(json.loads, lines))


def _sort_spec(spec_list: list):
    """ Sort a spec acording to the file name of the dicomseries """

    nondicomseries_list = [i for i in spec_list if i["type"] != "dicomseries"]
    dicomseries_list = sorted(
        [i for i in spec_list if i["type"] == "dicomseries"],
        key=lambda i: i["description"]["value"]
    )

    return nondicomseries_list + dicomseries_list


def _display_changes(changes: list):

    for changed in changes:
        tmp = changed
        while tmp is not None:
            if isinstance(tmp.t1, dict) and "type" in tmp.t1:
                if tmp.t1["type"] == "dicomseries":
                    identifier = tmp.t1["description"]["value"]
                else:
                    identifier = tmp.t1["type"]
                break
            tmp = tmp.up

        print("changes in entry for {} : {}"
              .format(identifier, str(changed)))
#              .format(identifier, re.sub(r"root\[[0-9]+\]", "", str(changed))))


def compare_specs(spec_file1: str, spec_file2: str):
    """ Compare two datalad spec files """

    spec_before = list(map(_remove_keys, read_spec(spec_file1)))
    spec_after = list(map(_remove_keys, read_spec(spec_file2)))

    sorted_spec_before = _sort_spec(spec_before)
    sorted_spec_after = _sort_spec(spec_after)

    diff = DeepDiff(sorted_spec_before, sorted_spec_after, view='tree')

    # key are "dictionary_item_added", "dictionary_item_removed",
    #         "values_changed"
    for key, value in diff.items():
        print("{}:".format(key))
        _display_changes(value)


if __name__ == "__main__":
    compare_specs("../ds_before/sourcedata/studyspec.json",
                 "../ds_after/sourcedata/studyspec.json")

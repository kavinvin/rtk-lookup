#!/usr/bin/python3
# -*- coding: utf8 -*-

""" Functions that don't fit into any other file.
"""


import os
import re
import csv
from .colorama import remove_color

__author__ = "ch4noyu"
__email__ = "ch4noyu@yahoo.com"
__license__ = "LGPLv3"


def copy_to_clipboard(clip: str) -> int:
    """ Copies argument to clipboard.
    :param clip: The text to look up.
    :return 0 for success, otherwise a number != 0
    """
    # Check if we are running on linux:
    if os.name == "posix":
        success = os.system("echo -n '%s' | xclip -selection c" % clip)
    else:
        raise NotImplemented
    return success


def lookup(clip: str) -> int:
    """ Looks up phrase in the www
    :param clip: The text to look up.
    :return 0 for success, otherwise a number != 0
    """
    # Check if we are running on linux:
    if os.name == "posix":
        success = os.system("firefox http://tangorin.com/general/dict.php?dict=general\&s=%s &" % clip)
    else:
        raise NotImplemented
    return success


class CyclicalList(list):
    """ Like a normal list only with the __getitem__ method overwritten
    so that CyclicalList[index] equals CyclicalList[index % len(CyclicalList)],
    i.e. this behaves like a periodic list: CyclicalList([1,2,3]) = [1,2,3,1,2,3,1,2,3,....]
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, item: int):
        return list.__getitem__(self, item % len(self))


def approximate_string_length(string: str) -> int:
    """ Note that kanji have about twice the width of latin
    characters. This Function returns the length of $string as a
    multiple of the length of a latin character.
    Note: Only works for combinations of Latin characters and (full width)
          Asian characters.
    :param string: String.
    :return:
    """
    string = remove_color(string)
    latin_chars_regex = re.compile("[\u0020-\u007f]")
    return 2*len(string) - len(latin_chars_regex.findall(string))

# todo: docstring
def guess_csv_config(filename: str, input_dict):
    return_dict = input_dict
    if not os.path.exists(filename):
        raise ValueError
    if not input_dict["delimiter"]:
            # guess delimiter from filename:
            if os.path.splitext(filename)[1] == ".tsv":
                return_dict["delimiter"] = '\t'
            elif os.path.splitext(filename)[1] == ".csv":
                return_dict["delimiter"] = ','
            else:
                raise ValueError
    if None in return_dict.values():
        # guess from first line of file
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=return_dict["delimiter"])
            for row in reader:
                for column_no, column in enumerate(row):
                    for key in return_dict:
                        if key.replace("_column", "") in column and return_dict[key] is None:
                            return_dict[key] = column_no
                # abort search after first line
                break

    if None in return_dict.values():
        raise ValueError

    return return_dict


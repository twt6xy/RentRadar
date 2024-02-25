import uuid

import pandas as pd


def string_to_uuid(input_string):
    namespace = uuid.NAMESPACE_DNS
    result_uuid = uuid.uuid5(namespace, input_string)
    return result_uuid


def convert_nan_to_none(data: dict) -> dict:
    """
    Recursively converts all occurrences of numpy.nan in a dictionary to None.

    Args:
        data (dict): The dictionary to clean.

    Returns:
        dict: The cleaned dictionary with all numpy.nan values replaced by None.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = convert_nan_to_none(value)
        elif isinstance(value, list):
            data[key] = [
                convert_nan_to_none(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            data[key] = None if pd.isna(value) else value
    return data

"""
This utility provides helper functions related to cbeff.
Check the docs to know the final cbeff xml format
"""
from .biometrics import Biometrics


def create(d: list[Biometrics], path: str):
    """Create a CBEFF xml file

        Keyword arguments:
        d -- List of Biometrics
        path -- destination path where the file will be created
    """
    return


def delete(path: str):
    """Delete a CBEFF xml file

        Keyword arguments:
        path -- path of the file to be deleted
    """
    return


def validate(path: str) -> bool:
    """Validate a CBEFF xml file and return true (if valid)/ false (if invalid)

        Keyword arguments:
        path -- path of the file to be validated
    """
    return

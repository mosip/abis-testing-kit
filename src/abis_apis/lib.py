"""
This utility provides helper functions related to ABIS APIs.
Check the docs to know about ABIS APIs
"""


def insert(request_id: str, reference_id: str, reference_url: str):
    """Create a CBEFF xml file

        Keyword arguments:
        d -- List of Biometrics
        path -- destination path where the file will be created
    """
    return


def identify(request_id: str, reference_id: str, reference_url: str, max_results: int, target_fpir: int, reference_ids: list[dict]):
    """Delete a CBEFF xml file

        Keyword arguments:
        path -- path of the file to be deleted
    """
    return


def delete(request_id: str, reference_id: str):
    """Validate a CBEFF xml file and return true (if valid)/ false (if invalid)

        Keyword arguments:
        path -- path of the file to be validated
    """
    return
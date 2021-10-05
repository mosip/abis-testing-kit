"""
This utility provides helper functions related to cbeff.
Check the docs to know the final cbeff xml format
"""
import base64

from biometrics import Biometrics
import xml.etree.ElementTree as ET
from typing import List, AnyStr
from cbeff_config import CBEFFConfig
import datetime
import os
import string
import random
from xml.dom import minidom


def create(d: List[Biometrics], path: AnyStr):
    """Create a CBEFF xml file

        Keyword arguments:
        d -- List of Biometrics
        path -- destination path where the file will be created
    """
    parent_bir = ET.Element('BIR')
    parent_bir_info = ET.SubElement(parent_bir, 'BIRInfo')
    for biometric in d:
        """ BIR block """
        bir = ET.SubElement(parent_bir, 'BIR')

        """ Version block """
        version = ET.SubElement(bir, 'Version')
        version_major = ET.SubElement(version, 'Major')
        version_major.text = CBEFFConfig.version_major
        version_minor = ET.SubElement(version, 'Minor')
        version_minor.text = CBEFFConfig.version_minor

        """ CBEFF Version block """
        cbeff_version = ET.SubElement(bir, 'CBEFFVersion')
        cbeff_version_major = ET.SubElement(cbeff_version, 'Major')
        cbeff_version_major.text = CBEFFConfig.cbeff_version_major
        cbeff_version_minor = ET.SubElement(cbeff_version, 'Minor')
        cbeff_version_minor.text = CBEFFConfig.cbeff_version_minor

        """ Child BIRInfo block """
        bir_info = ET.SubElement(bir, 'BIRInfo')
        integrity = ET.SubElement(bir_info, 'Integrity')
        integrity.text = CBEFFConfig.bir_info_integrity

        """ BDBInfo Block """
        bdb_info = ET.SubElement(bir, 'BDBInfo')

        """ Format Block """
        cbeff_format = ET.SubElement(bdb_info, 'Format')
        format_organization = ET.SubElement(cbeff_format, 'Organization')
        format_organization.text = CBEFFConfig.format_organization
        format_type = ET.SubElement(cbeff_format, 'Type')
        format_type.text = CBEFFConfig.format_type

        """ Creation date Block """
        creation_date = ET.SubElement(bdb_info, 'CreationDate')
        creation_date.text = str(datetime.datetime.now())

        """ Biometric Type Block """
        biometric_type = ET.SubElement(bdb_info, 'Type')
        biometric_type.text = biometric.bio_type

        """ Biometric Subtype Block """
        biometric_sub_type = ET.SubElement(bdb_info, 'Subtype')
        biometric_sub_type.text = biometric.sub_type

        """ Level Block """
        level = ET.SubElement(bdb_info, 'Level')
        level.text = CBEFFConfig.level

        """ Purpose Block """
        purpose = ET.SubElement(bdb_info, 'Purpose')
        purpose.text = CBEFFConfig.purpose

        """ Quality Block """
        quality = ET.SubElement(bdb_info, 'Quality')

        """ Quality Algorithm Block """
        quality_algorithm = ET.SubElement(quality, 'Algorithm')
        quality_algorithm_organization = ET.SubElement(quality_algorithm, 'Organization')
        quality_algorithm_organization.text = CBEFFConfig.quality_algorithm_organization
        quality_algorithm_type = ET.SubElement(quality_algorithm, 'Organization')
        quality_algorithm_type.text = CBEFFConfig.quality_algorithm_type

        """ Quality Score Block """
        quality_score = ET.SubElement(quality, 'Score')
        quality_score.text = CBEFFConfig.quality_score

        """ BDB Block """
        bdb = ET.SubElement(bir, 'BDB')
        bdb.text = biometric.file_content

        ET.dump(parent_bir)
        if not os.path.exists('tmp_data'):
            os.makedirs('tmp_data')
        path = os.path.join('tmp_data', uuid + "_cbeff.xml") if path is None else path
        uuid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        ET.ElementTree.write(ET.ElementTree(parent_bir), path)

        xml_str = minidom.parseString(ET.tostring(parent_bir)).toprettyxml(indent="   ")
        with open(path, "w") as f:
            f.write(xml_str)
            f.close()
    return


def createViaFolderPath():
    """Create a CBEFF xml from the folder structure

        Keyword arguments:
        folder_path -- folder path
        path -- destination path where the file will be created
    """
    biometric_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'biometric_data')

    if not os.path.isdir(biometric_folder_path):
        raise Exception("Path not found: "+biometric_folder_path)

    for dirr in os.listdir(biometric_folder_path):
        user_dir = os.path.join(biometric_folder_path, dirr)
        if os.path.isdir(user_dir):
            biometrics_list = []
            for sub_dirr in os.listdir(os.path.join(biometric_folder_path, dirr)):
                file_list = os.path.join(user_dir, sub_dirr)
                if os.path.isfile(file_list) and sub_dirr.endswith('.jpeg'):
                    strs = sub_dirr.split('.')[0].split("_")
                    if len(strs) != 2:
                        return False, None, "filename should be <Biometric type>_<Biometric subtype>"

                    with open(file_list, 'rb') as file:
                        data = file.read()
                        data = base64.b64encode(data).decode('utf-8')
                    biometric = Biometrics(strs[0], strs[1], data)
                    biometrics_list.append(biometric)
            print(user_dir)
            create(biometrics_list, os.path.join(user_dir, dirr+'_cbeff.xml'))
    return


def validate(self, path: AnyStr) -> bool:
    """Validate a CBEFF xml file and return true (if valid)/ false (if invalid)

        Keyword arguments:
        path -- path of the file to be validated
    """
    return True


if __name__ == '__main__':
    createViaFolderPath()

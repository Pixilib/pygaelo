import os
import zipfile
import hashlib
from typing import List
from pydicom import dicomdir, read_file, FileDataset

def read_folder(dicom_folder: str, read_pixel: bool = False) -> List[FileDataset]:
    """Retrieve all valid dicom files in a folder (recursively)

    Args:
        dicom_folder (str): folder to scan
        read_pixel (bool): load pixel in memory

    Returns:
        List[FileDataset]: Array of DICOM file metadata
    """
    instances: List[FileDataset] = []
    for root, dirs, files in os.walk(dicom_folder):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                dicom_data = read_file(
                    file_path, stop_before_pixels=(not read_pixel), force=True)
                if isinstance(dicom_data, dicomdir.DicomDir): continue
                instances.append(dicom_data)
            except:
                print(file + 'is not a dicom')
    return instances


def get_study_orthanc_id(instance: FileDataset) -> str:
    """Compute Orthanc Study UID of a DICOM instant Metadata

    Args:
        instance (FileDataset): Metadata of a DICOM

    Returns:
        str: Orthanc Study ID
    """
    string_to_hash = instance.PatientID + '|' + instance.StudyInstanceUID
    myhash = hashlib.sha1(string_to_hash.encode('utf-8'))
    hash = myhash.hexdigest()
    hash = '-'.join(hash[i:i+8] for i in range(0, len(hash), 8))
    return hash

def are_same_study(instances: List[FileDataset]) -> bool:
    """Checks all DICOMs metadata belongs to the same Study UID

    Args:
        instances (List[FileDataset]): Metadata of a list of DICOM

    Returns:
        bool
    """
    study_instance_uids = []
    for instance in instances:
        study_instance_uid = instance.StudyInstanceUID
        study_instance_uids.append(study_instance_uid)
    if len(set(study_instance_uids)) == 1:
        return True
    else:
        return False


def check_are_same_study_and_get_orthanc_id(instances: List[FileDataset]) -> str | None:
    """Checks that all DICOMS belong to a same study and return orthanc study ID

    Args:
        instances (List[FileDataset]): Metadata of a list of DICOM

    Returns:
        str | None: Orthanc Study ID
    """
    if (not are_same_study(instances)):
        return None
    return get_study_orthanc_id(instances[0])


def zip_dicoms(instances: List[FileDataset], destination: str) -> None:
    """ZIP all DICOMs

    Args:
        instances (List[FileDataset]): Metadata of a list of DICOM
        destination (str): Folder with filename to write
    """
    zf = zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED)
    for instance in instances:
        myhash = hashlib.sha1(instance.SOPInstanceUID.encode('utf-8'))
        hashed_instance_uid = myhash.hexdigest()
        zf.write(instance.filename, hashed_instance_uid)
    zf.close()

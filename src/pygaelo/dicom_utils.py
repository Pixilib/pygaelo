import os
import zipfile
import hashlib
from typing import List
from pydicom import dicomdir, read_file, FileDataset


def read_folder(dicom_folder: str, read_pixel: bool):
    instances: List[FileDataset] = []
    for root, dirs, files in os.walk(dicom_folder):
        for file in files:
            file_path = os.path.join(root, file)
            dicom_data = read_file(
                file_path, stop_before_pixels=(not read_pixel), force=True)
            if isinstance(dicom_data, dicomdir.DicomDir):
                raise Exception('DICOMDIR File')
            instances.append(dicom_data)
    return instances

def get_study_orthanc_id( instance : FileDataset) ->str:
    string_to_hash = instance.PatientID + '|' + instance.StudyInstanceUID
    myhash = hashlib.sha1(string_to_hash.encode('utf-8'))
    hash = myhash.hexdigest()
    hash = '-'.join(hash[i:i+8] for i in range(0, len(hash), 8))
    return hash

def are_same_study(instances: List[FileDataset]) -> bool:
    study_instance_uids = []
    for instance in instances:
        study_instance_uid = instance.StudyInstanceUID
        study_instance_uids.append(study_instance_uid)
    if len(set(study_instance_uids)) == 1:
        return True
    else:
        return False


def zip_dicoms(instances: List[FileDataset], destination :str):
   zf = zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED)
   for instance in instances:
       myhash = hashlib.sha1(instance.SOPInstanceUID.encode('utf-8'))
       hashed_instance_uid = myhash.hexdigest()
       zf.write(instance.filename, hashed_instance_uid)
   zf.close()
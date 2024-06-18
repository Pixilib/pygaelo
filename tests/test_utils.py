import unittest
from pydicom import Dataset
from pygaelo.dicom_utils import read_folder, are_same_study, zip_dicoms, get_study_orthanc_id


class TestDicomUtils(unittest.TestCase):

    @unittest.skip
    def test_read_folder(self):
        intances = read_folder("", False)
        self.assertIsInstance(intances, list)

    @unittest.skip
    def test_are_same_studies(self):
        intances = read_folder("", False)
        same_study = are_same_study(intances)
        self.assertTrue(same_study)

    @unittest.skip
    def test_zip_dicoms(self):
        intances = read_folder("", False)
        zip_dicoms(intances, 'dicom.zip')

    def test_get_study_orthanc_id(self):
        ds = Dataset()
        ds.PatientID = "5Yp0E"
        ds.StudyInstanceUID = "2.16.840.1.113669.632.20.1211.10000357775"
        orthanc_id = get_study_orthanc_id(ds)
        self.assertEqual(orthanc_id, '27f7126f-4f66fb14-03f4081b-f9341db2-53925988')

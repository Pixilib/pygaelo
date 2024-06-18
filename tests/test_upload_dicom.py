import unittest
from faker import Faker
from dotenv import dotenv_values
from pygaelo.dicom_utils import read_folder, zip_dicoms, get_study_orthanc_id
from pygaelo.gaelo_client import GaelOClient

# @unittest.skip
class TestUploadDicoms(unittest.TestCase):

    gaelo_apis: GaelOClient

    def setUp(self) -> None:
        config = dotenv_values(".env.dev")
        gaelo_apis = GaelOClient()
        gaelo_apis.set_url(config['GAELO_URL'])
        gaelo_apis.login(config['GAELO_USERNAME'], config['GAELO_PASSWORD'])
        self.gaelo_apis = gaelo_apis

        faker = Faker()
        patient_code = faker.pyint(10000000000000, 99999999999999)
        patient_firstname = faker.pystr(1, 1)
        patient_lastname = faker.pystr(1, 1)
        patient = {
            "code": str(patient_code),
            "firstname": patient_firstname,
            "lastname": patient_lastname,
            "centerCode": 0,
            "registrationDate": "5-5-2022",
            "inclusionStatus": "Included",
            "birthDay": None,
            "birthMonth": None,
            "birthYear":  None,
            "gender": "M",
            "investigatorName":  None
        }
        gaelo_apis.import_patients(
            'TEST', 'Supervisor', [patient])
        patient_id = '170000' + str(patient_code)

        creatable_visits = gaelo_apis.get_creatable_visits_types_of_patient(
            patient_id)
        creatable_visit_type = [
            visit for visit in creatable_visits if visit.get('name') == "CT0"]
        answer = gaelo_apis.create_visit(
            'TEST', 'Investigator', creatable_visit_type[0]['id'], '170000' + str(patient_code), 'Done', '2024-10-10')
        self.visit_id = answer.get('id')

    def test_read_folder(self):
        instances = read_folder(
            "/home/salim/Téléchargements/DICOM_REALYSA_PET_CT_PET0_202200419918101220219", False)
        zip_dicoms(instances, 'dicom.zip')
        uploaded_url = self.gaelo_apis.upload_dicoms('dicom.zip')
        tus_id = uploaded_url.split('/')[-1]
        print(tus_id)
        self.gaelo_apis.validate_dicom_upload(
            self.visit_id, get_study_orthanc_id(instances[0]), [tus_id], len(instances))
        self.gaelo_apis.create_investigator_form(
            self.visit_id, {"comments": "abc"}, True)

import unittest
from faker import Faker
from dotenv import dotenv_values
from pygaelo.gaelo_client import GaelOClient

# @unittest.skip
class TestGaelO(unittest.TestCase):

    gaelo_apis: GaelOClient
    faker: Faker

    @classmethod
    def setUpClass(cls):
        config = dotenv_values(".env.dev")
        cls.gaelo_apis = GaelOClient()
        cls.gaelo_apis.set_url(config['GAELO_URL'])
        cls.gaelo_apis.login(config['GAELO_USERNAME'], config['GAELO_PASSWORD'])
        cls.user_id = cls.gaelo_apis.get_user_id()
        cls.faker = Faker()

    def test_get_studies(self):
        studies = self.gaelo_apis.get_user_studies()
        self.assertIsInstance(studies, list)

    def test_get_studies(self):
        roles = self.gaelo_apis.get_user_roles_in_study(self.user_id, 'TEST')
        self.assertIsInstance(roles, list)

    def test_get_visit_from_study(self):
        visits = self.gaelo_apis.get_visits_from_study('TEST', None, 'Investigator')
        self.assertIsInstance(visits, list)

    def test_get_possible_upload_visit(self):
        visits = self.gaelo_apis.get_possible_upload_visit('TEST')
        self.assertIsInstance(visits, list)

    def test_import_patient(self):
        patient_code = self.faker.pyint(10000000000000, 99999999999999)
        patient_firstname = self.faker.pystr(1, 1)
        patient_lastname = self.faker.pystr(1, 1)
        patient = {
            "code": str(patient_code),
            "firstname": patient_firstname,
            "lastname": patient_lastname,
            "centerCode": 0,
            "registrationDate": "2022-12-31",
            "inclusionStatus": "Included",
            "birthDay": None,
            "birthMonth": None,
            "birthYear":  None,
            "gender": "M",
            "investigatorName":  None
        }
        answer = self.gaelo_apis.import_patients(
            'TEST', 'Supervisor', [patient])
        self.assertIsInstance(answer, dict)

    def test_create_visit(self):
        patient_code = self.faker.pyint(10000000000000, 99999999999999)
        patient_firstname = self.faker.pystr(1, 1)
        patient_lastname = self.faker.pystr(1, 1)
        patient = {
            "code": str(patient_code),
            "firstname": patient_firstname,
            "lastname": patient_lastname,
            "centerCode": 0,
            "registrationDate": "2022-12-31",
            "inclusionStatus": "Included",
            "birthDay": None,
            "birthMonth": None,
            "birthYear":  None,
            "gender": "M",
            "investigatorName":  None
        }
        self.gaelo_apis.import_patients(
            'TEST', 'Supervisor', [patient])

        patient_id = '170000' + str(patient_code)
        creatable_visits_types = self.gaelo_apis.get_creatable_visits_types_of_patient(
            patient_id)
        creatable_visit_type = [
            visit for visit in creatable_visits_types if visit.get('name') == "CT0"]
        answer = self.gaelo_apis.create_visit(
            'TEST', 'Investigator', creatable_visit_type[0]['id'], '170000' + str(patient_code), 'Done', '2024-12-31')
        self.assertIsInstance(answer, dict)

    def test_delete_visit(self):
        patient_code = self.faker.pyint(10000000000000, 99999999999999)
        patient_firstname = self.faker.pystr(1, 1)
        patient_lastname = self.faker.pystr(1, 1)
        patient = {
            "code": str(patient_code),
            "firstname": patient_firstname,
            "lastname": patient_lastname,
            "centerCode": 0,
            "registrationDate": "2022-12-31",
            "inclusionStatus": "Included",
            "birthDay": None,
            "birthMonth": None,
            "birthYear":  None,
            "gender": "M",
            "investigatorName":  None
        }
        self.gaelo_apis.import_patients(
            'TEST', 'Supervisor', [patient])

        patient_id = '170000' + str(patient_code)
        creatable_visits_types = self.gaelo_apis.get_creatable_visits_types_of_patient(
            patient_id)
        creatable_visit_type = [
            visit for visit in creatable_visits_types if visit.get('name') == "CT0"]
        answer = self.gaelo_apis.create_visit(
            'TEST', 'Investigator', creatable_visit_type[0]['id'], '170000' + str(patient_code), 'Done', '2024-12-31')
        print(answer)
        self.gaelo_apis.delete_visit(answer.get('id'), 'TEST', 'Supervisor', 'testing delete visit pyGaelO')
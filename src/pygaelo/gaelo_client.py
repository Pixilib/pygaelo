from typing import List
from tusclient import client
import requests

from .model.types import Patient, QCDecision, VisitStatus


class GaelOClient:

    token: str
    user_id: int

    def set_url(self, url: str) -> None:
        self.url = url

    def login(self, login: str, password: str) -> str:
        payload = {
            "email": login,
            "password": password
        }
        response = requests.post(
            self.__get_url()+'/api/login', json=payload)
        response.raise_for_status()
        answer: dict = response.json()
        self.token = answer.get('access_token')
        self.user_id = answer.get('id')
        return answer

    def get_user_studies(self) -> dict:
        response = requests.get(
            self.__get_url()+'/api/users/'+str(self.user_id)+'/studies', headers=self.__get_headers())
        response.raise_for_status()
        return response.json()

    def get_user_roles_in_study(self, user_id: int, study_name: str) -> dict:
        response = requests.get(
            self.__get_url()+'/api/users/'+str(user_id)+'/roles?studyName='+study_name, headers=self.__get_headers())
        response.raise_for_status()
        return response.json()

    def import_patients(self, study_name: str, role: str, patients: List[Patient]):
        response = requests.post(
            self.__get_url()+'/api/studies/' + study_name + '/import-patients?role=' + role, headers=self.__get_headers(), json=patients)
        response.raise_for_status()
        return response.json()

    def get_visits_from_study(self, study_name: str, visit_type_id: int | None = None) -> dict:
        query_params = ''
        if (visit_type_id):
            query_params = '?visitType=' + visit_type_id
        response = requests.get(
            self.__get_url()+'/api/studies/'+study_name+'/visits' + query_params, headers=self.__get_headers())
        response.raise_for_status()
        return response.json()

    def create_visit(self, study_name: str, role: str, visit_type_id: int, patient_id: str, statusDone: VisitStatus, visit_date: str | None, reason_for_not_done: str | None = None) -> dict:
        payload = {
            "patientId": patient_id,
            "visitDate": visit_date,
            "statusDone": statusDone,
            "reasonForNotDone": reason_for_not_done
        }

        response = requests.post(
            self.__get_url()+'/api/visit-types/'+str(visit_type_id)+'/visits?role=' + role + '&studyName=' + study_name, headers=self.__get_headers(), data=payload)
        response.raise_for_status()
        return response.json()

    def get_visit_tree(self, study_name: str, role: str) -> dict:
        response = requests.get(self.__get_url()+'/api/studies/' + study_name +
                                '/visits-tree?role=' + role, headers=self.__get_headers())
        response.raise_for_status()
        return response.json()

    def get_creatable_visits_types_of_patient(self, patient_id: str) -> dict:
        response = requests.get(self.__get_url(
        )+'/api/patients/' + patient_id + '/creatable-visits', headers=self.__get_headers())
        response.raise_for_status()
        return response.json()

    def get_possible_upload_visit(self, study_name: str) -> dict:
        response = requests.get(
            self.__get_url()+'/api/studies/' + study_name + '/possible-uploads', headers=self.__get_headers())
        response.raise_for_status()
        return response.json()

    def upload_dicoms(self, zip_path: str) -> str:
        my_client = client.TusClient(self.__get_url()+'/api/tus',
                                     headers=self.__get_headers())
        uploader = my_client.uploader(zip_path, chunk_size=2000000)
        uploader.upload()
        upload_id = uploader.url.split('/')[-1]
        return upload_id

    def validate_dicom_upload(self, visit_id: int, original_orthanc_id: str, tus_upload_ids: list[str], number_of_uploaded_instances: int):
        payload = {
            "originalOrthancId": original_orthanc_id,
            "uploadedFileTusId": tus_upload_ids,
            "numberOfInstances": number_of_uploaded_instances
        }
        response = requests.post(
            self.__get_url()+'/api/visits/' + str(visit_id) + '/validate-dicom', headers=self.__get_headers(), json=payload)
        response.raise_for_status()

    def create_investigator_form(self, visit_id: int, data: dict, validated: bool):
        payload = {
            "data": data,
            "validated": validated
        }
        response = requests.post(
            self.__get_url()+'/api/visits/' + str(visit_id) + '/investigator-form', headers=self.__get_headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def update_quality_control(self, visit_id: int, study_name: str, state_qc: QCDecision, image_qc_validation: bool, form_qc_validation: bool, image_qc_comment: str, from_qc_comment: str):
        payload = {
            "stateQc": state_qc,
            "imageQc": image_qc_validation,
            "formQc": form_qc_validation,
            "imageQcComment": image_qc_comment,
            "formQcComment": from_qc_comment
        }

        response = requests.patch(
            self.__get_url()+'/api/visits/' + str(visit_id) + '/quality-control?studyName=' + str(study_name), json=payload)
        response.raise_for_status()
        return response.json()

    def get_user_id(self) -> int | None:
        return self.user_id

    def __get_url(self):
        return self.url

    def __get_headers(self):
        return {'Authorization': 'Bearer '+self.token}

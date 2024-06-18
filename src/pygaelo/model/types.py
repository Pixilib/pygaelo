from enum import Enum
from typing import TypedDict


class Patient(TypedDict):
    code: str | None
    firstname: str | None
    lastname: str | None
    centerCode: int | None
    registrationDate: str | None
    inclusionStatus: str
    birthDay: int | None
    birthMonth: int | None
    birthYear: int | None
    gender: str | None
    investigatorName: str | None


class QCDecision(Enum):
    ACCEPTED = 'Accepted'
    REFUSED = 'Refused'
    CORRECTIVE_ACTION_ASKED = 'Corrective Action Asked'

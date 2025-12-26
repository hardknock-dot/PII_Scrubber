from enum import Enum


class IdentifierType(str, Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    NAME = "NAME"
    ADDRESS = "ADDRESS"
    DATE_OF_BIRTH = "DOB"
    PROVIDER = "PROVIDER"
    APPOINTMENT_ID = "APPT_ID"
    INSURANCE_ID = "INSURANCE_ID"
    GOVERNMENT_ID = "GOV_ID"
    URL = "URL"

from pydantic import BaseModel, EmailStr,AnyUrl,Field , field_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    email : EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    linkedin_url: AnyUrl

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com','icici.com','sbi.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Invalid email domain: {domain_name}. Allowed domains are: {', '.join(valid_domains)}")
        
        return value

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        value = value.upper()
        return value

def Patient_insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")
    


def Patient_update(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")


patient_data = {
    "name": "yuvaraj",
    "email":"yuvarajvanjari2@sbi.com",
    "age": 1,
    "weight": 83.2,
    "married": False,
    "allergies": ["pollen", "dust"],
    "contact_details" : {"phone":"9392716766"},
    "linkedin_url": "http://linkedin.com/ yuvarajkaleru"
}

patient1 = Patient(**patient_data)

Patient_insert(patient1)
Patient_update(patient1)

from pydantic import BaseModel, EmailStr,AnyUrl,Field
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    email : EmailStr
    age: int = Field(gt=0)
    weight: float
    married: Optional[bool] = None
    allergies: List[str]
    contact_details: Dict[str, str]
    linkedin_url: AnyUrl


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
    "email":"yuvarajvanjari2@gmail.com",
    "age": 1,
    "weight": 83.2,
    "married": None,
    "allergies": ["pollen", "dust"],
    "contact_details" : {"phone":"9392716766"},
    "linkedin_url": "http://linkedin.com/ yuvarajkaleru"
}

patient1 = Patient(**patient_data)

Patient_insert(patient1)
Patient_update(patient1)

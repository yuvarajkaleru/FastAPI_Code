from pydantic import BaseModel, EmailStr,AnyUrl,Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50,title="Patient Name", description="Name of the patient")]
    email : EmailStr = Field(...)
    age: int = Field(gt=0)
    weight: Annotated[float, Field(gt=0, description="Weight of the patient in kg",strict=True)]
    married: Annotated[bool, Field(default=None, description="Married status of the patient")]
    allergies: List[str] = Field(max_length=5)
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
    
    "allergies": ["pollen", "dust","","",""],
    "contact_details" : {"phone":"9392716766"},
    "linkedin_url": "http://linkedin.com/ yuvarajkaleru"
}

patient1 = Patient(**patient_data)

Patient_insert(patient1)
Patient_update(patient1)

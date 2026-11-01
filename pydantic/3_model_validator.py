from pydantic import BaseModel , EmailStr , model_validator
from typing import List , Dict

class Patient(BaseModel):
    name: str
    email : EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError("Emergency contact is required for patients over 60 years old.")
        return model

def update_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("updated")

patient_info = {
    "name": "yuvaraj","email":"yuvarajvanjari2@sbi.com","age": 61,"weight": 83.2,"married": False,"allergies": ["pollen","dust"],"contact_details" : {"phone":"9392716766","emergency_contact":"9000386595"},
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

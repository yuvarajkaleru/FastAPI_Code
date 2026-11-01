from pydantic import BaseModel , EmailStr , computed_field
from typing import List , Dict

class Patient(BaseModel):
    name: str
    email : EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/self.height**2,2)



def update_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("BMI :",patient.bmi)
    print("updated")

patient_info = {
    "name": "yuvaraj","email":"yuvarajvanjari2@sbi.com","age": 61,"weight": 75.2,"height" : 1.72,"married": False,"allergies": ["pollen","dust"],"contact_details" : {"phone":"9392716766","emergency_contact":"9000386595"}
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

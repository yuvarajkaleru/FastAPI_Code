import json
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
class Patient(BaseModel):
    id : Annotated[str,Field(..., description= "ID of the patient",examples=["P001","P002"])]
    name : Annotated[str,Field(..., description="Name of the patient")]
    city : Annotated[str,Field(..., description="City where the patient is living")]
    age : Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender : Annotated[Literal['male','female','others'],Field(..., description="Gender of the Patient")]
    height : Annotated[float,Field(...,gt=0,description="Height of patient in meters")]
    weight : Annotated[float,Field(...,gt=0,description="Weight of patient in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/self.height**2,2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str],Field(default=None)]
    age : Annotated[Optional[int],Field(default=None,gt=0)]
    gender : Annotated[Optional[str],Literal['male','female'], Field(default=None)]
    height : Annotated[Optional[float],Field(default=None,gt=0)]
    weight : Annotated[Optional[float],Field(default=None,gt=0)]

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message": "patient management system API"}


@app.get("/about")
def about():
    return {"message": "This is a FastAPI application for patient management."}


@app.get("/view")
def view():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ..., description="The ID of the patient to retrieve", example="P001"
    )
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/patient")
def patient():
    data = load_data()
    names = [patient["name"] for patient in data.values()]
    for p in data.values():
        names.append(p["name"])
    return {"names": names}


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ..., description="The field to sort by (height, weight, bmi)", example="height"
    ),
    order: str = Query(
        "asc", description="The order of sorting (asc or desc)", example="asc"
    ),
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Valid fields are: {valid_fields}",
        )

    valid_orders = ["asc", "desc"]

    if order not in valid_orders:
        raise HTTPException(
            status_code=400, detail="Invalid order. Valid orders are: asc, desc"
        )

    data = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(
        data.values(),
        key=lambda patient: patient[sort_by],
        reverse=sort_order,
    )

    return sorted_data


@app.get("/search")
# Search for a patient by name or ID
def search_patient(
    name: str = Query(
        ..., description="The name of the patient to search for", example="John Doe"
    ),
    patient_id: str = Query(
        ..., description="The ID of the patient to search for", example="P001"
    )
):
    data = load_data()
    results = []
    for patient in data.values():
        if name.lower() in patient["name"].lower() or patient_id == patient["id"]:
            results.append(patient)
        else: 
            HTTPException(status_code=404, detail="Patient not found")
    return results

@app.post('/create')
def create_patient(patient : Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient Already Exists")

    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201,content = {'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id : str,patient_update:PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value


    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'Patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200,content="patient deleted")
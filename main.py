import json

from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {"message": "patient management system API"}


@app.get("/about")
def about():
    return {"message": "This is a FastAPI application for patient management."}


@app.get("/view")
def view():
    data = load_data()
    return data


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
    names.reverse()
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
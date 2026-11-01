from pydantic import BaseModel

class Address(BaseModel):
    city : str
    pin : int
    state : str



class Patient(BaseModel):
    name : str
    age : str
    gender : str
    address : Address

address_data = {"city":"Uppal" , "pin":500039 , "state": "Telangana"}
address1 = Address(**address_data)

patient_data = {"name":"Yuvaraj","age":"20","gender":"Male","address" : address1}
patient1 = Patient(**patient_data)

data1 = patient1.model_dump(include=["name","address"])
data1 = patient1.model_dump(exclude={"address":["state"]})
data2 = patient1.model_dump_json()
print(data1)
print(data2)

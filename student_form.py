from pymongo import MongoClient
from fastapi import FastAPI, status,Body,HTTPException
from pydantic import BaseModel,Field as PydanticField
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from bson import ObjectId

app = FastAPI()

DB = "slack"
MSG_COLLECTION = "student_form"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Message class defined in Pydantic
class Message(BaseModel) :
    id: PyObjectId = PydanticField(default_factory=PyObjectId, alias="_id")
    Roll_number:int=None
    Name: str=None
    Address:str=None
    Mobile_number:int=None
    Branch:str=None
    State:str=None
    Country:str=None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                    "Roll_number": 14,
                    "Name": "prasad",
                    "Address": "rajahmundry, handa satram street,9-14-46,east godavari district",
                    "Mobile_number": 9701750369,
                    "Branch": "ACE",
                    "State": "AP",
                    "Country": "india",
                }
        }

class UpdateMessage(BaseModel):
    Roll_number: Optional[int]
    Name: Optional[str]
    Address: Optional[str]
    Mobile_number: Optional[int]
    Branch:Optional[str]
    Country:Optional[str]
    State:Optional[str]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                    "Roll_number": 14,
                    "Name": "prasad",
                    "Address": "rajahmundry, handa satram street,9-14-46,east godavari district",
                    "Mobile_number": 9701750369,
                    "Branch": "ACE",
                    "State": "AP",
                    "Country": "india",
                }
        }

# Instantiate the FastAPI

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/students_list")
def get_messages():
    """Get all messages for the specified channel."""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        msg_list = msg_collection.find()
        response_msg_list = []
        for msg in msg_list:
            response_msg_list.append(Message(**msg))
        return response_msg_list


@app.get( "/student_data", response_model=Message)
def show_student(id: str):
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
    if (student :=msg_collection.find_one({"_id": ObjectId(id)})) is not None:
        return student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.post("/post_student_details", status_code=status.HTTP_201_CREATED)
def post_message(message: Message):
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(message.dict())
        ack = result.acknowledged
        return {"insertion": ack}

@app.put("/update_student_details", response_description="Update a student", response_model=Message)
def update_student(id: str, student: UpdateMessage = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
    if len(student) >= 1:
        update_result = msg_collection.update_one({"_id": ObjectId(id)}, {"$set": student})
        if update_result.modified_count == 1:
            if (
                updated_student := msg_collection.find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_student
    if (existing_student := msg_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/delete_student_details", status_code=status.HTTP_201_CREATED) 
def delete_student(Roll_number: int):
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
    student =  msg_collection.find_one({"Roll_number": Roll_number})
    if student:
         msg_collection.delete_one({"Roll_number": Roll_number})
    return True
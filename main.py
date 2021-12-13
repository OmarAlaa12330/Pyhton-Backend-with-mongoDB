from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient, mongo_client
from fastapi.middleware.cors import CORSMiddleware


DB ='todo-application'
COLLECTION = 'todos'

class ToDoModel(BaseModel):
    title:str
    done:bool

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods =["*"],
    allow_headers=["*"]
)

@app.get("/")
def get_status():
    """get server status"""
    return{"server":"running"}



@app.post("/todo")
def create_todo(todo:ToDoModel):
    """create a new ToDo """
    with MongoClient() as client:
        todo_collection = client[DB][COLLECTION]
        result = todo_collection.insert_one(todo.dict())
        ack = result.acknowledged
        return {
            "insertion": ack,
            "object":todo.dict()
        }


@app.get("/todo")
def read_todo():
    """get all the todo's as a list"""
    with MongoClient() as client:
        todo_collection = client[DB][COLLECTION]
        todos = todo_collection.find()
        responses =[]
        for todo in todos:
            responses.append((ToDoModel(**todo)))
        return responses


@app.put("/todo")
def check_todo (title:str,todo:ToDoModel):
    """Sets a todo item from not done to done"""
    with MongoClient as client:
        todo_collection = client[DB][COLLECTION]
        result = todo_collection.update_one({"title":title},{"$set":todo.dict()})
        ack = result.acknowledged
        return {"Edited":ack}




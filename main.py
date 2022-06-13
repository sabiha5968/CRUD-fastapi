from fastapi import FastAPI,status,HTTPException
from database import Base, engine, ToDo
from pydantic import BaseModel
from sqlalchemy.orm import Session



class ToDoRequest(BaseModel):
    task:str

Base.metadata.create_all(engine)


app=FastAPI()

@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_todo(todo:ToDoRequest):
    session=Session(bind=engine,expire_on_commit=False)


    tododb=ToDo(task=todo.task)

    session.add(tododb)
    session.commit()

    id=tododb.id


    session.close()

    return f"created todo item with id {id}"



@app.get("/")
def root():

    session=Session(bind=engine,expire_on_commit=False)

    todo_list=session.query(ToDo).all()
    session.close()

    return todo_list


@app.post("/todo",status_code=status.HTTP_201_CREATED)
def post_root(todo:ToDoRequest):

    session=Session(bind=engine, expire_on_commit=False)

    tododb=ToDo(task= todo.task)
    session.add(tododb)
    session.commit()
    id= tododb.id
    session.close()
    return f"create todo item with id '{id}'"

@app.get("/todo/{id}")
def read_root(id:int):

    session=Session(bind=engine, expire_on_commit=False)

    todo=session.query(ToDo).get(id)

    session.close()

    if not todo:
        raise HTTPException(status_code=404,detail=f"todo item with id {id} not found")
    return todo

@app.put("/todo/{id}")
def update_root(id:int,task:str):
    session=Session(bind=engine,expire_on_commit=False)

    todo=session.query(ToDo).get(id)

    if todo:
        todo.task=task
        session.commit()

    session.close()
    if not todo:
        raise HTTPException(status_code=404,detail=f"todo item with id {id} not found")


    return todo



@app.delete("/todo/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_root(id:int):

    session=Session(bind=engine,expire_on_commit=False)

    todo=session.query(ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404,detail=f"todo item with {id} not found")
    return None


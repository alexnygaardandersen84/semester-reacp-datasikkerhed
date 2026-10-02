from fastapi import FastAPI, HTTPException
from entities.task import Task
from entities.user import User, UserResponse

import database
from bcrypt_hashing import hash_password, verify_password
# bcrypt_hashing.hash.... - hvis nu man ikke importer liberariet


app = FastAPI(title="Python API", version="1.0.0")

database.initialize_database()

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    connection = database.connect()
    try:
        with connection:
            
            dbresult = connection.execute(
                "SELECT title, description FROM tasks"
            )
            tasks = [
                Task(title=row[0], description=row[1])
                for row in dbresult.fetchall()
            ]
            return tasks
    finally:
        connection.close()


@app.post("/tasks")
def create_task(payload: Task):
    connection = database.connect()
    try:
        with connection:
            connection.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (payload.title, payload.description),
            )
    finally:
        connection.close()
    return "All done"


@app.post("/users")
def create_user(payload: User):
    try:
        password_hash = hash_password(payload.password)
    except ValueError:
        raise HTTPException(422, "Password cannot be hashed")
    connection = database.connect()
    try:
        with connection:
            connection.execute(
                "INSERT INTO users (username, passwordHash) VALUES (?, ?)",
                (payload.username, password_hash),
            )
    finally:
        connection.close()
    return "All done"



@app.get("/users", response_model=list[UserResponse])
def get_users():
    connection = database.connect()
    try:
        with connection:
            
            dbresult = connection.execute(
                "SELECT username FROM users"
            )
            users = [
                UserResponse(username=row[0])
                for row in dbresult.fetchall()
            ]
            return users
    finally:
        connection.close()




@app.post("/login")
def login(data: User):
    connection = database.connect()
    try:
        dbResult = connection.execute(
            "SELECT username, passwordHash FROM users "
            "WHERE username = ?",
            (data.username,),
        ).fetchone()
    finally:
        connection.close()
    
    if dbResult is None:
        raise HTTPException(401, "Invalid credentials")
    
    try:
        password_matches = verify_password(data.password, dbResult[1])
    except ValueError:
        password_matches = False
    if not password_matches:
        raise HTTPException(401, "Invalid credentials")
    return {"message": "Login successful"}

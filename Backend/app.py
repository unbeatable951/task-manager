from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_connection, init_db

app = FastAPI()
pwd = CryptContext(schemes=["bcrypt"])

# Allow the HTML files (opened from file://) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Run once on startup ───────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    init_db()

# ── Request / Response schemas ────────────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    completed: bool

# ── Auth endpoints ────────────────────────────────────────────────────────
@app.post("/register")
def register(data: RegisterRequest):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data.username, pwd.hash(data.password))
        )
        conn.commit()
        return {"message": "User created successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Username already taken")
    finally:
        conn.close()

@app.post("/login")
def login(data: LoginRequest):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (data.username,)
    ).fetchone()
    conn.close()

    if not user or not pwd.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return the user id so the frontend knows who is logged in
    return {"user_id": user["id"], "username": user["username"]}

# ── Task endpoints ────────────────────────────────────────────────────────
@app.get("/tasks/{user_id}")
def get_tasks(user_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return [{"id": r["id"], "title": r["title"], "completed": bool(r["completed"])} for r in rows]

@app.post("/tasks/{user_id}")
def add_task(user_id: int, data: TaskCreate):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (user_id, title, completed) VALUES (?, ?, 0)",
        (user_id, data.title)
    )
    conn.commit()
    conn.close()
    return {"message": "Task added"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    conn = get_connection()
    conn.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (1 if data.completed else 0, task_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted"}
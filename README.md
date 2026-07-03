# ✅ Task Manager

A full-stack task management web app built with **HTML/CSS/JS** on the frontend and **Python FastAPI + SQLite** on the backend.

---

## 📸 Features

- 🔐 User Registration and Login
- ➕ Add tasks with a title
- ✅ Mark tasks as Complete or Pending
- 🗑️ Delete tasks
- 🔍 Filter tasks — All / Pending / Completed
- 💾 Submit all changes at once
- 📊 Live stats — Total, Completed, Pending count
- 💡 Data saved in SQLite database (persists after refresh)

---

## 🗂️ Project Structure

```
task-manager/
├── backend/
│   ├── app.py          # FastAPI server — all API endpoints
│   └── database.py     # SQLite setup and connection
├── frontend/
│   ├── index.html      # Login and Register page
│   └── tasks.html      # Task dashboard
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Backend | Python, FastAPI |
| Database | SQLite (via Python sqlite3) |
| Server | Uvicorn (ASGI) |
| Auth | Passlib bcrypt password hashing |

---
## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Create a new user account |
| POST | `/login` | Login and get user ID |
| GET | `/tasks/{user_id}` | Get all tasks for a user |
| POST | `/tasks/{user_id}` | Add a new task |
| PUT | `/tasks/{task_id}` | Update task (complete/incomplete) |
| DELETE | `/tasks/{task_id}` | Delete a task |

---

## 🗄️ Database Schema

**users table**
```sql
CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE NOT NULL,
    password TEXT    NOT NULL
);
```

**tasks table**
```sql
CREATE TABLE tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    title     TEXT    NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 📖 How It Works

```
Browser (index.html / tasks.html)
        ↕  HTTP requests (fetch API)
FastAPI server (app.py on port 8000)
        ↕  SQL queries
SQLite database (tasks.db)
```

1. User registers/logs in → `user_id` saved in `localStorage`
2. Tasks page fetches tasks for that `user_id` from the API
3. Checkbox toggles are staged locally first
4. Clicking **Submit All Changes** sends PUT requests to save to DB
5. SQLite stores everything in `tasks.db` inside the `backend/` folder

---

## ⚙️ Requirements

- Python 3.8+
- VS Code with **Live Server** extension (by Ritwick Dey)
- Modern browser (Chrome, Firefox, Edge)

---

## 👤 Author

**Your Name**  
GitHub: Diksha Singh

---

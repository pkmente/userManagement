# Task Management System

## Project Overview

**Project Name:** `userManagement`  
**Apps:**
- **accounts** - Handles authentication, authorization, and user ownership.
- **tasks** - Manages task CRUD operations, filtering, and exporting task data to CSV.

---

## Authentication in Accounts

- The authentication system uses **JWT (JSON Web Tokens)**.
- After logging in, a token is generated.
- The token must be included in the headers of all API requests for authentication.

---

## Task Management APIs

### **1️⃣ Task Creation**
- **Endpoint:** `POST http://127.0.0.1:8000/tasks/tasks/create/`
- Allows users to create tasks with:
  - `user_id`
  - `title`
  - `description`
  - `priority`
  - `assignee`
  - `status`

### **2️⃣ Read Task List**
- **Endpoint:** `GET http://127.0.0.1:8000/tasks/tasks/`
- Fetches all tasks with their details.

### **3️⃣ Update Task**
- **Endpoint:** `PUT http://127.0.0.1:8000/tasks/tasks/<task_id>/update/`
- Updates the task with the given `task_id`.

### **4️⃣ Delete Task**
- **Endpoint:** `DELETE http://127.0.0.1:8000/tasks/tasks/<task_id>/delete/`
- Deletes the task with the given `task_id`.

### **5️⃣ Task Filtering by Due Date**
- **Endpoint:** `GET http://127.0.0.1:8000/tasks/tasks/filt`
- Filters tasks based on their due date.

### **6️⃣ Export Tasks to CSV**
- **Endpoint:** `GET http://127.0.0.1:8000/tasks/tasks/export/`
- Exports the task list to a CSV file.

---

## Additional Features

### **Redis Cache**
- Used to store and manage frequently accessed data.
- Cache is updated when tasks are modified or deleted.

### **Celery Module**
- Celery is integrated to handle background tasks asynchronously.
- It replaces traditional **sendMail** operations.

### **JWT Authentication**
- Secure authentication using **JSON Web Tokens (JWT)**.
- Required for all API requests.

---

## Technologies Used

- **Django** - Web framework
- **Django REST Framework** - API handling
- **PostgreSQL / SQLite** - Database
- **Redis** - Caching
- **Celery** - Asynchronous task queue
- **JWT (JSON Web Tokens)** - Authentication

---

## How to Run the Project

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/pkmente/userManagement.git
cd userManagement

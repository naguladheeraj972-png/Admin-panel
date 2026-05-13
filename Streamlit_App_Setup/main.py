from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ---------------- Demo Data ----------------
attendance_data = [
    {"employee_id": 1, "name": "Alice", "status": "Present"},
    {"employee_id": 2, "name": "Bob", "status": "Absent"},
    {"employee_id": 3, "name": "Charlie", "status": "Late"},
]

employees_data = [
    {"employee_id": 1, "name": "Alice", "department": "HR", "email": "alice@example.com"},
    {"employee_id": 2, "name": "Bob", "department": "IT", "email": "bob@example.com"},
    {"employee_id": 3, "name": "Charlie", "department": "Finance", "email": "charlie@example.com"},
]

# ---------------- Models ----------------
class Employee(BaseModel):
    name: str
    department: str
    email: str

# ---------------- Endpoints ----------------

@app.get("/attendance")
def get_attendance():
    """Return demo attendance data"""
    return attendance_data

@app.get("/employees")
def get_employees():
    """Return demo employee list"""
    return employees_data

@app.post("/employees")
def add_employee(employee: Employee):
    """Add a new employee (demo only, no DB yet)"""
    new_id = len(employees_data) + 1
    new_employee = {
        "employee_id": new_id,
        "name": employee.name,
        "department": employee.department,
        "email": employee.email,
    }
    employees_data.append(new_employee)
    return {"message": "Employee added successfully", "employee": new_employee}

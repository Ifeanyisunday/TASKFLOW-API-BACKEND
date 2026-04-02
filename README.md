📘 TaskFlow API Documentation
🧩 Project Overview

TaskFlow API is a secure task management backend built with Django REST Framework.
It supports:

User authentication (JWT)
Task creation, update, deletion
Per-user data isolation (no cross-user access)
Filtering, searching, and ordering tasks
⚙️ Tech Stack
Python 3.x
Django
Django REST Framework
JWT Authentication (SimpleJWT)
SQLite (default, can switch to PostgreSQL)
Pytest (testing)

📁 Project Structure
TaskFlow-Api/
│
├── project_settings/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── tasks/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── pytest.ini
└── README.md


🚀 Setup Instructions 
1. Clone the repository
git clone <https://github.com/Ifeanyisunday/TASKFLOW-API-BACKEND.git>
cd TaskFlow-Api

2. Create virtual environment
pip install pipenv 
pipenv install

to activate virtual envronment
pipenv shell

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables

Create a .env file:

cp .env.example .env
5. Run migrations
python manage.py makemigrations
python manage.py migrate
6. Create superuser (optional)
python manage.py createsuperuser
7. Run the server
python manage.py runserver

Server runs at:

http://127.0.0.1:8000/
8. Run tests
pytest -v
🔐 Authentication (JWT)

All protected routes require:

Authorization: Bearer <access_token>
📡 API Endpoints
🔑 Auth Endpoints
✅ Register
POST /api/users/register/

Body

{
  "email": "user@example.com",
  "username": "testuser",
  "password": "StrongPass123"
}
✅ Login
POST /api/users/login/

Body

{
  "email": "user@example.com",
  "password": "StrongPass123"
}

Response

{
  "message": "Login successful",
  "tokens": {
    "access": "...",
    "refresh": "..."
  }
}
✅ Logout
POST /api/users/logout/

Body

{
  "refresh": "your_refresh_token"
}
📝 Task Endpoints
✅ Create Task
POST /api/tasks/

Headers

Authorization: Bearer <token>

Body

{
  "title": "My Task",
  "description": "Task details",
  "priority": "high",
  "status": "todo",
  "due_date": "2026-04-10T00:00:00Z"
}
✅ Get All Tasks (User only)
GET /api/tasks/
🔍 Filtering
GET /api/tasks/?status=todo&priority=high
🔎 Search
GET /api/tasks/?search=meeting
↕️ Ordering
GET /api/tasks/?ordering=due_date
GET /api/tasks/?ordering=-created_at
✅ Get Single Task
GET /api/tasks/{id}/
✅ Update Task
PATCH /api/tasks/{id}/

Body

{
  "status": "in-progress"
}
✅ Delete Task
DELETE /api/tasks/{id}/
🔒 Security Features Implemented
✅ Password Hashing
Uses Django’s set_password() (bcrypt compatible)
✅ JWT Authentication
Secure token-based authentication using SimpleJWT
✅ Per-User Data Isolation
Users can only access their own tasks:
def get_queryset(self):
    return Task.objects.filter(user=self.request.user)
✅ Object-Level Permission
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
✅ Input Validation
DRF serializers validate all incoming data
⚠️ Common Issues & Fixes
❌ 404 / Reverse errors
Ensure URLs are included properly:
path("api/users/", include("users.urls")),
path("api/tasks/", include("tasks.urls")),
❌ Logout error (APPEND_SLASH)

Always use:

/api/users/logout/
❌ 400 on PATCH
Ensure serializer allows partial updates:
partial=True
🌱 Environment Variables (.env.example)
SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_URL=sqlite:///db.sqlite3

JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_LIFETIME=60
JWT_REFRESH_LIFETIME=1
🧪 Testing

Run:

pytest -v

Tests cover:

Auth (register, login, logout)
Task CRUD
User isolation
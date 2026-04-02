TaskFlow API

TaskFlow API is a Django REST Framework project for managing tasks. Users can register, log in, create, update, and delete tasks. Only the task owner can access their own tasks. JWT authentication is used.

1. Features
User registration, login, logout (JWT-based)
Passwords hashed using Django's built-in mechanisms (bcrypt)
JWTs signed & validated
Per-user task access (no cross-user leakage)
Task CRUD with filtering, searching, and ordering
Timezone-aware due_date
Input validation and error handling



2. Setup Instructions (Fresh Machine)
2.1 Clone the repository
git clone <your-repo-url>
cd TaskFlow-Api


3. Create and activate virtual environment
using pipenv

pip install pipenv
pipenv install django
pipenv shell
python manage.py runserver


4. Folder Structure 

TaskFlow-Api/
├─ manage.py
├─ requirements.txt
├─ README.md
├─ project_settings/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ users/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ urls.py
│  ├─ views.py
│  └─ tests.py
├─ tasks/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  ├─ permissions.py
│  ├─ urls.py
│  └─ tests.py
└─ db.sqlite3


5. Api Endpoints Documentation

| Method | URL                  | Description                      |
| ------ | -------------------- | -------------------------------- |
| POST   | /api/users/register/ | Register a new user              |
| POST   | /api/users/login/    | Login and receive JWT tokens     |
| POST   | /api/users/logout/   | Logout (blacklist refresh token) |

| Method | URL                   | Description                             |
| ------ | --------------------- | --------------------------------------- |
| GET    | /api/tasks/           | List tasks (only your tasks)            |
| POST   | /api/tasks/           | Create a new task                       |
| PATCH  | /api/tasks/{id}/      | Update your task                        |
| DELETE | /api/tasks/{id}/      | Delete your task                        |
| GET    | /api/tasks/?search=   | Search tasks by title/description       |
| GET    | /api/tasks/?status=   | Filter by status                        |
| GET    | /api/tasks/?priority= | Filter by priority                      |
| GET    | /api/tasks/?ordering= | Order by due_date, priority, created_at |

6. Run tests
pytest -v

7. Using Sqlite
python manage.py makemigrations
python manage.py migrate
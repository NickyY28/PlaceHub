# PlaceHub - Placement Portal Application V2

PlaceHub is a role-based Placement Portal Application designed to manage campus recruitment activities between institutes, companies, and students.

The application provides separate dashboards and functionalities for Admin, Companies, and Students. It simplifies company approvals, placement drive management, student applications, application tracking, and placement activity reporting.

This project is developed as part of the **Modern Application Development II (MAD-II)** course.

## Features

### Admin

- Pre-existing Admin account
- Secure Admin login
- Admin dashboard with system statistics
- View total users, students, companies, placement drives, and applications
- View and manage registered users
- View registered companies
- Approve or reject company registrations
- View registered students
- Block and unblock users
- Delete users
- View and manage placement drives
- Delete placement drives
- View student applications
- Generate Monthly Placement Activity Reports
- Monthly reports generated asynchronously using Celery
- Download generated reports in HTML format

### Company

- Company registration and login
- Company profile management
- Admin approval required for registered companies
- Company dashboard
- Create placement drives
- View created placement drives
- View student applications
- View student details such as college and CGPA
- Manage applications for placement drives
- Update application status
- Application statuses include:
  - Applied
  - In Touch
  - Shortlisted
  - Rejected

### Student

- Student registration and login
- Student dashboard
- View and update student profile
- View available placement drives
- Apply for placement drives
- Prevention of duplicate applications
- View application status
- View application history
- Export placement application history as CSV
- CSV export runs asynchronously using Celery and Redis
- Download generated CSV file

## Background Jobs

PlaceHub uses **Celery and Redis** for asynchronous background processing.

### Student Application CSV Export

Students can export their placement application history as a CSV file.

The export process runs as a background Celery task and generates a CSV file containing application-related information such as:

- Student ID
- Company Name
- Placement Drive Title
- Application Status
- Application Date

The frontend periodically checks the Celery task status. Once the background task is completed, the generated CSV file is automatically downloaded.

### Monthly Placement Activity Report

The Admin can generate a Monthly Placement Activity Report.

The report is generated asynchronously using Celery and contains placement statistics such as:

- Total Students
- Total Companies
- Total Placement Drives
- Total Applications
- Placement Drives created during the current month
- Applications submitted during the current month
- Shortlisted Applications
- Rejected Applications

The generated report is saved as an HTML file and can be downloaded by the Admin.

## Tech Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Celery
- Redis
- SQLite

### Frontend

- Vue.js
- Vue Router
- Pinia
- Axios
- Bootstrap
- Bootstrap Icons

## Authentication and Authorization

PlaceHub uses JWT-based authentication for secure API access.

The application supports three roles:

- Admin
- Company
- Student

Role-based authorization ensures that users can only access APIs and pages permitted for their role.

Custom decorators are used on the backend for role-based access control.

Example:

```python
@jwt_required()
@admin_required
def admin_route(user):
    pass
```

```python
@jwt_required()
@student_required
def student_route(user):
    pass
```

## Project Structure

```text
PlaceHub/
│
├── backend/
│   ├── api/
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── student_tasks.py
│   │   └── admin_tasks.py
│   │
│   ├── utils/
│   │
│   ├── exports/
│   │
│   ├── reports/
│   │
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── seed.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │
│   │   ├── components/
│   │   │   └── common/
│   │   │
│   │   ├── pages/
│   │   │   ├── admin/
│   │   │   ├── auth/
│   │   │   ├── company/
│   │   │   └── student/
│   │   │
│   │   ├── router/
│   │   ├── stores/
│   │   ├── App.vue
│   │   └── main.js
│   │
│   └── package.json
│
└── README.md
```

## Database Models

The application uses SQLite with SQLAlchemy ORM.

The main database models are:

### User

Stores common user information and identifies users by their role.

Roles:

- Admin
- Company
- Student

### CompanyProfile

Stores company-specific information such as:

- Company Name
- Website
- Location
- Description
- Approval Status

### StudentProfile

Stores student-specific information such as:

- College
- CGPA
- Skills
- Resume

### PlacementDrive

Stores placement drive information such as:

- Company
- Job Title
- Description
- Package
- Location
- Application Deadline
- Eligibility Criteria

### Application

Stores student placement applications including:

- Student
- Placement Drive
- Application Status
- Application Date

## Application Workflow

```text
Company Registration
        |
        v
Admin Approval
        |
        v
Company Accesses Placement Features
        |
        v
Company Creates Placement Drive
        |
        v
Students View Available Drives
        |
        v
Student Applies for Drive
        |
        v
Company Reviews Applications
        |
        v
Company Updates Application Status
        |
        v
Student Tracks Application Status
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NickyY28/PlaceHub
cd PlaceHub
```

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Start the Flask backend:

```bash
python app.py
```

The Flask API will be available at:

```text
http://127.0.0.1:5000
```

## Redis Setup

Redis is required as the message broker and result backend for Celery background tasks.

### Install Redis on macOS

Using Homebrew:

```bash
brew install redis
```

Start Redis as a background service:

```bash
brew services start redis
```

Check whether Redis is running:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

Alternatively, Redis can be started manually using:

```bash
redis-server
```

## Celery Worker Setup

The Celery worker is required for background tasks such as:

- Student CSV Export
- Admin Monthly Activity Report

Open a new terminal.

Navigate to the backend directory:

```bash
cd backend
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the Celery worker:

```bash
celery -A app.celery worker --loglevel=info
```

The worker should register tasks such as:

```text
tasks.student_tasks.export_student_applications
tasks.admin_tasks.generate_monthly_report
```

The Celery worker must remain running while using background job features.

## Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install Node.js dependencies:

```bash
npm install
```

Start the Vue development server:

```bash
npm run dev
```

Open the frontend URL displayed in the terminal.

## Running the Complete Application

For all PlaceHub features to work correctly, the following services should be running:

1. Flask Backend
2. Vue Frontend
3. Redis Server
4. Celery Worker

### Terminal 1 - Backend

```bash
cd backend
source .venv/bin/activate
python app.py
```

### Terminal 2 - Celery Worker

```bash
cd backend
source .venv/bin/activate
celery -A app.celery worker --loglevel=info
```

### Terminal 3 - Frontend

```bash
cd frontend
npm run dev
```

Redis can run as a background service using:

```bash
brew services start redis
```

## API Architecture

The application follows a REST API architecture.

The frontend communicates with the Flask backend using Axios.

API routes are separated based on user roles:

```text
/api/auth/*
/api/admin/*
/api/company/*
/api/student/*
```

JWT tokens are used to authenticate protected API requests.

## Admin Workflow

The Admin is a pre-existing superuser created programmatically.

Admin can:

```text
Login
  |
  v
View Dashboard
  |
  +----> Manage Users
  |
  +----> Manage Students
  |
  +----> Manage Companies
  |         |
  |         +----> Approve Company
  |         |
  |         +----> Reject Company
  |
  +----> Manage Placement Drives
  |
  +----> View Applications
  |
  +----> Generate Monthly Report
```

## Company Workflow

```text
Register Company
      |
      v
Wait for Admin Approval
      |
      v
Login
      |
      v
Company Dashboard
      |
      +----> Create Placement Drive
      |
      +----> View Placement Drives
      |
      +----> View Student Applications
                  |
                  +----> Mark In Touch
                  |
                  +----> Shortlist
                  |
                  +----> Reject
```

## Student Workflow

```text
Register Student
      |
      v
Login
      |
      v
Student Dashboard
      |
      +----> View Placement Drives
      |
      +----> Apply for Drive
      |
      +----> View Applications
      |
      +----> Track Application Status
      |
      +----> Export Applications as CSV
```

## CSV Export Flow

Student application history is exported asynchronously.

```text
Student Clicks Export CSV
        |
        v
Frontend Sends Export Request
        |
        v
Flask Creates Celery Task
        |
        v
Task Added to Redis Queue
        |
        v
Celery Worker Processes Task
        |
        v
CSV File Generated
        |
        v
Frontend Checks Task Status
        |
        v
CSV Downloaded
```

## Monthly Report Flow

Monthly activity reports are generated asynchronously.

```text
Admin Clicks Generate Report
        |
        v
Frontend Sends Request
        |
        v
Flask Creates Celery Task
        |
        v
Task Added to Redis Queue
        |
        v
Celery Worker Generates Report
        |
        v
HTML Report Saved
        |
        v
Frontend Checks Task Status
        |
        v
Report Downloaded
```

## Security

The application implements:

- JWT-based authentication
- Role-based access control
- Protected backend APIs
- Password hashing
- Admin-only routes
- Company-only routes
- Student-only routes
- User blocking functionality
- Company approval system

Passwords are stored securely using password hashing instead of plain text.

## Key Highlights

- Role-based authentication and authorization
- Separate dashboards for Admin, Company, and Student
- Pre-existing Admin account
- Company registration approval workflow
- Student and Company self-registration
- Placement drive management
- Student application management
- Duplicate application prevention
- Application status tracking
- User blocking and unblocking
- Redis integration
- Celery background task processing
- Asynchronous CSV application export
- Asynchronous Monthly Activity Report generation
- Responsive user interface
- Bootstrap-based UI
- REST API architecture
- SQLite database
- Programmatic database creation

## Future Improvements

The application can be further extended with:

- Scheduled daily reminders for upcoming placement deadlines
- Celery Beat for automatic scheduled jobs
- Automatic monthly report generation
- Email notifications
- Placement drive approval workflow
- Advanced eligibility validation
- API response caching with Redis
- Search and advanced filtering
- Interview scheduling
- Final selection status
- PDF placement reports
- Placement analytics and charts

## Author

**Nicky Yadav**

Student: IIT Madras BS in Data Science and Applications

## License

This project is developed for academic and educational purposes as part of the Modern Application Development II project.

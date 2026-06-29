# AIML Department Management System

A robust, role-based Flask web application designed to streamline academic operations, assignment management, attendance tracking, and administrative workflows for the **Artificial Intelligence & Machine Learning (AIML) Department**.

This portal implements three distinct user portals: **Admin**, **Faculty**, and **Student**, providing customized dashboards and action flows for each role.

---

## 🚀 Features

### 👤 Admin Portal
- **User Management**: Add, update, and manage student and faculty credentials and access rights.
- **Leave Operations**: Review and approve/reject leave requests submitted by faculty and students.
- **System Logs**: Oversee department schedules, announcements, and general system updates.

### 👨‍🏫 Faculty Portal
- **Attendance Registry**: Mark and view student attendance per subject and date.
- **Academics & Grades**: Input and upload results/marks for different courses.
- **Assignment Hub**: Create assignments with descriptions and custom deadlines.
- **Study Materials**: Upload syllabus, books, and lecture notes.
- **Timetable**: View active class schedules.

### 🎓 Student Portal
- **Dashboard Overview**: Check aggregate attendance, semester details, and CGPA/grades.
- **Assignment Submissions**: View posted assignments, track deadlines, and submit files directly through the portal.
- **Timetables & Syllabus**: View daily class timings, classroom numbers, and active courses.
- **Leave Application**: Request leaves and track approval status in real-time.
- **Support Desk**: Open support/ticket requests for administrative help.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask (3.1.3)
- **Database**: SQLite (managed with Flask-SQLAlchemy)
- **Authentication**: Flask-Login (session-based)
- **Security**: Flask-Bcrypt (password hashing)
- **Templating**: Jinja2 (HTML5, CSS3, responsive dark/light layouts)
- **Production Server**: Gunicorn (configured via `Procfile`)

---

## 📦 Directory Structure

```
AIML_DEPT/
│
├── instance/               # SQLite database instance (aiml.db)
├── static/                 # Styling, images, and Javascript
│   └── css/
│       └── style.css       # Core CSS file (dark/light themes)
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base layout template
│   ├── admin_*.html        # Admin dashboards and management views
│   ├── faculty_*.html      # Faculty dashboards, attendance, library, etc.
│   └── student_*.html      # Student dashboards, attendance, submissions, etc.
│
├── models.py               # SQLAlchemy Database Models (User, Attendance, Result, etc.)
├── app.py                  # Main Application logic & routing controller
├── requirements.txt        # Python dependency list
├── Procfile                # Heroku/Gunicorn server deployment config
│
└── seed/script files       # Database initialization & population tools
    ├── init_db.py          # Creates DB schema
    ├── seed_data.py        # Seeds core mock users and courses
    └── populate_academics.py # Populates schedules, academic records, and grades
```

---

## ⚙️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MUKESHKUMAR-21/AIML_DEPT.git
   cd AIML_DEPT
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and Seed Database**:
   Run the setup scripts in order to create the SQLite database and seed it with realistic test data:
   ```bash
   python init_db.py
   python seed_data.py
   python populate_academics.py
   ```

5. **Start Flask Development Server**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 🔒 Default Login Credentials (for Testing)

You can use the following default accounts created by the seed scripts to test different user experiences:

* **Administrator**:
  - **Username**: `admin`
  - **Password**: `admin123`

* **Faculty**:
  - Refer to the database or output of `seed_data.py` / `populate_academics.py` for seeded faculty usernames (usually `faculty1`, `faculty2`, etc. with password `password123`).

* **Student**:
  - Refer to the database or output of `seed_data.py` / `populate_academics.py` for seeded student usernames (usually `student1`, `student2`, etc. with password `password123`).

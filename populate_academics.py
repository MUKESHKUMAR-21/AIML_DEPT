from app import app, db
from models import User, FacultyCredentials, StudentCredentials, Attendance, Result
from datetime import datetime, timedelta
import random

def populate_data():
    courses = [
        "Webtech and Mobile Applications",
        "Principles of AI",
        "Fundamentals of AI",
        "Optimisation Techniques for AI",
        "Python",
        "Java",
        "DBMS"
    ]

    faculties_data = [
        {'username': 'faculty1', 'password': 'faculty123', 'full_name': 'Dr. Alan Turing', 'employee_id': 'AIML-F001', 'designation': 'Professor'},
        {'username': 'faculty2', 'password': 'faculty123', 'full_name': 'Dr. Ada Lovelace', 'employee_id': 'AIML-F002', 'designation': 'Associate Professor'},
        {'username': 'faculty3', 'password': 'faculty123', 'full_name': 'Dr. John McCarthy', 'employee_id': 'AIML-F003', 'designation': 'Assistant Professor'}
    ]

    with app.app_context():
        # 1. Add Faculties
        for data in faculties_data:
            existing = User.query.filter_by(username=data['username']).first()
            if not existing:
                new_user = User(username=data['username'], role='faculty')
                new_user.set_password(data['password'])
                db.session.add(new_user)
                db.session.flush()
                
                profile = FacultyCredentials(
                    user_id=new_user.id,
                    employee_id=data['employee_id'],
                    full_name=data['full_name'],
                    designation=data['designation']
                )
                db.session.add(profile)
        
        # 2. Add Attendance and Results for all students
        students = User.query.filter_by(role='student').all()
        
        # Clear old mock data just in case
        Attendance.query.delete()
        Result.query.delete()
        
        for student in students:
            for course in courses:
                # Add Results
                marks = round(random.uniform(60, 100), 1)
                result = Result(
                    student_id=student.id,
                    subject=course,
                    marks=marks,
                    max_marks=100.0
                )
                db.session.add(result)
                
                # Add Attendance (Mock 5 days of attendance)
                for i in range(5):
                    date = datetime.now().date() - timedelta(days=i)
                    status = 'Present' if random.random() > 0.2 else 'Absent'
                    att = Attendance(
                        student_id=student.id,
                        subject=course,
                        date=date,
                        status=status
                    )
                    db.session.add(att)

        db.session.commit()
        print("Successfully added 3 faculties and populated attendance/results for all students across AIML courses.")

if __name__ == '__main__':
    populate_data()

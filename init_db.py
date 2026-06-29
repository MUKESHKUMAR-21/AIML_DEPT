from app import app, db
from models import User, FacultyCredentials, StudentCredentials

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if admin already exists
        if User.query.filter_by(username='admin').first():
            print("Database already initialized.")
            return

        print("Initializing database with default users...")

        # Create Admin
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # Create Faculty
        faculty_user = User(username='faculty1', role='faculty')
        faculty_user.set_password('faculty123')
        db.session.add(faculty_user)
        db.session.commit() # Commit to get the ID

        faculty_profile = FacultyCredentials(
            user_id=faculty_user.id,
            employee_id='EMP-1001',
            full_name='Dr. Alan Turing',
            designation='Professor',
            qualifications='Ph.D. in Computer Science, M.Sc. in Mathematics'
        )
        db.session.add(faculty_profile)

        # Create Student
        student_user = User(username='student1a', role='student')
        student_user.set_password('student123')
        db.session.add(student_user)
        db.session.commit()

        student_profile = StudentCredentials(
            user_id=student_user.id,
            roll_number='AIML2023001',
            full_name='Ada Lovelace',
            year=3,
            semester=6,
            cgpa=9.8
        )
        db.session.add(student_profile)

        db.session.commit()
        print("Initialization complete!")
        print("Credentials:")
        print("Admin: admin / admin123")
        print("Faculty: faculty1 / faculty123")
        print("Student: student1a / student123")

if __name__ == '__main__':
    init_database()

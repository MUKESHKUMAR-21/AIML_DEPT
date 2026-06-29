from app import app, db
from models import User, FacultyCredentials

def add_more_faculty():
    with app.app_context():
        # 4. Add faculty4 (Dr. Kavitha Natarajan)
        faculty4 = User.query.filter_by(username='faculty4').first()
        if not faculty4:
            faculty4 = User(username='faculty4', role='faculty')
            faculty4.set_password('password')
            db.session.add(faculty4)
            db.session.flush()
            
            profile4 = FacultyCredentials(
                user_id=faculty4.id,
                full_name="Dr. Kavitha Natarajan",
                employee_id="EMP-AIML-004",
                designation="Assistant Professor",
                qualifications="Ph.D. in Computer Science. Focuses on Computer Vision and Medical Image Processing."
            )
            db.session.add(profile4)

        # 5. Add faculty5 (Prof. Senthil Kumar)
        faculty5 = User.query.filter_by(username='faculty5').first()
        if not faculty5:
            faculty5 = User(username='faculty5', role='faculty')
            faculty5.set_password('password')
            db.session.add(faculty5)
            db.session.flush()
            
            profile5 = FacultyCredentials(
                user_id=faculty5.id,
                full_name="Prof. Senthil Kumar",
                employee_id="EMP-AIML-005",
                designation="Guest Lecturer",
                qualifications="M.Tech in Data Analytics. Over 10 years of industry experience working with massive scale data platforms."
            )
            db.session.add(profile5)

        db.session.commit()
        print("2 additional faculty members added successfully!")

if __name__ == "__main__":
    add_more_faculty()

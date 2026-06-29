from app import app, db
from models import User, FacultyCredentials

def update_and_add_faculty():
    with app.app_context():
        # 1. Update existing faculty1
        faculty1 = User.query.filter_by(username='faculty1').first()
        if faculty1:
            profile1 = FacultyCredentials.query.filter_by(user_id=faculty1.id).first()
            if profile1:
                profile1.full_name = "Dr. Karthikeyan Ramasamy"
                profile1.designation = "Head of Department (HOD)"
                profile1.qualifications = "Ph.D. in Artificial Intelligence, M.Tech in Computer Science. 15+ years of research experience in Deep Learning and Computer Vision."
            else:
                profile1 = FacultyCredentials(
                    user_id=faculty1.id, 
                    full_name="Dr. Karthikeyan Ramasamy", 
                    employee_id="EMP-AIML-001",
                    designation="Head of Department (HOD)",
                    qualifications="Ph.D. in Artificial Intelligence, M.Tech in Computer Science."
                )
                db.session.add(profile1)
                
        # 2. Add faculty2 (Dr. Anitha Subramaniam)
        faculty2 = User.query.filter_by(username='faculty2').first()
        if not faculty2:
            faculty2 = User(username='faculty2', role='faculty')
            faculty2.set_password('password')
            db.session.add(faculty2)
            db.session.flush() # Get the ID
            
            profile2 = FacultyCredentials(
                user_id=faculty2.id,
                full_name="Dr. Anitha Subramaniam",
                employee_id="EMP-AIML-002",
                designation="Associate Professor",
                qualifications="Ph.D. in Data Science, B.E. in Electronics. Specializes in Natural Language Processing and big data analytics."
            )
            db.session.add(profile2)

        # 3. Add faculty3 (Prof. Muthukumar Velayutham)
        faculty3 = User.query.filter_by(username='faculty3').first()
        if not faculty3:
            faculty3 = User(username='faculty3', role='faculty')
            faculty3.set_password('password')
            db.session.add(faculty3)
            db.session.flush()
            
            profile3 = FacultyCredentials(
                user_id=faculty3.id,
                full_name="Prof. Muthukumar Velayutham",
                employee_id="EMP-AIML-003",
                designation="Assistant Professor",
                qualifications="M.Tech in Machine Learning. Research interests include Robotics, Reinforcement Learning, and IoT integrations."
            )
            db.session.add(profile3)

        db.session.commit()
        print("Faculty records updated and added successfully!")

if __name__ == "__main__":
    update_and_add_faculty()

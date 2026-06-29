from app import app, db
from models import User, StudentCredentials
from sqlalchemy.exc import IntegrityError

def add_users():
    with app.app_context():
        try:
            # Check if student1a already exists
            existing_user = User.query.filter_by(username='student1a').first()
            if not existing_user:
                student_user = User(username='student1a', role='student')
                student_user.set_password('student123')
                db.session.add(student_user)
                db.session.commit()

                student_profile = StudentCredentials(
                    user_id=student_user.id,
                    roll_number='AIML2023001A',
                    full_name='Ada Lovelace A',
                    year=3,
                    semester=6,
                    cgpa=9.8
                )
                db.session.add(student_profile)
                db.session.commit()
                print("Created student1a successfully.")
            else:
                print("student1a already exists.")
                
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error: {e}")

if __name__ == '__main__':
    add_users()

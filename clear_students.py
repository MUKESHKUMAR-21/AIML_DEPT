from app import app, db
from models import User, StudentCredentials, Attendance, Result, Submission

def clear_students():
    with app.app_context():
        # First get all student users to delete their related records
        students = User.query.filter_by(role='student').all()
        student_ids = [student.id for student in students]

        if student_ids:
            # Delete related records
            Attendance.query.filter(Attendance.student_id.in_(student_ids)).delete(synchronize_session=False)
            Result.query.filter(Result.student_id.in_(student_ids)).delete(synchronize_session=False)
            Submission.query.filter(Submission.student_id.in_(student_ids)).delete(synchronize_session=False)
            StudentCredentials.query.filter(StudentCredentials.user_id.in_(student_ids)).delete(synchronize_session=False)
            
            # Finally delete the user accounts
            User.query.filter(User.id.in_(student_ids)).delete(synchronize_session=False)
            
            db.session.commit()
            print(f"Successfully deleted {len(student_ids)} students and their related records.")
        else:
            print("No students found in the database.")

if __name__ == '__main__':
    clear_students()

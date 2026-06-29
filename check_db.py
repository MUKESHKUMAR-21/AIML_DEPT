from app import app
from models import db, User, FacultyCredentials, StudentCredentials, Announcement

def check_db():
    with app.app_context():
        total_users = User.query.count()
        students = StudentCredentials.query.count()
        faculty = FacultyCredentials.query.count()
        announcements = Announcement.query.count()
        
        print(f"Database Integration Status: SUCCESS")
        print(f"Total Users: {total_users}")
        print(f"Total Students: {students}")
        print(f"Total Faculty: {faculty}")
        print(f"Total Announcements: {announcements}")

if __name__ == '__main__':
    check_db()

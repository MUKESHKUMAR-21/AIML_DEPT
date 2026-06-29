from app import app, db
from models import Announcement
from datetime import datetime, timedelta

def add_announcements():
    announcements = [
        {
            'title': 'National Hackathon 2024 - Registrations Open!',
            'content': 'We are excited to announce that registrations for the National Level AI Hackathon are now open! All 3rd and 4th-year students are encouraged to participate. Cash prizes up to $5000. Form teams of 3-4 members.',
            'target_role': 'student',
            'date_offset': 0
        },
        {
            'title': 'Industrial Visit (IV) to Google Tech Park',
            'content': 'An Industrial Visit is scheduled for all AIML students to the Google Tech Park next Friday. Transportation will be provided from the college campus at 8:00 AM sharp. Please submit your consent forms to your respective class advisors by Wednesday.',
            'target_role': 'student',
            'date_offset': -1
        },
        {
            'title': 'Faculty Development Program on GenAI',
            'content': 'A mandatory 3-day Faculty Development Program (FDP) on Generative AI capabilities in education will be held starting next Monday. All faculty members must ensure they have registered on the faculty portal.',
            'target_role': 'faculty',
            'date_offset': -2
        },
        {
            'title': 'End Semester Exam Schedule Update',
            'content': 'The tentative schedule for the End Semester Examinations has been published. Please check the departmental notice board or the course resources section for detailed timelines. Practical exams commence in 3 weeks.',
            'target_role': 'all',
            'date_offset': -3
        },
        {
            'title': 'Guest Lecture: Future of Quantum Computing in AI',
            'content': 'Dr. Ramanathan from MIT will be delivering an exclusive guest lecture this Saturday at 10:00 AM in the Main Auditorium. Attendance is highly recommended for all AIML department members.',
            'target_role': 'all',
            'date_offset': -4
        }
    ]

    with app.app_context():
        # Clear existing announcements for a fresh start (optional, but requested by user to "add announcements", it's better to just add them)
        added_count = 0
        for data in announcements:
            # Check if announcement with same title exists to prevent duplicates if run multiple times
            existing = Announcement.query.filter_by(title=data['title']).first()
            if not existing:
                date_posted = datetime.utcnow() + timedelta(days=data['date_offset'])
                new_announcement = Announcement(
                    title=data['title'],
                    content=data['content'],
                    target_role=data['target_role'],
                    date_posted=date_posted
                )
                db.session.add(new_announcement)
                added_count += 1
                
        db.session.commit()
        print(f"Successfully added {added_count} new announcements to the database.")

if __name__ == '__main__':
    add_announcements()

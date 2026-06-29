from app import app, db
from models import User, Assignment, Material, ClassSchedule
from datetime import datetime, timedelta, time

def seed_database():
    with app.app_context():
        # Get a faculty user to assign these to
        faculty = User.query.filter_by(role='faculty').first()
        if not faculty:
            print("No faculty user found. Please ensure you have run initialize_db.py first.")
            return
            
        faculty_id = faculty.id
        
        # --- SEED ASSIGNMENTS ---
        print("Seeding Assignments...")
        assignments_data = [
            {"title": "Neural Networks Project Phase 1", "desc": "Implement a basic MLP from scratch using Numpy.", "days": 3},
            {"title": "Data Visualization Assignment", "desc": "Use Matplotlib and Seaborn to visualize the Iris dataset.", "days": 5},
            {"title": "NLP Sentiment Analysis", "desc": "Build a sentiment analysis model using NLTK and logistic regression.", "days": 7},
            {"title": "Midterm Review Quiz", "desc": "Complete the online review quiz for chapters 1-4.", "days": 2},
            {"title": "Computer Vision: Edge Detection", "desc": "Apply Sobel and Canny edge detectors to the provided images.", "days": 10}
        ]
        
        for data in assignments_data:
            a = Assignment(
                faculty_id=faculty_id,
                title=data['title'],
                description=data['desc'],
                deadline=datetime.utcnow() + timedelta(days=data['days'])
            )
            db.session.add(a)
            
        # --- SEED CLASS SCHEDULE ---
        print("Seeding Class Schedule...")
        schedule_data = [
            {"course": "Deep Learning (DL-401)", "day": "Monday", "start": time(9, 0), "end": time(11, 0), "room": "Lab 1"},
            {"course": "Data Structures & Algorithms", "day": "Tuesday", "start": time(11, 15), "end": time(13, 0), "room": "Room 304"},
            {"course": "Computer Vision", "day": "Wednesday", "start": time(10, 0), "end": time(12, 0), "room": "Room 401A"},
            {"course": "Natural Language Processing", "day": "Thursday", "start": time(14, 0), "end": time(16, 0), "room": "Lab 2"},
            {"course": "AI Ethics & Seminar", "day": "Friday", "start": time(15, 0), "end": time(17, 0), "room": "Auditorium"}
        ]
        
        for data in schedule_data:
            c = ClassSchedule(
                course=data['course'],
                day_of_week=data['day'],
                start_time=data['start'],
                end_time=data['end'],
                room_number=data['room'],
                faculty_id=faculty_id
            )
            db.session.add(c)
            
        # --- SEED STUDY MATERIALS ---
        print("Seeding Study Materials...")
        materials_data = [
            {"title": "Week 1: Intro to Machine Learning (Slides)", "url": "https://www.cs.cmu.edu/~tom/10701_sp11/slides/intro.pdf"},
            {"title": "Deep Learning Book - Ian Goodfellow", "url": "https://www.deeplearningbook.org/"},
            {"title": "PyTorch Official Documentation & Tutorials", "url": "https://pytorch.org/tutorials/"},
            {"title": "Dataset: UCI Machine Learning Repository", "url": "https://archive.ics.uci.edu/ml/index.php"}
        ]
        
        for data in materials_data:
            m = Material(
                faculty_id=faculty_id,
                title=data['title'],
                file_url=data['url']
            )
            db.session.add(m)
            
        db.session.commit()
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()

from app import app, db
from models import User, StudentCredentials
from werkzeug.security import generate_password_hash
import random

def generate_students():
    # User provided data - strictly Section A
    base_students = [
        {'username': 'muthesh', 'password': 'muthesh123', 'full_name': 'mutheshkumar', 'roll_number': '241501124', 'year': 2024, 'semester': 4, 'cgpa': 9.5, 'section': 'A'},
        {'username': 'mukilan', 'password': 'mukilan123', 'full_name': 'mukilan', 'roll_number': '241501123', 'year': 2024, 'semester': 4, 'cgpa': 9.0, 'section': 'A'},
        {'username': 'fadil', 'password': 'fadil123', 'full_name': 'mofadil', 'roll_number': '241501114', 'year': 2024, 'semester': 4, 'cgpa': 9.5, 'section': 'A'},
        {'username': 'ashwaq', 'password': 'ashwaq123', 'full_name': 'moashwaq', 'roll_number': '241501113', 'year': 2024, 'semester': 4, 'cgpa': 9.5, 'section': 'A'},
        {'username': 'mohiet', 'password': 'mohiet123', 'full_name': 'mohietjs', 'roll_number': '241501117', 'year': 2024, 'semester': 4, 'cgpa': 8.0, 'section': 'A'}
    ]

    # Tamil names for generation
    first_names = [
        "Aarav", "Adhithya", "Ajay", "Akash", "Anand", "Aravind", "Arjun", "Arun", "Ashwin", "Bala",
        "Bharath", "Chandran", "Dhanush", "Dinesh", "Ganesh", "Gautham", "Gokul", "Hari", "Harish", "Ilan",
        "Jagan", "Jayanth", "Jeeva", "Kannan", "Karthik", "Kavi", "Kishore", "Krishnan", "Kumar", "Madhav",
        "Manoj", "Mithun", "Mohan", "Murali", "Naveen", "Nithish", "Prabhakar", "Pradeep", "Prakash", "Praveen",
        "Prem", "Rahul", "Rajesh", "Ram", "Ramesh", "Ranjith", "Ravi", "Rishi", "Roshan", "Sanjay",
        "Santhosh", "Saravanan", "Sathish", "Selvam", "Senthil", "Shiva", "Siddharth", "Sridhar", "Sriram", "Suresh",
        "Surya", "Varun", "Vasanth", "Venkatesh", "Vignesh", "Vijay", "Vikram", "Vinoth", "Vishal", "Vishnu",
        "Aadhya", "Aarthi", "Abinaya", "Aishwarya", "Akshaya", "Amritha", "Ananya", "Anjali", "Anu", "Aparna",
        "Bhavana", "Charanya", "Deepa", "Deepika", "Dharani", "Divya", "Gayathri", "Geetha", "Gowri", "Harini",
        "Hema", "Indhu", "Ishwarya", "Janani", "Jeevitha", "Kalpana", "Kamala", "Kanimozhi", "Karthika", "Kavitha",
        "Kavya", "Keerthi", "Lavanya", "Madhu", "Maha", "Malathi", "Meena", "Meenakshi", "Mohana", "Monika",
        "Nandhini", "Nithya", "Nivedita", "Pavithra", "Pooja", "Poornima", "Prabha", "Preethi", "Priya", "Priyanka",
        "Radha", "Rajalakshmi", "Ramya", "Rashmi", "Rekha", "Revathi", "Roopa", "Rupa", "Sandhya", "Sangeetha",
        "Santhiya", "Saranya", "Saraswathi", "Sasikala", "Sathya", "Shalini", "Shanthi", "Sharmila", "Shobana", "Shruthi",
        "Sindhu", "Sneha", "Soundarya", "Sowmya", "Sree", "Sruthi", "Sudha", "Sujatha", "Sumathi", "Surya",
        "Swathi", "Swetha", "Tamil", "Uma", "Vandhana", "Vani", "Vasudha", "Vidya", "Vijayalakshmi", "Vimala"
    ]

    last_names = [
        "A", "B", "C", "D", "E", "G", "H", "I", "J", "K", "L", "M", "N", "P", "R", "S", "T", "V"
    ]
    
    sections = ['A', 'B', 'C', 'D']
    
    students = base_students.copy()
    existing_rolls = set(int(s['roll_number']) for s in base_students)
    roll_start = 241501001

    # Generate 120 more students to get > 100 total
    for i in range(120):
        while roll_start in existing_rolls:
            roll_start += 1
            
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        full_name = f"{fname} {lname}"
        
        username = fname.lower() + str(random.randint(10, 999))
        password = username + '123'
        
        # We need to distribute across A, B, C, D (already heavily in A from base)
        # So we'll assign semi-randomly but ensure even distribution
        section = random.choice(sections)
        
        cgpa = round(random.uniform(6.0, 9.9), 1)
        
        student = {
            'username': username,
            'password': password,
            'full_name': full_name,
            'roll_number': str(roll_start),
            'year': 2024,
            'semester': 4,
            'cgpa': cgpa,
            'section': section
        }
        
        students.append(student)
        existing_rolls.add(roll_start)

    return students

def add_students():
    student_data = generate_students()

    with app.app_context():
        added_count = 0
        for data in student_data:
            existing_user = User.query.filter_by(username=data['username']).first()
            if not existing_user:
                new_user = User(username=data['username'], role='student')
                new_user.set_password(data['password'])
                db.session.add(new_user)
                db.session.flush() 
                
                new_student_profile = StudentCredentials(
                    user_id=new_user.id,
                    roll_number=data['roll_number'],
                    full_name=data['full_name'],
                    year=data['year'],
                    semester=data['semester'],
                    cgpa=data['cgpa'],
                    section=data.get('section', 'A')
                )
                db.session.add(new_student_profile)
                added_count += 1
                
        db.session.commit()
        print(f"Successfully added {added_count} new students to the database.")

if __name__ == '__main__':
    add_students()

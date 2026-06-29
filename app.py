from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from models import db, User, FacultyCredentials, StudentCredentials, Attendance, Result, Assignment, Submission, Material, Announcement, Notification, SupportTicket, LeaveRequest, ClassSchedule
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_aiml_dept'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aiml.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

COURSES = [
    "Webtech and Mobile Applications",
    "Principles of AI",
    "Fundamentals of AI",
    "Optimisation Techniques for AI",
    "Python",
    "Java",
    "DBMS"
]

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.context_processor
def inject_user_data():
    if current_user.is_authenticated:
        profile = None
        if current_user.role == 'student':
            profile = StudentCredentials.query.filter_by(user_id=current_user.id).first()
        elif current_user.role == 'faculty':
            profile = FacultyCredentials.query.filter_by(user_id=current_user.id).first()
        
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
        
        counts = {'library': 0, 'assignments': 0, 'attendance': 0, 'results': 0, 'leaves': 0, 'support': 0}
        all_unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
        for n in all_unread:
            if n.category in counts:
                counts[n.category] += 1
            else:
                counts[n.category] = 1
                
        return dict(user_profile=profile, unread_notifications=notifications, unread_counts=counts)
    return dict(user_profile=None, unread_notifications=[], unread_counts={})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_dashboard(current_user.role)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect_dashboard(user.role)
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

def redirect_dashboard(role):
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'faculty':
        return redirect(url_for('faculty_dashboard'))
    elif role == 'student':
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    Notification.query.filter_by(user_id=current_user.id, category='support', is_read=False).update({'is_read': True})
    db.session.commit()
    users = User.query.all()
    faculty = FacultyCredentials.query.all()
    students = StudentCredentials.query.all()
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).all()
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template('admin_dashboard.html', users=users, faculty=faculty, students=students, announcements=announcements, tickets=tickets)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/dashboard/faculty')
@login_required
def faculty_dashboard():
    if current_user.role != 'faculty':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    profile = FacultyCredentials.query.filter_by(user_id=current_user.id).first()
    materials = Material.query.filter_by(faculty_id=current_user.id).all()
    assignments = Assignment.query.filter_by(faculty_id=current_user.id).all()
    section = request.args.get('section', 'A')
    students = StudentCredentials.query.filter_by(section=section).all()
    sections = ['A', 'B', 'C', 'D']
    return render_template('faculty_dashboard.html', profile=profile, materials=materials, assignments=assignments, students=students, current_section=section, sections=sections)

from datetime import datetime

@app.route('/faculty/attendance', methods=['GET', 'POST'])
@login_required
def faculty_attendance():
    if current_user.role != 'faculty':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    section = request.form.get('section') if request.method == 'POST' else request.args.get('section', 'A')
    students = User.query.join(StudentCredentials).filter(User.role=='student', StudentCredentials.section==section).all()
    sections = ['A', 'B', 'C', 'D']
    
    if request.method == 'POST':
        course = request.form.get('course')
        date_str = request.form.get('date')
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            for student in students:
                status = request.form.get(f'status_{student.id}')
                if status:
                    # Check if attendance already marked
                    existing = Attendance.query.filter_by(student_id=student.id, subject=course, date=attendance_date).first()
                    if existing:
                        existing.status = status
                        notif = Notification(user_id=student.id, message=f"Attendance updated for {course}", category='attendance')
                        db.session.add(notif)
                    else:
                        new_att = Attendance(student_id=student.id, subject=course, date=attendance_date, status=status)
                        db.session.add(new_att)
                        notif = Notification(user_id=student.id, message=f"Attendance marked for {course}", category='attendance')
                        db.session.add(notif)
            
            db.session.commit()
            flash(f'Attendance successfully marked for {course} (Section {section}) on {date_str}', 'success')
            return redirect(url_for('faculty_attendance', section=section))
        except Exception as e:
            flash(f'Error processing attendance: {str(e)}', 'danger')
            
    return render_template('faculty_attendance.html', students=students, courses=COURSES, current_section=section, sections=sections)

@app.route('/faculty/results', methods=['GET', 'POST'])
@login_required
def faculty_results():
    if current_user.role != 'faculty':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    section = request.form.get('section') if request.method == 'POST' else request.args.get('section', 'A')
    students = User.query.join(StudentCredentials).filter(User.role=='student', StudentCredentials.section==section).all()
    sections = ['A', 'B', 'C', 'D']
    
    if request.method == 'POST':
        course = request.form.get('course')
        max_marks_str = request.form.get('max_marks', '100')
        
        try:
            max_marks = float(max_marks_str)
            for student in students:
                marks_str = request.form.get(f'marks_{student.id}')
                if marks_str and marks_str.strip() != '':
                    marks = float(marks_str)
                    
                    # Update or Add Result
                    existing = Result.query.filter_by(student_id=student.id, subject=course).first()
                    if existing:
                        existing.marks = marks
                        existing.max_marks = max_marks
                        notif = Notification(user_id=student.id, message=f"Exam result updated for {course}", category='results')
                        db.session.add(notif)
                    else:
                        new_res = Result(student_id=student.id, subject=course, marks=marks, max_marks=max_marks)
                        db.session.add(new_res)
                        notif = Notification(user_id=student.id, message=f"Exam result posted for {course}", category='results')
                        db.session.add(notif)
            
            db.session.commit()
            flash(f'Results successfully posted for {course} (Section {section})', 'success')
            return redirect(url_for('faculty_results', section=section))
        except Exception as e:
            flash(f'Error processing results: {str(e)}', 'danger')
            
    return render_template('faculty_results.html', students=students, courses=COURSES, current_section=section, sections=sections)

@app.route('/dashboard/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    profile = StudentCredentials.query.filter_by(user_id=current_user.id).first()
    announcements = Announcement.query.filter(Announcement.target_role.in_(['all', 'student'])).order_by(Announcement.date_posted.desc()).all()
    materials = Material.query.all()
    all_assignments = Assignment.query.all()
    submissions = Submission.query.filter_by(student_id=current_user.id).all()
    submitted_ids = {sub.assignment_id for sub in submissions}
    assignments = [ass for ass in all_assignments if ass.id not in submitted_ids]
    attendance = Attendance.query.filter_by(student_id=current_user.id).all()
    results = Result.query.filter_by(student_id=current_user.id).all()
    
    # Calculate attendance aggregation
    aggregated_attendance = {}
    for course in COURSES:
        course_records = [r for r in attendance if r.subject == course]
        total = len(course_records)
        if total > 0:
            present = len([r for r in course_records if r.status == 'Present'])
            percentage = round((present / total * 100), 1)
            aggregated_attendance[course] = {
                'total': total,
                'present': present,
                'absent': total - present,
                'percentage': percentage
            }
            
    return render_template('student_dashboard.html', profile=profile, announcements=announcements, materials=materials, assignments=assignments, attendance=attendance, results=results, aggregated_attendance=aggregated_attendance)

@app.route('/student/attendance')
@login_required
def student_attendance():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    Notification.query.filter_by(user_id=current_user.id, category='attendance', is_read=False).update({'is_read': True})
    db.session.commit()
        
    records = Attendance.query.filter_by(student_id=current_user.id).order_by(Attendance.date.desc()).all()
    
    # Calculate aggregation
    aggregated = {}
    for course in COURSES:
        course_records = [r for r in records if r.subject == course]
        total = len(course_records)
        present = len([r for r in course_records if r.status == 'Present'])
        percentage = round((present / total * 100), 1) if total > 0 else 0
        aggregated[course] = {
            'total': total,
            'present': present,
            'absent': total - present,
            'percentage': percentage
        }
        
    return render_template('student_attendance.html', records=records, aggregated=aggregated)

@app.route('/student/results')
@login_required
def student_results():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    Notification.query.filter_by(user_id=current_user.id, category='results', is_read=False).update({'is_read': True})
    db.session.commit()
        
    results = Result.query.filter_by(student_id=current_user.id).all()
    return render_template('student_results.html', results=results)

@app.route('/api/stats')
@login_required
def api_stats():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    admin_count = User.query.filter_by(role='admin').count()
    faculty_count = User.query.filter_by(role='faculty').count()
    student_count = User.query.filter_by(role='student').count()
    
    return jsonify({
        'labels': ['Admin', 'Faculty', 'Student'],
        'data': [admin_count, faculty_count, student_count]
    })

@app.route('/api/announcements', methods=['POST'])
@login_required
def create_announcement():
    if current_user.role not in ['admin', 'faculty']:
        return jsonify({'error': 'Unauthorized'}), 403
    title = request.form.get('title')
    content = request.form.get('content')
    target = request.form.get('target_role', 'all')
    announcement = Announcement(title=title, content=content, target_role=target)
    db.session.add(announcement)
    db.session.commit()
    flash('Announcement posted!', 'success')
    return redirect(request.referrer)

@app.route('/faculty/library', methods=['GET', 'POST'])
@login_required
def faculty_library():
    if current_user.role != 'faculty':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title')
        file_url = request.form.get('file_url')
        material = Material(faculty_id=current_user.id, title=title, file_url=file_url)
        db.session.add(material)
        
        # Notify all students
        students = User.query.filter_by(role='student').all()
        for s in students:
            notif = Notification(user_id=s.id, message=f"New study material: {title}", category='library')
            db.session.add(notif)
            
        db.session.commit()
        flash('Study material uploaded to E-Library!', 'success')
        return redirect(url_for('faculty_library'))
    materials = Material.query.filter_by(faculty_id=current_user.id).order_by(Material.uploaded_at.desc()).all()
    return render_template('faculty_library.html', materials=materials)

@app.route('/faculty/assignments', methods=['GET', 'POST'])
@login_required
def faculty_assignments():
    if current_user.role != 'faculty':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        from datetime import datetime
        deadline = datetime.strptime(request.form.get('deadline'), '%Y-%m-%dT%H:%M')
        assignment = Assignment(faculty_id=current_user.id, title=title, description=description, deadline=deadline)
        db.session.add(assignment)
        
        # Notify all students
        students = User.query.filter_by(role='student').all()
        for s in students:
            notif = Notification(user_id=s.id, message=f"New assignment posted: {title}", category='assignments')
            db.session.add(notif)
            
        db.session.commit()
        flash('Assignment published successfully!', 'success')
        return redirect(url_for('faculty_assignments'))
    assignments = Assignment.query.filter_by(faculty_id=current_user.id).order_by(Assignment.created_at.desc()).all()
    # Fetch submissions for these assignments
    submissions = Submission.query.join(Assignment).filter(Assignment.faculty_id == current_user.id).order_by(Submission.submitted_at.desc()).all()
    return render_template('faculty_assignments.html', assignments=assignments, submissions=submissions)

@app.route('/student/library')
@login_required
def student_library():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    Notification.query.filter_by(user_id=current_user.id, category='library', is_read=False).update({'is_read': True})
    db.session.commit()
    
    materials = Material.query.order_by(Material.uploaded_at.desc()).all()
    return render_template('student_library.html', materials=materials)

@app.route('/student/assignments', methods=['GET', 'POST'])
@login_required
def student_assignments():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        assignment_id = request.form.get('assignment_id')
        file_path = request.form.get('file_path')
        # Check if already submitted
        existing = Submission.query.filter_by(assignment_id=assignment_id, student_id=current_user.id).first()
        if existing:
            existing.file_path = file_path
            existing.status = 'Submitted'
            from datetime import datetime
            existing.submitted_at = datetime.utcnow()
        else:
            submission = Submission(assignment_id=assignment_id, student_id=current_user.id, file_path=file_path, status='Submitted')
            db.session.add(submission)
        db.session.commit()
        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('student_assignments'))
        
    Notification.query.filter_by(user_id=current_user.id, category='assignments', is_read=False).update({'is_read': True})
    db.session.commit()
    
    assignments = Assignment.query.order_by(Assignment.deadline.asc()).all()
    submissions = {sub.assignment_id: sub for sub in Submission.query.filter_by(student_id=current_user.id).all()}
    return render_template('student_assignments.html', assignments=assignments, submissions=submissions)

@app.route('/schedule')
@login_required
def schedule():
    classes = ClassSchedule.query.order_by(ClassSchedule.start_time).all()
    # Group by day
    schedule_dict = {
        'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []
    }
    for c in classes:
        if c.day_of_week in schedule_dict:
            schedule_dict[c.day_of_week].append(c)
    
    faculty_list = FacultyCredentials.query.all()
    return render_template('schedule.html', schedule=schedule_dict, faculty_list=faculty_list)

@app.route('/admin/schedule/add', methods=['POST'])
@login_required
def add_schedule():
    if current_user.role not in ['admin', 'faculty']:
        return jsonify({'error': 'Unauthorized'}), 403
    course = request.form.get('course')
    day_of_week = request.form.get('day_of_week')
    from datetime import datetime
    start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
    end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
    room_number = request.form.get('room_number')
    faculty_id = request.form.get('faculty_id')
    
    new_class = ClassSchedule(course=course, day_of_week=day_of_week, start_time=start_time, end_time=end_time, room_number=room_number, faculty_id=faculty_id)
    db.session.add(new_class)
    db.session.commit()
    flash('Class added to schedule successfully.', 'success')
    return redirect(url_for('schedule'))

@app.route('/admin/schedule/delete/<int:class_id>', methods=['POST'])
@login_required
def delete_schedule(class_id):
    if current_user.role not in ['admin', 'faculty']:
        return jsonify({'error': 'Unauthorized'}), 403
    cls = ClassSchedule.query.get_or_404(class_id)
    db.session.delete(cls)
    db.session.commit()
    flash('Class removed from schedule.', 'info')
    return redirect(url_for('schedule'))

@app.route('/placements')
@login_required
def placements():
    # Mock placement data
    stats = {
        'highest_package': '42 LPA',
        'average_package': '12.5 LPA',
        'placement_rate': '96%',
        'total_offers': 145
    }
    top_recruiters = [
        {'name': 'Google', 'role': 'Software Engineer', 'package': '42 LPA'},
        {'name': 'Amazon', 'role': 'SDE-1', 'package': '35 LPA'},
        {'name': 'Microsoft', 'role': 'Data Scientist', 'package': '38 LPA'},
        {'name': 'TCS Digital', 'role': 'Systems Engineer', 'package': '7.5 LPA'},
        {'name': 'Infosys', 'role': 'Specialist Programmer', 'package': '9.5 LPA'}
    ]
    return render_template('placements.html', stats=stats, top_recruiters=top_recruiters)

@app.route('/student/leaves', methods=['GET', 'POST'])
@login_required
def student_leaves():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        reason = request.form.get('reason')
        from datetime import datetime
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        leave_req = LeaveRequest(student_id=current_user.id, reason=reason, start_date=start_date, end_date=end_date)
        db.session.add(leave_req)
        
        admins = User.query.filter_by(role='admin').all()
        for a in admins:
            notif = Notification(user_id=a.id, message=f"New leave request from {current_user.username}", category='leaves')
            db.session.add(notif)
            
        db.session.commit()
        flash('Leave request submitted successfully.', 'success')
        return redirect(url_for('student_leaves'))
        
    Notification.query.filter_by(user_id=current_user.id, category='leaves', is_read=False).update({'is_read': True})
    db.session.commit()
    
    requests = LeaveRequest.query.filter_by(student_id=current_user.id).order_by(LeaveRequest.applied_at.desc()).all()
    return render_template('student_leaves.html', requests=requests)

@app.route('/admin/leaves')
@login_required
def admin_leaves():
    if current_user.role not in ['admin', 'faculty']:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    Notification.query.filter_by(user_id=current_user.id, category='leaves', is_read=False).update({'is_read': True})
    db.session.commit()
        
    requests = LeaveRequest.query.order_by(LeaveRequest.applied_at.desc()).all()
    return render_template('admin_leaves.html', requests=requests)

@app.route('/admin/leave/update/<int:req_id>', methods=['POST'])
@login_required
def update_leave(req_id):
    if current_user.role not in ['admin', 'faculty']:
        return jsonify({'error': 'Unauthorized'}), 403
    status = request.form.get('status')
    leave_req = LeaveRequest.query.get_or_404(req_id)
    if status in ['Approved', 'Rejected']:
        leave_req.status = status
        
        notif = Notification(user_id=leave_req.student_id, message=f"Leave request has been {status}", category='leaves')
        db.session.add(notif)
        
        db.session.commit()
        flash(f'Leave request {status.lower()}!', 'success')
    return redirect(request.referrer)

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        category = request.form.get('category')
        message = request.form.get('message')
        if category and message:
            ticket = SupportTicket(student_id=current_user.id, category=category, message=message)
            db.session.add(ticket)
            
            admins = User.query.filter_by(role='admin').all()
            for a in admins:
                notif = Notification(user_id=a.id, message=f"New support ticket from {current_user.username}", category='support')
                db.session.add(notif)
                
            db.session.commit()
            flash('Thank you! Your feedback/request has been sent to the Admin.', 'success')
            return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/admin/resolve_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def resolve_ticket(ticket_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = 'Resolved'
    db.session.commit()
    flash('Ticket marked as resolved!', 'success')
    return redirect(request.referrer)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

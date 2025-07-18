from flask import Flask, render_template, request, redirect, url_for, flash, g, session
import sqlite3
import os
import base64
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB

connection = sqlite3.connect('task_manager.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS content
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content_type TEXT NOT NULL,
                video_url TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        budget REAL,
        deadline TEXT,
        skills TEXT,
        assigned_to TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        creator_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS freelancers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        skills TEXT,
        password TEXT,
        points TEXT,
        experiance TEXT,
        rating TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        password TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        subject TEXT,
        message TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create task_files table for output photos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        employee_id TEXT,
        file_path TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eid TEXT,
        rating TEXT,
        review TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employeerequests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        taskid TEXT NOT NULL,
        employeeid TEXT NOT NULL,
        email TEXT NOT NULL,
        skills TEXT NOT NULL, 
        points TEXT NOT NULL,
        status TEXT NOT NULL
    )
''')

connection.commit()
connection.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employer')
def employer():
    return render_template('employer.html')

from flask import session

@app.route('/employerlogin', methods=['POST','GET'])
def employerlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employers WHERE email = ? AND password = ?", [email, password])
        result = cursor.fetchone()

        if result:
            # Assuming result[0] is employer_id and result[1] is email
            session['id'] = result[0] # Store employer ID in session
            session['email'] = result[1]
            
            return redirect(url_for('employer_dashboard'))
        else:
            return render_template('employer.html', msg="Entered wrong credentials")
    return render_template('employer.html')

@app.route('/employersignup', methods=['POST', 'GET'])
def employersignup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO employers (name, email, phone, password) values (?,?,?,?)
        ''', (name, email, phone, password))
        connection.commit()
        return render_template('employer.html', msg="Registered successfully")
    return render_template('employer.html')

@app.route('/freelancer_login', methods=['POST', 'GET'])
def freelancer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute("select * from freelancers where email = ? and password = ?", [email, password])
        result = cursor.fetchone()
        if result:
            session['id'] = result[0]
            session['email'] = result[2]
            session['skills'] = result[3]
            session['points'] = result[5]
            session['ratings'] = result[7]
            return redirect(url_for('freelancer_dashboard'))
        else:
            return render_template('freelancer.html', msg="Entered wrong credantials")
    return render_template('freelancer.html')

@app.route('/freelancer_signup', methods=['POST', 'GET'])
def freelancer_signup():
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        email = request.form['email']
        password = request.form['password']
        skill_level = request.form['skill_level']

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        try:
            if skill_level == 'fresher':
                points = 100
            else:
                points = 50
            rating = 0
            cursor.execute('''
                INSERT INTO freelancers (name, email, skills, password, points, experiance, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, skills, password, points, skill_level, rating))
            connection.commit()

            #  Go back to login page with success message
            return render_template('freelancer.html', msg="Registered successfully!", show_login=True)
        except Exception as e:
            print(e)
            return render_template('freelancer.html', msg="This email already exists. Try with a different email", show_login=True)

    return render_template('freelancer.html', show_login=True)


@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@gmail.com' and password == 'admin123':
            return render_template('admin_login.html')
        else:
            return render_template('admin.html', msg="Entered wrong credantials")
    return render_template('admin.html')

# Employer Dashboard
@app.route('/employer_dashboard')
def employer_dashboard():
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute("select * from tasks")
    total_tasks = cursor.fetchall()

    cursor.execute("select * from freelancers")
    freelancers = cursor.fetchall()

    cursor.execute("select * from messages")
    messages = cursor.fetchall()

    cursor.execute("select * from tasks where status = 'pending'")
    pending_tasks = cursor.fetchall()

    cursor.execute("select * from tasks where status = 'in-progress'")
    in_progress_tasks = cursor.fetchall()

    cursor.execute("select * from tasks where status = 'completed'")
    completed_tasks = cursor.fetchall()


    return render_template('employer_dashboard.html',total_messages = len(messages),  total_tasks = len(total_tasks), total_freelancers = len(freelancers), pending_tasks = len(pending_tasks), in_progress_tasks = len(in_progress_tasks), completed_tasks = len(completed_tasks))

# Freelancers Dashboard
@app.route('/freelancer_dashboard')
def freelancer_dashboard():
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute("select * from tasks where assigned_to = ?", [session['id']])
    total_tasks = cursor.fetchall()


    cursor.execute("select * from tasks where assigned_to = ? and status = 'pending'", [session['id']])
    pending_tasks = cursor.fetchall()

    cursor.execute("select * from tasks where assigned_to = ? and status = 'in-progress'", [session['id']])
    in_progress_tasks = cursor.fetchall()

    cursor.execute("select * from tasks where assigned_to = ? and status = 'completed'", [session['id']])
    completed_tasks = cursor.fetchall()

    return render_template('freelancer_dashboard.html', total_tasks = len(total_tasks), pending_tasks = len(pending_tasks), in_progress_tasks = len(in_progress_tasks), completed_tasks = len(completed_tasks))

@app.route('/employee/tasks/<int:employee_id>')
def employee_tasks(employee_id):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM tasks WHERE assigned_to = ?', (employee_id,))
    tasks = cursor.fetchall()

    return render_template('freelancer_tasks.html', tasks=tasks)


@app.route("/freelancer_tasks")
def freelancer_tasks():
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    freelancer_id = session.get('id')  # Get from session
    return render_template("freelancer_tasks.html", tasks=tasks, freelancer_id=freelancer_id)

@app.route('/my_assigned_tasks')
def my_assigned_tasks():
    """
    Display only tasks assigned to the current freelancer
    """
    if 'id' not in session:
        flash('Please log in to view your assigned tasks', 'error')
        return redirect(url_for('freelancer_login'))
        
    freelancer_id = session.get('id')
    
    try:
        connection = sqlite3.connect('task_manager.db')
        connection.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = connection.cursor()

        # Get tasks assigned to this freelancer with a fresh query
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE assigned_to = ? 
            ORDER BY deadline ASC
        ''', (freelancer_id,))
        
        assigned_tasks = cursor.fetchall()
        
        # Close database connection properly
        cursor.close()
        connection.close()
        
        return render_template('my_assigned_tasks.html', tasks=assigned_tasks, freelancer_id=freelancer_id)
    
    except sqlite3.Error as e:
        # Log the error and show a user-friendly message
        print(f"Database error: {e}")
        flash('Unable to retrieve your assigned tasks. Please try again.', 'error')
        return render_template('my_assigned_tasks.html', tasks=[], freelancer_id=freelancer_id)
    
    finally:
        # Ensure connection is closed even if an error occurs
        if connection:
            connection.close()


@app.route('/tasks')
def tasks():
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id, name FROM freelancers ORDER BY name ASC')
    freelancers = cursor.fetchall()
    
    return render_template('tasks.html', freelancers=freelancers)

@app.route('/freelancer_profile', methods = ['POST', 'GET'])
def freelancer_profile():
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        email = request.form['email']
        password = request.form['password']
        skill_level = request.form.get('skill_level', '')
        
        cursor.execute("UPDATE freelancers SET name = ?, email = ?, skills = ?, password = ?, experiance = ? WHERE id = ?", 
                      [name, email, skills, password, skill_level, session['id']])
        connection.commit()
        flash('Profile updated successfully!', 'success')
        cursor.execute("SELECT * FROM freelancers WHERE id = ?", [session['id']])
        row = cursor.fetchone()
        return render_template('freelancer_profile.html', row=row)
    
    cursor.execute("SELECT * FROM freelancers WHERE id = ?", [session['id']])
    row = cursor.fetchone()
    return render_template('freelancer_profile.html', row=row)

@app.route('/freelancer_list')
def freelancer_list():
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM freelancers')
    freelancers = cursor.fetchall()
    
    return render_template('freelancer_list.html', freelancers=freelancers)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM freelancers WHERE id = ?', (id,))
        connection.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting employee: {str(e)}', 'danger')
    return redirect(url_for('freelancer_list'))

# ADDING TASKS
@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['task-title']
        category = request.form['task-category']
        description = request.form['task-description']
        budget = request.form.get('task-budget', 0)
        deadline = request.form['task-deadline']
        skills = request.form['task-skills']

        try:
            connection = sqlite3.connect('task_manager.db')
            cursor = connection.cursor()
            
            # Get creator ID from session
            creator_id = session.get('id')  # Use .get() to avoid KeyError

            cursor.execute('''
                INSERT INTO tasks (title, category, description, budget, deadline, skills, creator_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, category, description, budget, deadline, skills, creator_id))
            
            connection.commit()
            flash('Task added successfully!', 'success')

        except Exception as e:
            flash(f'Error adding task: {str(e)}', 'danger')

        return redirect(url_for('tasks'))
    
@app.route('/view/<e_id>')
def view(e_id):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM tasks where assigned_to = ?', [e_id])
    tasks = cursor.fetchall()
    
    return render_template('view_task.html', tasks=tasks)
    
# VIEWING TASKS
@app.route('/view_task')
def view_task():
    connection = sqlite3.connect('task_manager.db')
    connection.row_factory = sqlite3.Row  # Enables dict-style access
    cursor = connection.cursor()

    cursor.execute('''
        SELECT t.*, em.name AS employer_name
        FROM tasks t
        LEFT JOIN freelancers em ON t.creator_id = em.id
    ''')
    tasks = cursor.fetchall()

    return render_template('view_task.html', tasks=tasks)

@app.route('/view_task_details/<int:task_id>')
def view_task_details(task_id):
    """
    Display detailed information about a specific task
    """
    connection = sqlite3.connect('task_manager.db')
    connection.row_factory = sqlite3.Row  # Enables dict-style access
    cursor = connection.cursor()

    # Get detailed task information including the employer name
    cursor.execute('''
        SELECT t.*, em.name AS employer_name
        FROM tasks t
        LEFT JOIN employers em ON t.creator_id = em.id
        WHERE t.id = ?
    ''', (task_id,))
    
    task = cursor.fetchone()
    
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('view_task'))
        
    return render_template('task_details.html', task=task)

@app.route('/freelancer_task_details/<int:task_id>')
def freelancer_task_details(task_id):
    # Check if user is logged in
    if 'id' not in session:
        return redirect(url_for('freelancer_login'))
    
    # Connect to database
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    
    # Fetch task details
    cursor.execute('''
        SELECT id, title, category, description, budget, deadline, skills, assigned_to, status, created_at
        FROM tasks 
        WHERE id = ?
    ''', (task_id,))
    
    task_data = cursor.fetchone()
    connection.close()
    
    if not task_data:
        flash('Task not found', 'error')
        return redirect(url_for('freelancer_tasks'))
    
    # Convert task data to dictionary for easier template access
    task = {
        'id': task_data[0],
        'title': task_data[1],
        'category': task_data[2],
        'description': task_data[3],
        'budget': task_data[4],
        'deadline': task_data[5],
        'skills': task_data[6],
        'assigned_to': task_data[7],
        'status': task_data[8],
        'created_at': task_data[9]
    }
    
    return render_template('freelancer_task_details.html', task=task)
    

@app.route('/my_tasks')
def my_tasks():
    if 'id' not in session:
        return redirect('/login')

    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    # Get all tasks created by the logged-in employer
    cursor.execute("SELECT * FROM tasks WHERE creator_id = ?", (session['id'],))
    tasks = cursor.fetchall()

    # Get task IDs with accepted requests (corrected case)
    cursor.execute("SELECT DISTINCT taskid FROM employeerequests WHERE status = 'Accepted'")
    accepted_task_ids = set(row[0] for row in cursor.fetchall())

    # Mark each task with a flag if accepted
    tasks_with_acceptance = []
    for task in tasks:
        task_id = str(task[0])
        is_accepted = task_id in accepted_task_ids
        tasks_with_acceptance.append(task + (is_accepted,))

    connection.close()
    return render_template('employer_tasks.html', tasks=tasks_with_acceptance)



# REQUESTS
@app.route('/sendrequest/<int:task_id>')
def sendrequest(task_id):
    try:
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employeerequests(taskid, employeeid, email, skills, points, status) values (?,?,?,?,?,?)", [task_id, session['id'], session['email'], session['skills'], session['points'], 'pending'])
        connection.commit()
        flash('Request sent successfully!', 'success')
    except Exception as e:
        flash(f'Error sending request: {str(e)}', 'danger')
    return redirect(url_for('freelancer_tasks'))

@app.route('/view_request/<int:task_id>')
def view_request(task_id):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM employeerequests')
    tasks = cursor.fetchall()
    return render_template('view_requests.html',tasks=tasks )

@app.route('/Accept/<int:task_id>')
def Accept(task_id):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    cursor.execute("select * from employeerequests where taskid = ?", [task_id])
    row = cursor.fetchone()
    cursor.execute("update tasks set assigned_to = ? where id = ?", [row[2], task_id])
    cursor.execute("update employeerequests set status = ? where id = ?", ['Accepted', row[0]])
    
    cursor.execute("select * from freelancers where id = ?", [row[2]])
    res = cursor.fetchone()
    points = int(res[5]) + 10
    cursor.execute("update freelancers set points = ? where id = ?", [points, row[2]])
    connection.commit()
    return redirect(url_for('view_task'))

@app.route('/Reject/<int:task_id>')
def Reject(task_id):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    
    # Find the request for this task
    cursor.execute("SELECT * FROM employeerequests WHERE taskid = ?", [task_id])
    row = cursor.fetchone()
    
    if row:
        # Update the request status to 'Rejected'
        cursor.execute("UPDATE employeerequests SET status = ? WHERE id = ?", ['Rejected', row[0]])
        
        # Update the task status but keep it unassigned
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ['rejected', task_id])
        
        connection.commit()
    
    connection.close()
    return redirect(url_for('view_task'))

# TASK DETAILS
@app.route('/viewdetails/<tid>')
def viewdetails(tid):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM task_files where task_id = ? and employee_id = ?', [tid, session['id']])
    photos = cursor.fetchall()
    
    return render_template('view_details.html', photos=photos, tid=tid)

@app.route('/update/<task_id>')
def update(task_id):
    return render_template('update.html', task_id=task_id)

@app.route('/update_task', methods=['GET', 'POST'])
def update_task():
    if request.method == 'POST':
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        task_id = int(request.form['tid'])
        status = request.form['status']
        if status == 'completed':
            points = int(session['points']) + 10
            session['points'] = str(points)
            cursor.execute("update freelancers set points = ? where id = ?", [points, session['id']])
            connection.commit()

        files = request.files.getlist('photos')
        print(files)
        for file in files:
            if file.filename != '':
                file_content = file.read()
                my_string1 = base64.b64encode(file_content).decode('utf-8')
                cursor.execute('''
                    INSERT INTO task_files (task_id, employee_id, file_path)
                    VALUES (?, ?, ?)
                ''', (task_id, session['id'], my_string1))
        cursor.execute("update tasks set status = ? where id = ?", [status, task_id])
        connection.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('freelancer_tasks'))  # Use freelancer_tasks instead, which doesn't require employee_id
    return redirect(url_for('freelancer_tasks'))  # Same here

@app.route('/resources')
def resources():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    pdfs = None
    videos = None

    cursor.execute('''SELECT id, title, description, file_path, created_at 
                FROM content 
                WHERE content_type = 'pdf'
                ORDER BY created_at DESC''')

    pdfs = cursor.fetchall()

    cursor.execute('''SELECT id, title, description, video_url, created_at 
                FROM content 
                WHERE content_type = 'video'
                ORDER BY created_at DESC''')

    videos = cursor.fetchall()

    return render_template('resources.html', pdfs=pdfs, videos=videos)

@app.route('/view_result/<tid>')
def view_result(tid):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM task_files where task_id = ?', [tid])
    photos = cursor.fetchall()
    
    return render_template('view_result.html', photos=photos, tid=tid)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    try:
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        connection.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting task: {str(e)}', 'danger')
    return redirect(url_for('view_task'))

@app.route('/rate_task/<eid>')
def rate_task(eid):
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    return render_template('rate_task.html', eid=eid)

@app.route('/submit_rating', methods=['POST', 'GET'])
def submit_rating():
    if request.method == 'POST':
        eid = request.form['eid']
        rating = int(request.form['rating'])
        review = request.form['review']
        print(eid, rating, review)

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        cursor.execute("insert into reviews values(NULL,?,?,?)", [eid, rating, review])

        if rating == 5:
            cursor.execute("select * from freelancers where id = ?", [eid])
            res = cursor.fetchone()
            points = int(res[5]) + 10
            cursor.execute("update freelancers set points = ? where id = ?", [points, eid])
            
        cursor.execute("select * from reviews where eid = ?", [eid])
        result = cursor.fetchall()
        ratings = 0.0
        for row in result:
            ratings += float(row[2])
        rate = ratings/len(result)
        cursor.execute("update freelancers set rating = ? where id = ?", [rate, eid])

        connection.commit()
        return redirect(url_for('freelancer_list'))
    return redirect(url_for('freelancer_list'))

# MESSAGES
@app.route('/messages', methods=['POST', 'GET'])
def messages():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO messages (name, email, subject, message) values (?,?,?,?)
            ''', (name, email, subject, message))
            connection.commit()
            flash("Message sent successfully", "success")
            return render_template('index.html')
        except Exception as e:
            print(e)
            flash("This email already exists. Try with different email", "error")
            return render_template('index.html')
    
    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()
    cursor.execute("select * from messages")
    msgs = cursor.fetchall()
    return render_template('messages.html', msgs=msgs)

@app.route('/deletemessage/<int:id>')
def deletemessage(id):
    try:
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM messages WHERE id = ?', (id,))
        connection.commit()
        flash('Message deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting employee: {str(e)}', 'danger')
    return redirect(url_for('messages'))

# UPLOADINGING CONTENT FOR SKILL ENHANCEMENT
@app.route('/upload_content', methods=['GET', 'POST'])
def upload_content():
    if request.method == 'POST':
        # Get form data
        title = request.form['contentTitle']
        description = request.form['contentDescription']
        content_type = request.form['contentType']
        
        # Initialize variables
        video_url = None
        file_path = None

        conn = sqlite3.connect('task_manager.db')
        c = conn.cursor()
        
        if content_type == 'video':
            video_url = request.form['videoUrl']
            if not video_url:
                flash('Video URL is required', 'error')
                return redirect(request.url)
            
            # Insert video data into database
            c.execute('''INSERT INTO content 
                        (title, description, content_type, video_url)
                        VALUES (?, ?, ?, ?)''',
                        (title, description, content_type, video_url))
            
        elif content_type == 'pdf':
            if 'pdfFile' not in request.files:
                flash('No file selected', 'error')
                return redirect(request.url)
            
            file = request.files['pdfFile']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                # Check file size
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0)
                
                if file_length > MAX_FILE_SIZE:
                    flash('File size exceeds 25MB limit', 'error')
                    return redirect(request.url)
                
                # Secure filename and save
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                unique_filename = f"{timestamp}_{filename}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                # Create upload folder if it doesn't exist
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(save_path)
                
                # Store relative path in database
                file_path = os.path.join('uploads', unique_filename)
                
                # Insert PDF data into database
                c.execute('''INSERT INTO content 
                            (title, description, content_type, file_path)
                            VALUES (?, ?, ?, ?)''',
                            (title, description, content_type, file_path))
        
        conn.commit()
        flash('Content uploaded successfully!', 'success')
        return render_template('admin_login.html')
    # For GET requests, just render the page
    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
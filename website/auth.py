from flask import Blueprint, render_template, redirect, session, url_for, request, flash
import pymysql, os
import pymysql.cursors

auth = Blueprint('auth', __name__)

def connect_db():
    if os.environ.get('PYTHONANYWHERE'): # Check if running on PyhtonAnywhere
        return pymysql.connect(host=os.environ.get('DB_HOST'),
                               user=os.environ.get('DB_USER'),
                               password=os.environ.get('DB_PASSWORD'),
                               database=os.environ.get('DB_NAME'),
                               cursorclass=pymysql.cursors.DictCursor)
    
    else: # local development XAMPP
        return pymysql.connect(host='localhost', user='root',
                            password='', database='flask_python',
                            cursorclass=pymysql.cursors.DictCursor)

def add_data(name, email, password):
    base = connect_db()
    conn = base.cursor()
    conn.execute("INSERT INTO `blog_project` (name, email, password) VALUES(%s, %s, %s)", (name, email, password))
    base.commit()
    base.close()
    conn.close()

def get_id(email):
    base = connect_db()
    conn = base.cursor()
    conn.execute("SELECT (id) FROM `blog_project` WHERE email = %s", (email))
    result = conn.fetchone()
    base.commit()
    base.close()
    conn.close()
    return result

def check_email(email):
    base = connect_db()
    conn = base.cursor()
    conn.execute("SELECT * FROM `blog_project` WHERE email = %s", (email))
    result = conn.fetchone()
    base.commit()
    base.close()
    conn.close()
    return result

def check_password(password):
    base = connect_db()
    conn = base.cursor()
    conn.execute("SELECT * FROM `blog_project` WHERE password=%s", (password))
    result = conn.fetchone()
    base.commit()
    base.close()
    conn.close()
    return result

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not check_email(email):
            flash('Incorrect Email', category='danger')
        elif not check_password(password):
            flash('Incorrect Password', category='danger')
        else:
            flash('Login Successfully', category='success')
            session['email'] = email
            session['logged_in'] = True
            return redirect(url_for('views.home'))
        
    return render_template('login.html')


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash('Password does not match', category='danger')

        elif len(password) < 4:
            flash('Password must be longer than 4', category='danger')

        elif check_email(email):
            flash('Email already exists', category='danger')

        else:
            add_data(name, email, password)
            flash('Account created successfully', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', category='success')
    return redirect(url_for('views.home'))
    

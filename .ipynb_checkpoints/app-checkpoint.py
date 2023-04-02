import os, hashlib, sqlite3
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'development key'



class User():
    pass

class Database():
    """
    placeholder, to be replaced with sql database later
    """
    
    def __init__(self):
        self.users = {}
    
    def addUser(self, userObject):
        "user object is placeholder object which stores all user data"
        #self.users[userObject.username] = userObject
        ### db implementation:
        con = sqlite3.connect('database.db') 
        cur = con.cursor()

        query = """INSERT INTO users(user_id, email, password, join_date) 
                   VALUES('{}','{}','{}','{}')""".format(userObject.username, "", userObject.password, datetime.today())
        cur.execute(query)
        con.commit()
        con.close()

    def getUser(self, username):
       # if username in self.users:
       #     return self.users[username]
       # else:
       #     return None
        con = sqlite3.connect('database.db') 
        cur = con.cursor() 
        
        query="""SELECT user_id FROM users WHERE user_id = '{}'""".format(username)
        cur.execute(query)
        all_rows = cur.fetchall()
        con.close()
        if (len(all_rows) == 0): # Username not found in database
            return None;
        else:
            return username
        
        
def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

db = Database()

@app.cli.command('initdb')
def initdb_command():
    # Reinitialize the database tables
            
    print('Initialized Database')

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db.getUser(session['user_id'])

@app.route('/')
def default():
    if 'user_id' in session:
        return redirect(url_for('home'))
    g.user = None
    return render_template('layout.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('layout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        user = db.getUser(request.form['username'])
        if user is None:
            error = 'Invalid username'
        elif user.password != hash(request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user.username
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif db.getUser(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            newUser = User()
            newUser.username = request.form['username']
            hashedPassword = hash(request.form['password'])
            newUser.password = hashedPassword
            db.addUser(newUser)
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error, header="Sign Up")

@app.route('/game', methods=['GET', 'POST'])
def game():
    return render_template('game.html')

@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('home'))

import os, hashlib, sqlite3, re
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'development key'

class User():
    def __init__(self, username, password, email, creationTime = None):
        self.username = username
        self.password = password
        self.email = email
        self.creationTime = creationTime

    def __str__(self):
        return F"User Object: {self.username}, password: [...], email: {self.email}"

    def fromDB(data_row):
        # static function: creates User object from database entry
        username, email, password, creationTime = data_row
        return User(username, password, email, creationTime)

class Review():
    def __init__(self, id, gameName, user, date, rating, review):
        self.id = id
        self.gameName = gameName
        self.user = user
        if date:
            self.date = date.split(" ", 1)[0]
        else:
            self.date = "NULL"
        self.rating = rating 
        self.review = review

class Game():
    def __init__(self, title, desc, genreid):
        self.title = title
        self.desc = desc
        self.genre = "None"
        for key in Database.genre_mappings.keys():
            if Database.genre_mappings[key] in genreid:
                if self.genre == "None":
                    self.genre = key
                else:
                    self.genre += (', ' + key)

    def fromDB(data_row):
        genreids = [int(val) for val in data_row[12].strip('][').split(', ')] if data_row[12] != 'None' else []
        return Game(data_row[1], data_row[6], genreids)
        
class Database():
    genre_mappings = { # maps a readable genre to the genre id number, currently genre names are g_ as i dont know what the mapping is
        'g1' : 1,
        'g2' : 2,
        'g3' : 3,
        'g4' : 4,
        'g5' : 5,
        'g6' : 6,
        'g7' : 7,
        'g8' : 8,
        'g9' : 9,
        'g10' : 10,
        'g11' : 11,
        'g12' : 12,
        'g13' : 13,
        'g14' : 14,
        'g15' : 15,
        'g16' : 16,
        'g17' : 17,
        'g18' : 18,
        'g19' : 19,
    }

    def get(query):
        con = sqlite3.connect('database.db') 
        cur = con.cursor() 
        cur.execute(query)
        all_rows = cur.fetchall()
        con.close()
        if (len(all_rows) == 0): # Username not found in database
            return None
        else:
            return all_rows

    def post(query):
        con = sqlite3.connect('database.db') 
        cur = con.cursor()

        cur.execute(query)
        con.commit()
        con.close()

    
    def addUser(self, userObject):
        query = """INSERT INTO users(user_id, email, password, join_date) 
                   VALUES('{}','{}','{}','{}')""".format(userObject.username, userObject.email, userObject.password, datetime.today())
        Database.post(query)

    def getUser(self, username):
        query="""SELECT * FROM users WHERE user_id = '{}'""".format(username)
        all_rows = Database.get(query)
        return User.fromDB(all_rows[0]) if all_rows and len(all_rows) > 0 else None

    def getReviews(self, gameName):
        query="""SELECT * FROM reviews WHERE gameName = '{}'""".format(gameName)
        all_rows = Database.get(query)
        return [Review(*data_row) for data_row in all_rows] if all_rows and len(all_rows) > 0 else []

    def postReview(self, reviewObject):
        query = """INSERT INTO reviews(gameName, user, date, rating, review) 
                   VALUES('{}','{}','{}','{}','{}')""".format(reviewObject.gameName, reviewObject.user.username, datetime.today(), reviewObject.rating, reviewObject.review)
        Database.post(query)

    def getGenre(self, genreid):
        query=F"""SELECT * FROM games WHERE genres LIKE '%{genreid}%' LIMIT 100"""
        all_rows = Database.get(query)

        for data_row in all_rows: # the search query will also return things like genre = 12 when searching for genre = 1 due to the way string matching works
            genreids = [int(val) for val in data_row[12].strip('][').split(', ')] if data_row[12] != 'None' else []
            if int(genreid) not in genreids:
                all_rows.remove(data_row)

        return [Game.fromDB(data_row) for data_row in all_rows][:50] if all_rows and len(all_rows) > 0 else []

    def getGame(self, title):
        query=F"""SELECT * FROM games WHERE game_title LIKE '%{title.lower()}%'"""
        all_rows = Database.get(query)
        return [Game.fromDB(data_row) for data_row in all_rows] if all_rows and len(all_rows) > 0 else []

    def deleteAllUsers(self):
        print("TODO: implement Database.deleteAllUsers")

    
        
def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

db = Database()

@app.cli.command('initdb')
def initdb_command():
    # Reinitialize the database tables
    db.deleteAllUsers()
    db.addUser(User("example", hash("password"), "example@email.com"))
    print('Initialized Database')
    print(db.getUser("example"))

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
            hashedPassword = hash(request.form['password'])
            newUser = User(request.form['username'], hashedPassword, request.form['email'])
            db.addUser(newUser)
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error, header="Sign Up")

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('search', None)
    if query == None:
        return redirect('/')

    if query.startswith('genre:'):
        return redirect(F'/search/genre/{query.replace("genre:", "", 1)}')
        
    return redirect(F'/search/title/{query}')

@app.route('/search/genre/<path:genre>', methods=['GET'])
def search_genre(genre):
    genreid = Database.genre_mappings[genre.lower()]
    games = db.getGenre(genreid)
    games = removeDuplicates(games)
    return render_template('search_results.html', header = genre, games = games)

@app.route('/search/title/<path:title>', methods=['GET'])
def search_title(title):
    games = db.getGame(title)
    games = removeDuplicates(games)
    return render_template('search_results.html', header = title, games = games)

def removeDuplicates(games):
    hashTable = {}

    for game in games:
        if game.title.lower() not in hashTable:
            hashTable[game.title.lower()] = game

    return hashTable.values()



@app.route('/game/<path:gameName>', methods=['GET', 'POST'])
def game(gameName):
    if request.method == 'POST':
        if not g.user:
            flash("You must be logged in to post a review")
        else:
            newReview = Review(None, gameName, g.user, None, request.form['rate'], request.form['review'])
            db.postReview(newReview)

    reviews = db.getReviews(gameName)
    internal_name = re.sub(r'\W+', '', gameName.replace(" ", "_"))
    file_address = F"images/{internal_name}.png"
    return render_template('game.html', header = gameName, reviews = reviews, internal_name = internal_name, file_address = file_address)

@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('home'))

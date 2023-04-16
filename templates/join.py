from flask import Flask, request, abort, url_for, redirect

app = Flask(__name__)



#---------------------------------------------

logout = """<html>
	<head>
        <h4 style="font-weight: bold; font-size: 32px;">You have been Logged out</h4>
	</head>
	<body style="word-wrap: break-word">
        
	</body>
</html>
"""

#---------------------------------------------

register = """{% extends "layout.html" %}
{% block title %}{{header}}{% endblock %}
{% block body %}
  <h2>{{header}}</h2>
  {% if error %}<div class="error"><strong>Error:</strong> {{ error }}</div>{% endif %}
  <form action="" method="post">
    <dl>
      <dt>Username:
      <dd><input type="text" name="username" size="30" value="{{ request.form.username }}">
      <dt>Password:
      <dd><input type="password" name="password" size="30">
      <dt>Password <small>(repeat)</small>:
      <dd><input type="password" name="password2" size="30">
    </dl>
    <div class="actions"><input type="submit" value={{header}}></div>
  </form>
{% endblock %}"""


#---------------------------------------------

login = """
{% extends "layout.html" %}
{% block title %}Sign In{% endblock %}
{% block body %}
  <h2>Sign In</h2>
  {% if error %}<div class="error"><strong>Error:</strong> {{ error }}</div>{% endif %}
  <form action="" method="post">
    <dl>
      <dt>Username:
      <dd><input type="text" name="username" size="30" value="{{ request.form.username }}">
      <dt>Password:
      <dd><input type="password" name="password" size="30">
    </dl>
    <div class="actions"><input type="submit" value="Sign In"></div>
  </form>
{% endblock %} """



#----------------------------------------------
game = """<!DOCTYPE html>
<html>
	<head>
        <h4 style="font-weight: bold; font-size: 24px;">Game Page</h4>
    
	</head>
	<body style="word-wrap: break-word">
        First line of text First line of text First line of text First line of text First line of text </br>
        Second line of text Second line of text Second line of text Second line of text Second line of text </br>
        Third line of text Third line of text Third line of text Third line of text Third line of text </br>
        Fourth line of text Fourth line of text Fourth line of text Fourth line of text Fourth line of text </br>
        </br>
     
        <a href="/">Home</a>

	</body>
</html>
"""


#----------------------------------------------


home = """
<!doctype html>
<title>{% block title %}Welcome{% endblock %}</title>
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
<div class="page">
  <h1>GameRekt</h1>
  <div class="navigation">
  {% if g.user %}
    <a href="/">Home</a> |
    <a href="/logout">Sign Out [{{ g.user.username }}]</a>
    <br />
    
    <a href="/game"><img src="../resources/Minecraft_cover.png" alt="Minecraft"></a>
  {% else %}
    <a href="/register">Sign Up</a> |
    <a href="/login">Sign In</a>
  {% endif %}
  </div>
  
  {% with flashes = get_flashed_messages() %}
    {% if flashes %}
      <ul class="flashes">
      {% for message in flashes %}
        <li>{{ message }}
      {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}

  <div class="body">
  {% block body %}
  {% endblock %}
  </div>

  <br>
  <div class="footer">
    GameRekt &mdash; A Flask ff
  </div>
</div>
"""

#------^^^teammember code in strings^^^--------
#----------------------------------------------
#----------------------------------------------

@app.route("/", methods =['GET'])
def home_controller():
        return home

@app.route("/game", methods =['GET'])
def game_controller():
        return game

@app.route("/login", methods =['GET'])
def login_controller():
        return login

@app.route("/logout", methods =['GET'])
def logout_controller():
        return logout

@app.route("/register", methods =['GET'])
def register_controller():
        return register

if __name__ == "__main__":
    app.run()